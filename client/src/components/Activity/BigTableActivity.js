import React from "react";
import classes from "./Activity.module.scss";
import { observer } from "mobx-react-lite";
import { DatePicker, IconButton, Table } from "rsuite";
import Trash from "@rsuite/icons/Trash";
import Plus from "@rsuite/icons/Plus";
import BigPlayerActivity from "./BigPlayerActivity";

const { Column, HeaderCell, Cell } = Table;

const BigTableActivity = ({
  data,
  setData,
  widthTable,
  activityHeaderWidth,
  date1,
  setDate1,
  date2,
  setDate2,
  loading,
  setModalAddPlayer,
}) => {
  return (
    <Table
      data={data}
      width={widthTable}
      rowHeight={74}
      headerHeight={50}
      className={classes.activityTable}
      disabledScroll
      autoHeight
      hover={false}
      locale={{
        emptyMessage: "Список игроков пустой",
        loading: "Загружаем список игроков...",
      }}
    >
      <Column width={275}>
        <HeaderCell align="center">
          <div className={classes.dates}>
            <DatePicker
              oneTap
              cleanable={false}
              value={date1}
              onChange={setDate1}
            />
            <DatePicker
              oneTap
              cleanable={false}
              value={date2}
              onChange={setDate2}
            />
          </div>
        </HeaderCell>
        <Cell verticalAlign="middle">
          {(rowData) => <BigPlayerActivity Player={rowData.Player} />}
        </Cell>
      </Column>

      <Column width={activityHeaderWidth}>
        <HeaderCell
          className={classes.cellHeader}
          align="left"
          verticalAlign="middle"
        >
          [L]
        </HeaderCell>
        <Cell
          className={classes.cellSize}
          verticalAlign="middle"
          dataKey="local_msg"
        />
      </Column>

      <Column width={activityHeaderWidth}>
        <HeaderCell
          verticalAlign="middle"
          className={classes.cellHeader}
          align="left"
        >
          [G]
        </HeaderCell>
        <Cell
          className={classes.cellSize}
          verticalAlign="middle"
          dataKey="global_msg"
        />
      </Column>

      <Column width={activityHeaderWidth}>
        <HeaderCell
          verticalAlign="middle"
          className={classes.cellHeader}
          align="left"
        >
          [PM]
        </HeaderCell>
        <Cell
          className={classes.cellSize}
          verticalAlign="middle"
          dataKey="private_msg"
        />
      </Column>

      <Column width={activityHeaderWidth}>
        <HeaderCell
          verticalAlign="middle"
          className={classes.cellHeader}
          align="left"
        >
          Warn
        </HeaderCell>
        <Cell
          className={classes.cellSize}
          verticalAlign="middle"
          dataKey="warns"
        />
      </Column>

      <Column width={activityHeaderWidth}>
        <HeaderCell
          verticalAlign="middle"
          className={classes.cellHeader}
          align="left"
        >
          Mute
        </HeaderCell>
        <Cell
          className={classes.cellSize}
          verticalAlign="middle"
          dataKey="kicks"
        />
      </Column>

      <Column width={activityHeaderWidth}>
        <HeaderCell
          verticalAlign="middle"
          className={classes.cellHeader}
          align="left"
        >
          Kick
        </HeaderCell>
        <Cell
          className={classes.cellSize}
          verticalAlign="middle"
          dataKey="mutes"
        />
      </Column>
      <Column width={activityHeaderWidth}>
        <HeaderCell
          verticalAlign="middle"
          className={classes.cellHeader}
          align="left"
        >
          Ban
        </HeaderCell>
        <Cell
          className={classes.cellSize}
          verticalAlign="middle"
          dataKey="bans"
        />
      </Column>
      <Column width={84}>
        <HeaderCell
          verticalAlign="middle"
          className={classes.cellHeader}
          align="center"
        >
          AVG
        </HeaderCell>
        <Cell
          className={classes.cellSize}
          verticalAlign="middle"
          align="center"
        >
          {(rowData) => (
            <div dangerouslySetInnerHTML={{ __html: rowData.AVG }}></div>
          )}
        </Cell>
      </Column>
      <Column width={84}>
        <HeaderCell
          verticalAlign="middle"
          className={classes.cellHeader}
          align="center"
        >
          Total
        </HeaderCell>
        <Cell
          className={classes.cellSize}
          verticalAlign="middle"
          align="center"
        >
          {(rowData) => (
            <div dangerouslySetInnerHTML={{ __html: rowData.Total }}></div>
          )}
        </Cell>
      </Column>
      <Column width={62}>
        <HeaderCell align="center">
          <IconButton
            icon={<Plus />}
            color="green"
            appearance="primary"
            size="sm"
            onClick={() => setModalAddPlayer(true)}
          />
        </HeaderCell>
        <Cell verticalAlign="middle" align="center">
          {(rowData) => (
            <IconButton
              icon={<Trash />}
              color="red"
              appearance="primary"
              size="lg"
              onClick={() =>
                setData(data.filter((item) => item.Player !== rowData.Player))
              }
            />
          )}
        </Cell>
      </Column>
    </Table>
  );
};

export default observer(BigTableActivity);
