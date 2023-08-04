import React, { useContext, useEffect, useState } from "react";
import { observer } from "mobx-react-lite";
import useWindowDimensions from "../useWindowDimensions";
import BigTableActivity from "./BigTableActivity";
import ModalAddPlayer from "./ModalAddPlayer";
import StaffService from "../../services/StaffService";
import ActivityService from "../../services/ActivityService";
import { Context } from "../../main";

function getMondayOfCurrentWeek() {
  const date = new Date();
  const day = date.getDay();
  const diff = date.getDate() - day + (day === 0 ? -6 : 1);
  date.setDate(diff);
  return date;
}

function dateToString(date) {
  let daysSplit = date.toISOString().split("T")[0].split("-");
  return `${daysSplit[2]}-${daysSplit[1]}-${daysSplit[0]}`;
}

const ActivityWindow = () => {
  const { store } = useContext(Context);
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);
  const [date1, setDate1] = useState(getMondayOfCurrentWeek());
  const [date2, setDate2] = useState(new Date());
  const [modalAddPlayer, setModalAddPlayer] = useState(false);
  const { width } = useWindowDimensions();

  const getActivityData = async () => {
    try {
      const response = await StaffService.getStaff();
      const activity = await ActivityService.getActivity(
        dateToString(date1),
        dateToString(date2),
        response.data[store.selected_server].map((item) => item.Player),
        store.selected_server
      );
      setData(activity.data);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);
    getActivityData();
    // eslint-disable-next-line
  }, [store.selected_server, date1, date2]);
  const getHeaderWidth = () => {
    if (width >= 986) {
      if (width < 1400) {
        return (width - 605) / 7;
      } else {
        return 114;
      }
    } else {
      return 55;
    }
  };
  const getTableWidth = () => {
    if (width >= 986) {
      if (width < 1400) {
        return width - 100;
      } else {
        return 1303;
      }
    } else {
      return 890;
    }
  };
  return (
    <div>
      {width >= 922 ? (
        <BigTableActivity
          data={data}
          activityHeaderWidth={getHeaderWidth()}
          widthTable={getTableWidth()}
          date1={date1}
          setDate1={setDate1}
          date2={date2}
          setDate2={setDate2}
          loading={loading}
          setData={setData}
          setModalAddPlayer={setModalAddPlayer}
        />
      ) : (
        <h1>{width}</h1>
      )}
      <ModalAddPlayer open={modalAddPlayer} setOpen={setModalAddPlayer} />
    </div>
  );
};

export default observer(ActivityWindow);
