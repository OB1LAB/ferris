import React from "react";
import { observer } from "mobx-react-lite";
import { InputNumber } from "rsuite";
import classes from "./Finder.module.scss";

const Pos = ({ logsFilters, setLogsFilters, posNumber }) => {
  return (
    <div className={classes.pos}>
      {posNumber === "first" ? (
        <>
          <InputNumber
            className={classes.posItem}
            type="number"
            placeholder="X1"
            value={logsFilters.dropPrivate.pos1.x}
            onChange={(x) => {
              setLogsFilters({
                ...logsFilters,
                dropPrivate: {
                  ...logsFilters.dropPrivate,
                  pos1: {
                    ...logsFilters.dropPrivate.pos1,
                    x,
                  },
                },
              });
            }}
          />
          <InputNumber
            className={classes.posItem}
            type="number"
            placeholder="Z1"
            value={logsFilters.dropPrivate.pos1.z}
            onChange={(z) => {
              setLogsFilters({
                ...logsFilters,
                dropPrivate: {
                  ...logsFilters.dropPrivate,
                  pos1: {
                    ...logsFilters.dropPrivate.pos1,
                    z,
                  },
                },
              });
            }}
          />
        </>
      ) : posNumber === "second" ? (
        <>
          <InputNumber
            className={classes.posItem}
            type="number"
            placeholder="X2"
            value={logsFilters.dropPrivate.pos2.x}
            onChange={(x) => {
              setLogsFilters({
                ...logsFilters,
                dropPrivate: {
                  ...logsFilters.dropPrivate,
                  pos2: {
                    ...logsFilters.dropPrivate.pos2,
                    x,
                  },
                },
              });
            }}
          />
          <InputNumber
            className={classes.posItem}
            type="number"
            placeholder="Z2"
            value={logsFilters.dropPrivate.pos2.z}
            onChange={(z) => {
              setLogsFilters({
                ...logsFilters,
                dropPrivate: {
                  ...logsFilters.dropPrivate,
                  pos2: {
                    ...logsFilters.dropPrivate.pos2,
                    z,
                  },
                },
              });
            }}
          />
        </>
      ) : (
        <>
          <InputNumber
            className={classes.posItem}
            type="number"
            placeholder="X"
            value={logsFilters.dropPrivate.pos.x}
            onChange={(x) => {
              setLogsFilters({
                ...logsFilters,
                dropPrivate: {
                  ...logsFilters.dropPrivate,
                  pos: {
                    ...logsFilters.dropPrivate.pos,
                    x,
                  },
                },
              });
            }}
          />
          <InputNumber
            className={classes.posItem}
            type="number"
            placeholder="Z"
            value={logsFilters.dropPrivate.pos.z}
            onChange={(z) => {
              setLogsFilters({
                ...logsFilters,
                dropPrivate: {
                  ...logsFilters.dropPrivate,
                  pos: {
                    ...logsFilters.dropPrivate.pos,
                    z,
                  },
                },
              });
            }}
          />
        </>
      )}
    </div>
  );
};

export default observer(Pos);
