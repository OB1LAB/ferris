import $api from "../http";

export default class infoService {
  static get() {
    return $api.get("/info");
  }
}
