import React from "react";
import { observer } from "mobx-react-lite";
import classes from "./Activity.module.scss";

const BigPlayerActivity = ({ Player, group }) => {
  return (
    <div className={classes.bigPlayerActivity}>
      <img
        alt={Player}
        width={48}
        src={`https://skins.mcskill.net/?name=${Player}&mode=5&fx=48&fy=48`}
      />
      <div className={`${classes.nickName} ${group}`}>{Player}</div>
    </div>
  );
};

export default observer(BigPlayerActivity);
