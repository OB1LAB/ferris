import $api from "../http";

export default class ActivityService {
  static getActivity(firstDate, secondDate, players) {
    return $api.post("/getActivity", {
      first_date: firstDate,
      second_date: secondDate,
      players,
    });
  }
}
