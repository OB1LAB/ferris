import React, { useContext, useEffect, useState } from "react";
import { observer } from "mobx-react-lite";
import useWindowDimensions from "../components/useWindowDimensions";
import BigTableActivity from "../components/Activity/BigTableActivity";
import ModalAddPlayer from "../components/Activity//ModalAddPlayer";
import ActivityService from "../services/ActivityService";
import { Context } from "../main";
import BigTablePayerActivityMobile from "../components/Activity/BigTablePayerActivityMobile";

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

const Activity = () => {
  const { store } = useContext(Context);
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);
  const [date1, setDate1] = useState(getMondayOfCurrentWeek());
  const [date2, setDate2] = useState(new Date());
  const [modalAddPlayer, setModalAddPlayer] = useState(false);
  const { width } = useWindowDimensions();

  const getActivityData = async () => {
    try {
      setLoading(true);
      if (store.staff[store.selected_server]) {
        const activity = await ActivityService.getActivity(
          dateToString(date1),
          dateToString(date2),
          store.staff[store.selected_server],
          store.selected_server
        );
        setData(activity.data);
      }
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
  }, [store.selected_server, date1, date2, store.staff]);
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
    <div className="content">
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
          setModalAddPlayer={setModalAddPlayer}
        />
      ) : (
        <BigTablePayerActivityMobile
          data={data}
          date1={date1}
          setDate1={setDate1}
          date2={date2}
          setDate2={setDate2}
          loading={loading}
          setModalAddPlayer={setModalAddPlayer}
        />
      )}
      <ModalAddPlayer
        open={modalAddPlayer}
        setOpen={setModalAddPlayer}
        server={store.selected_server}
      />
    </div>
  );
};

export default observer(Activity);
