#include <iostream>
#include <string>
#include <fstream>
#include <ctime>
#include <time.h>
#include <map>
#include <bits/stdc++.h>
using namespace std;
using namespace std::chrono;


struct Player {
    int local_msg = 0;
    int global_msg = 0;
    int private_msg = 0;
    int warns = 0;
    int kicks = 0;
    int mutes = 0;
    int bans = 0;
    int online_time = 0;
    int vanish_time = 0;
    long join_time;
    long exit_time;
    long vanish_join_time;
    long vanish_exit_time;
    char* nickName[16];
    bool online_status = false;
    bool vanish_status = false;
};


string to_lower(string line) {
    int leg_line = line.length();
    for (int i = 0; i < leg_line; ++i) {
        line[i] = tolower(line[i]);
    }
    return line;
}


long to_unixtime(string line) {
    tm t{};
    istringstream ss(line);
    ss >> get_time(&t, "%d-%m-%Y[%H:%M:%S]");
    return static_cast<long>(mktime(&t));
}


vector<string> split(string line, char delimiter) {
    vector<string> result;
    string buff;
    stringstream ss(line);
    while(getline(ss, buff, delimiter)){
        result.push_back(buff);
    }
    return result;
}


Player *activity(const char* players[], const char* days[], char* path, bool before_day) {
    ifstream file;
    int players_count = 0;
    int days_count = 0;
    string line = "";
    string str_path = string(path);
    map<string, Player> player_list;
    for (int i = 0; players[i] != nullptr; ++i) {
        char* nick_name = new char[16];
        strncpy(nick_name, players[i], 16);
        player_list[players[i]] = Player{.nickName = nick_name};
        players_count++;
    }
    for (int j = 0; days[j] != nullptr; ++j) {
        file.open(str_path + '/' + days[j] + ".txt");
        if (!file.is_open()) {
            break;
        }
        switch(before_day) {
        case true:
            while (!file.eof()) {
                getline(file, line);
                vector<string> log = split(line, ' ');
                if (log.size() == 3 && player_list.contains(log[{1}])) {
                    if (log[{2}] == "зашёл" && not player_list[log[{1}]].online_status) {
                        player_list[log[{1}]].join_time = to_unixtime(days[j+1]+string("[00:00:00]"));
                        player_list[log[{1}]].online_status = true;
                    } else if (log[{2}] == "вышел" && player_list[log[{1}]].online_status) {
                        player_list[log[{1}]].online_status = false;
                        player_list[log[{1}]].vanish_status = false;
                    }
                } else if (log.size() > 5 && player_list.contains(log[{1}])) {
                    if (to_lower(log[{2}]) == "/vanish") {
                        switch(player_list[log[{1}]].vanish_status) {
                        case true:
                            player_list[log[{1}]].vanish_status = false;
                            break;
                        default:
                            player_list[log[{1}]].vanish_join_time = to_unixtime(days[j+1]+string("[00:00:00]"));
                            player_list[log[{1}]].vanish_status = true;
                            break;
                        }
                    }
                }
            }
            before_day = false;
            break;
        default:
            while (!file.eof()) {
                getline(file, line);
                vector<string> log = split(line, ' ');
                if (log.size() == 3 && player_list.contains(log[{1}])) {
                    if (log[{2}] == "зашёл" && not player_list[log[{1}]].online_status) {
                        player_list[log[{1}]].online_status = true;
                        player_list[log[{1}]].join_time = to_unixtime(days[j]+log[{0}]);
                    } else if (log[{2}] == "вышел" && player_list[log[{1}]].online_status) {
                        player_list[log[{1}]].online_status = false;
                        player_list[log[{1}]].exit_time = to_unixtime(days[j]+log[{0}]);
                        player_list[log[{1}]].online_time += player_list[log[{1}]].exit_time - player_list[log[{1}]].join_time;
                        switch(player_list[log[{1}]].vanish_status) {
                        case true:
                            player_list[log[{1}]].vanish_status = false;
                            player_list[log[{1}]].vanish_exit_time = to_unixtime(days[j]+log[{0}]);
                            player_list[log[{1}]].vanish_time += player_list[log[{1}]].vanish_exit_time - player_list[log[{1}]].vanish_join_time;
                            break;
                        }
                    }
                } else if (log.size() > 3 && player_list.contains(split(log[{2}], ':')[{0}])) {
                    if (log[{1}] == "[L]") {
                        player_list[split(log[{2}], ':')[{0}]].local_msg++;
                    } else {
                        player_list[split(log[{2}], ':')[{0}]].global_msg++;
                    }
                } else if (log.size() > 5 && player_list.contains(log[{1}])) {
                    switch(player_list[log[{1}]].online_status) {
                    case false:
                        player_list[log[{1}]].join_time = to_unixtime(days[j]+log[{0}]);
                        player_list[log[{1}]].online_status = true;
                        break;
                    }
                    string command = to_lower(log[{5}]);
                    if (
                        ((command == "/tell" || command == "/m" || command == "/w" || command == "/msg" || command == "/pm" || command == "/t" || command == "/whisper" || command == "/mail") && log.size() > 7)
                        || (command == "/r" && log.size() > 6)
                        ) {
                        player_list[log[{1}]].private_msg++;
                    } else if (command == "/vanish") {
                        switch(player_list[log[{1}]].vanish_status) {
                        case true:
                            player_list[log[{1}]].vanish_status = false;
                            player_list[log[{1}]].vanish_exit_time = to_unixtime(days[j]+log[{0}]);
                            player_list[log[{1}]].vanish_time += player_list[log[{1}]].vanish_exit_time - player_list[log[{1}]].vanish_join_time;
                            break;
                        default:
                            player_list[log[{1}]].vanish_status = true;
                            player_list[log[{1}]].vanish_join_time = to_unixtime(days[j]+log[{0}]);
                            break;
                        }
                    } else if(command == "/warn" && log.size() > 6) {
                        player_list[log[{1}]].warns++;
                    } else if(command == "/kick" && log.size() > 6) {
                        player_list[log[{1}]].kicks++;
                    } else if((command == "/mute" && log.size() > 6) || (command == "/tempmute" && log.size() > 9)) {
                        player_list[log[{1}]].mutes++;
                    } else if((command == "/ban" && log.size() > 6) || (command == "/tempban" && log.size() > 9)) {
                        player_list[log[{1}]].bans++;
                    }
                }
            }   
            break;
        }
        days_count++;
        file.close();
    }
    Player* players_array = new Player[players_count];
    for (int k = 0; players[k] != nullptr; ++k) {
        vector<string> log = split(line, ' ');
        if (player_list[players[k]].online_status) {
            player_list[players[k]].online_time += to_unixtime(days[days_count-1]+log[{0}]) - player_list[players[k]].join_time;
        }
        if (player_list[players[k]].vanish_status) {
            player_list[players[k]].vanish_time += to_unixtime(days[days_count-1]+log[{0}]) - player_list[players[k]].vanish_join_time;
        }
        players_array[k] = player_list[players[k]];
    }
    return players_array;
}


extern "C" __declspec(dllexport) Player *getActivity(const char* players[], const char* days[], char* path_logs, bool before_day) {
    return activity(players, days, path_logs, before_day);
}
