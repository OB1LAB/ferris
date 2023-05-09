import React from "react";
import { observer } from "mobx-react-lite";
import ActivityWindow from "../components/Activity/ActivityWindow";

const Activity = () => {
  return (
    <div className="content">
      <ActivityWindow />
    </div>
  );
};
export default observer(Activity);
