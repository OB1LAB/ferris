import React from "react";
import classes from "./Activity.module.scss";
import { observer } from "mobx-react-lite";
import { DatePicker, IconButton, Loader } from "rsuite";
import Plus from "@rsuite/icons/Plus";
import PlayerActivityMobile from "./PlayerActivityMobile";

const BigTableActivityMobile = ({
  data,
  date1,
  setDate1,
  date2,
  setDate2,
  loading,
  setModalAddPlayer,
}) => {
  return (
    <div className={classes.mobile_activity_zone}>
      <div className={classes.mobile_buttons}>
        <div className={classes.dates}>
          <DatePicker
            oneTap
            isoWeek
            cleanable={false}
            value={date1}
            onChange={setDate1}
          />
          <DatePicker
            oneTap
            isoWeek
            cleanable={false}
            value={date2}
            onChange={setDate2}
          />
        </div>
        <div>
          <IconButton
            icon={<Plus />}
            color="green"
            appearance="primary"
            size="sm"
            onClick={() => setModalAddPlayer(true)}
          />
        </div>
      </div>
      {data.length > 0 ? (
        <div
          className={`${classes.mobile_activity} ${loading && classes.loading}`}
        >
          {data.map((line) => (
            <PlayerActivityMobile key={line.Player} player={line} />
          ))}
        </div>
      ) : (
        <div style={{ marginTop: "25px" }}>
          {!loading && "Список игроков пустой"}
        </div>
      )}
      {loading && <Loader size="sm" center content="Загрузка..." />}
    </div>
  );
};

export default observer(BigTableActivityMobile);
