import React, { useContext } from "react";
import { Link, useLocation } from "react-router-dom";
import { Context } from "../../main";
import { observer } from "mobx-react-lite";
import useWindowDimensions from "../useWindowDimensions";
import {
  INDEX_ROUTE,
  ACTIVITY_ROUTE,
  PARSER_ROUTE,
  FINDER_ROUTE,
} from "../../router/const";
import { Nav, Toggle } from "rsuite";
import Pc from "@rsuite/icons/legacy/Pc";
import HomeIcon from "@rsuite/icons/legacy/Home";
import Sun from "@rsuite/icons/legacy/SunO";
import Moon from "@rsuite/icons/legacy/MoonO";
import Search from "@rsuite/icons/legacy/Search";
import Server from "@rsuite/icons/legacy/Server";
import Commenting from "@rsuite/icons/legacy/Commenting";
import classes from "./Navigations.module.scss";

const Navigation = () => {
  const { store } = useContext(Context);
  const location = useLocation();
  const { width } = useWindowDimensions();
  const getColor = (path) => {
    if (path === location.pathname) {
      return `rs-nav-item-active ${classes.navItem}`;
    }
    return "";
  };
  return (
    <Nav appearance="subtle" className={classes.navBar}>
      <Nav.Item
        as={Link}
        to={ACTIVITY_ROUTE}
        className={getColor(ACTIVITY_ROUTE)}
        icon={<Pc />}
      >
        {width >= 700 && "Игровая активность"}
      </Nav.Item>
      <Nav.Item
        as={Link}
        to={PARSER_ROUTE}
        className={getColor(PARSER_ROUTE)}
        icon={<Commenting />}
      >
        {width >= 700 && "Парсер"}
      </Nav.Item>
      <Nav.Item
        as={Link}
        to={FINDER_ROUTE}
        className={getColor(FINDER_ROUTE)}
        icon={<Search />}
      >
        {width >= 700 && "Поиск"}
      </Nav.Item>
      <Nav.Item
        as={Link}
        to={INDEX_ROUTE}
        className={getColor(INDEX_ROUTE)}
        icon={<HomeIcon />}
      >
        {width >= 700 && "Информация"}
      </Nav.Item>
      <Nav.Menu icon={<Server />} title={store.selected_server}>
        <Nav.Item onClick={() => store.setSelectedServer("HTC Titan")}>
          HTC Titan
        </Nav.Item>
        <Nav.Item onClick={() => store.setSelectedServer("HTC Phobos")}>
          HTC Phobos
        </Nav.Item>
        <Nav.Item onClick={() => store.setSelectedServer("HTC Elara")}>
          HTC Elara
        </Nav.Item>
      </Nav.Menu>
      <Nav.Item
        as={Toggle}
        checkedChildren={<Sun />}
        unCheckedChildren={<Moon />}
        defaultChecked={localStorage.getItem("theme") === "light"}
        onChange={(checked) => store.changeTheme(checked)}
      ></Nav.Item>
    </Nav>
  );
};

export default observer(Navigation);
