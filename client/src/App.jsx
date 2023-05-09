import { useContext } from "react";
import { Context } from "./main";
import { observer } from "mobx-react-lite";
import { BrowserRouter } from "react-router-dom";
import Navigation from "./components/navBar/Navigations";
import AppRouter from "./components/navBar/AppRouter";
import { CustomProvider, Loader } from "rsuite";
import "./App.scss";
import "rsuite/dist/rsuite.min.css";

function App() {
  const { store } = useContext(Context);
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
