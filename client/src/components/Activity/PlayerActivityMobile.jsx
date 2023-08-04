import React, { useContext } from "react";
import classes from "./Activity.module.scss";
import { observer } from "mobx-react-lite";
import { IconButton, Tooltip, Whisper } from "rsuite";
import Trash from "@rsuite/icons/Trash";
import { Context } from "../../main";

const PlayerActivityMobile = ({ player }) => {
  const { store } = useContext(Context);
  return (
    <div>
      <div>
        <div className={classes.mobile_player}>
          <img
            alt={player.Player}
            width={48}
            height={48}
            src={`https://skins.mcskill.net/?name=${player.Player}&mode=5&fx=48&fy=48`}
          />
          <div className={`${classes.mobile_name} ${player.Group}`}>
            {player.Player}
          </div>
          <IconButton
            icon={<Trash />}
            color="red"
            appearance="primary"
            size="md"
            style={{ marginLeft: "auto" }}
            onClick={() => {
              const newStaff = JSON.parse(JSON.stringify(store.staff));
              store.setStaff({
                ...newStaff,
                [store.selected_server]: newStaff[store.selected_server].filter(
                  (line) => line.Player !== player.Player
                ),
              });
            }}
          />
        </div>
        <div className={classes.mobile_data}>
          <div className={classes.mobile_row}>[L]</div>
          <div>{player.local_msg}</div>
        </div>
        <div className={classes.mobile_data}>
          <div className={classes.mobile_row}>[G]</div>
          <div>{player.global_msg}</div>
        </div>
        <div className={classes.mobile_data}>
          <div className={classes.mobile_row}>[PM]</div>
          <div>{player.private_msg}</div>
        </div>
        <div className={classes.mobile_data}>
          <div className={classes.mobile_row}>Warn</div>
          <div>{player.warns}</div>
        </div>
        <div className={classes.mobile_data}>
          <div className={classes.mobile_row}>Mute</div>
          <div>{player.mutes}</div>
        </div>
        <div className={classes.mobile_data}>
          <div className={classes.mobile_row}>Kick</div>
          <div>{player.kicks}</div>
        </div>
        <div className={classes.mobile_data}>
          <div className={classes.mobile_row}>Ban</div>
          <div>{player.bans}</div>
        </div>
        <div className={classes.mobile_data}>
          <div className={classes.mobile_row}>AVG</div>
          <Whisper
            trigger="hover"
            placement="top"
            speaker={
              <Tooltip>
                Средний онлайн без ваниша: {player.AVG_without_vanish}
              </Tooltip>
            }
          >
            <div>
              {player.AVG}
              <br />
              {player.AVG_vanish}
            </div>
          </Whisper>
        </div>
        <div className={classes.mobile_data}>
          <div className={classes.mobile_row}>Total</div>
          <Whisper
            trigger="hover"
            placement="top"
            speaker={
              <Tooltip>
                Общий онлайн без ваниша: {player.Total_without_vanish}
              </Tooltip>
            }
          >
            <div>
              {player.Total}
              <br />
              {player.Total_vanish}
            </div>
          </Whisper>
        </div>
      </div>
    </div>
  );
};

export default observer(PlayerActivityMobile);
