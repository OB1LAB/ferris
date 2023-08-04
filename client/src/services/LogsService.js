import $api from "../http";

export default class LogsService {
  static downloadLogs(server) {
    return $api.get(`/logs?server=${server}`);
  }
  static openLogsFolder() {
    return $api.post("/logs");
  }
}
