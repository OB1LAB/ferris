import React from "react";
import classes from "./Finder.module.scss";
import { observer } from "mobx-react-lite";

const OutputLogs = ({ logs, loading }) => {
  return (
    <div className={`${classes.outputLogs} ${loading && classes.loading}`}>
      {logs.map((value) => {
        return (
          <div className={classes.msg} key={value.lid}>
            <span>{value.content}</span>
          </div>
        );
      })}
    </div>
  );
};

export default observer(OutputLogs);
