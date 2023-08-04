import Index from "../pages/Index";
import Parser from "../pages/Parser";
import {
  INDEX_ROUTE,
  ACTIVITY_ROUTE,
  PARSER_ROUTE,
  FINDER_ROUTE,
} from "./const";
import Finder from "../pages/Finder";
import Activity from "../pages/Activity";

export const routes = [
  {
    path: INDEX_ROUTE,
    Element: <Index />,
  },
  {
    path: ACTIVITY_ROUTE,
    Element: <Activity />,
  },
  {
    path: PARSER_ROUTE,
    Element: <Parser />,
  },
  {
    path: FINDER_ROUTE,
    Element: <Finder />,
  },
];
