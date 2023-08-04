import $api from "../http";

export default class FinderService {
  static globalFind(firstDate, secondDate, findData, server) {
    return $api.post("/finder", {
      first_date: firstDate,
      second_date: secondDate,
      findData,
      server,
    });
  }
}
