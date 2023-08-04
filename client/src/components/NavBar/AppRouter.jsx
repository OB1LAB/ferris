import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { routes } from "../../router/index";
import { INDEX_ROUTE } from "../../router/const";
import { observer } from "mobx-react-lite";

const AppRouter = () => {
  return (
    <Routes>
      {routes.map(({ path, Element }) => {
        return <Route key={path} path={path} element={Element} exact />;
      })}
      <Route path="*" element={<Navigate to={INDEX_ROUTE} />} />
    </Routes>
  );
};

export default observer(AppRouter);
