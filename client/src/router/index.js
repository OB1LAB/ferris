import Index from "../pages/Index";
import Activity from "../pages/Activity";
import Parser from "../pages/Parser";
import { INDEX_ROUTE, ACTIVITY_ROUTE, PARSER_ROUTE } from "./consts";

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
];
