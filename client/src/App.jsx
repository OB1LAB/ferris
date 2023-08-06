import { useContext, useEffect } from "react";
import { observer } from "mobx-react-lite";
import { BrowserRouter } from "react-router-dom";
import { io } from "socket.io-client";
import { Context } from "./main";
import Navigation from "./components/NavBar/Navigation";
import AppRouter from "./components/NavBar/AppRouter";
import StaffService from "./services/StaffService";
import { CustomProvider, Loader, useToaster, Notification } from "rsuite";
import "./App.scss";
import "rsuite/dist/rsuite.min.css";
import InfoService from "./services/InfoService";

function App() {
  const { store } = useContext(Context);
  const toaster = useToaster();

  const getStaff = async () => {
    try {
      const response = await StaffService.getStaff();
      store.setStaff(response.data);
    } catch (err) {
      console.log(err);
    }
  };

  const getServerInfo = async () => {
    try {
      const response = await InfoService.get();
      store.setActualVersion(response.data.actual_version);
      store.setLastLogsUpdate(response.data.last_update)
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    const socket = io(`http://${window.location.hostname}:8000`);
    store.setSocket(socket);
    store.socket.on("connect", () => {
      store.setSocketConnect(true);
    });
    store.socket.on("error", (errorMsg) => {
      toaster.push(
        <Notification type="error" header="Ошибка" closable>
          {errorMsg}
        </Notification>,
        { placement: "topEnd" }
      );
    });
    getStaff();
    getServerInfo();
    if (store.socket) {
      return () => store.socket.disconnect();
    }
  }, []);

  if (store.isLoading) {
    return <Loader backdrop content="Загрузка..." vertical />;
  }

  return (
    <CustomProvider theme={store.theme}>
      <div className="App">
        <BrowserRouter>
          <Navigation />
          <AppRouter />
        </BrowserRouter>
      </div>
    </CustomProvider>
  );
}

export default observer(App);
