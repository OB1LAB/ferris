import $api from "../http";

export default class InfoService {
  static get() {
    return $api.get("/info");
  }
}
