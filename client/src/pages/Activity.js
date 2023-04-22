import React, { useEffect } from "react";
import { observer } from "mobx-react-lite";
import ActivityService from "../services/ActivityService";
import classes from "../styles/Activity.scss";
import ActivityWindow from "../components/Activity/ActivityWindow";

const Activity = () => {
  return (
    <div className="content">
      <ActivityWindow />
    </div>
  );
};
export default observer(Activity);
