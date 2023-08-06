import { makeAutoObservable } from "mobx";

export default class Store {
  isLoading = false;
  theme = localStorage.getItem("theme") || "dark";
  selected_server = localStorage.getItem("selected_server") || "HTC Elara";
  socket = null;
  socketIsConnected = false;
  staff = {};
  actualVersion = null;
  lastLogsUpdate = null;
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
  setSocketConnect(bool) {
    this.socketIsConnected = bool;
  }
  setSocket(socket) {
    this.socket = socket;
  }
  setStaff(staff) {
    this.staff = staff;
  }
  setActualVersion(actualVersion) {
    this.actualVersion = actualVersion;
  }
  setLastLogsUpdate(dateTime) {
    this.lastLogsUpdate = dateTime;
  }
}
