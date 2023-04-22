import $api from "../http";

export default class StaffService {
  static getStaff(firstDate, secondDate, players) {
    return $api.get("/getStaff");
  }
}
