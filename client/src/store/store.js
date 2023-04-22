import { makeAutoObservable } from "mobx";

export default class Store {
  user = {};
  isLoading = false;
  theme = localStorage.getItem("theme") || "dark";
  selected_server = localStorage.getItem("selected_server") || "HTC Elara";
  constructor() {
    makeAutoObservable(this);
  }
  setLoading(bool) {
    this.isLoading = bool;
  }
  setSelectedServer(server) {
    this.selected_server = server;
    localStorage.setItem("selected_server", server);
  }
  changeTheme(bool) {
    if (bool) {
      this.theme = "light";
    } else {
      this.theme = "dark";
    }
    localStorage.setItem("theme", this.theme);
  }
}
