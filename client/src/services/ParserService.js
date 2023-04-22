import $api from "../http";

export default class ParserService {
  static getLogs(offset) {
    return $api.get(`/parser?offset=${offset}`);
  }
  static sendMsg(msg) {
    return $api.post(`/parser`, {
      msg,
    });
  }
}
