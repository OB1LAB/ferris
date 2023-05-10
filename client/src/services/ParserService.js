import $api from "../http";

export default class ParserService {
  static getData() {
    return $api.get(`/parser`);
  }
  static sendMsg(msg) {
    return $api.post(`/parser`, {
      msg,
    });
  }
}
