import requests

r = requests.get('https://mcskill.net/api/v2/?section=admin&action=get_crew').json()
for i in r:
    print(i['title'])
    for j in i['moders']:
        if j['group'] in ['helper1', 'helper2', 'moder']:
            print(j)
