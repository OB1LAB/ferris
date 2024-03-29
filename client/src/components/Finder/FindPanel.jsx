import { useState, useContext } from "react";
import { observer } from "mobx-react-lite";
import { DatePicker, Button, useToaster, Notification } from "rsuite";
import useWindowDimensions from "../useWindowDimensions";
import classes from "./Finder.module.scss";
import ModalFinder from "./ModalFinder";
import FinderService from "../../services/FinderService";
import { Context } from "../../main";
import { LocalFinder } from "./Finder.js";

function dateToString(date) {
  let daysSplit = date.toISOString().split("T")[0].split("-");
  return `${daysSplit[2]}-${daysSplit[1]}-${daysSplit[0]}`;
}

// eslint-disable-next-line react/prop-types
const FindPanel = ({ logs, setLogs, setLoading }) => {
  const { store } = useContext(Context);
  const toaster = useToaster();
  const [modal, setModal] = useState(false);
  const [date1, setDate1] = useState(new Date());
  const [date2, setDate2] = useState(new Date());
  const [localLogs, setLocalLogs] = useState([]);
  const { width } = useWindowDimensions();
  const [logsFilters, setLogsFilters] = useState({
    chatPublic: {
      whiteList: "",
      blackList: "",
    },
    chatPrivate: {
      whiteList: "",
      blackList: "",
    },
    dropPrivate: {
      type: "square",
      worlds: [],
      pos1: {
        x: null,
        z: null,
      },
      pos2: {
        x: null,
        z: null,
      },
      pos: {
        x: null,
        z: null,
      },
      radius: null,
      whiteList: "",
      blackList: "",
    },
    selectedTypeFind: "chatPublic",
  });
  const msgOk = (msg) => {
    toaster.push(
      <Notification type="success" header="Успешно" closable>
        {msg}
      </Notification>,
      { placement: "topEnd" },
    );
  };
  const findLogsGlobal = async () => {
    try {
      setLoading(true);
      setLocalLogs(logs);
      const response = await FinderService.globalFind(
        dateToString(date1),
        dateToString(date2),
        logsFilters,
        store.selected_server,
      );
      setLogs(
        response.data.map((line, index) => ({
          content: line,
          lid: index,
        })),
      );
      msgOk("Поиск закончен");
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className={width > 955 ? classes.findPanel : classes.findPanelMobile}>
      <DatePicker
        oneTap
        isoWeek
        cleanable={false}
        value={date1}
        onChange={setDate1}
        className={classes.date}
      />
      <DatePicker
        oneTap
        isoWeek
        cleanable={false}
        value={date2}
        onChange={setDate2}
        className={classes.date}
      />
      <Button appearance="primary" onClick={findLogsGlobal}>
        Поиск
      </Button>
      <Button
        appearance="primary"
        onClick={() => {
          setLocalLogs(logs);
          setLogs(
            // eslint-disable-next-line no-undef
            LocalFinder(
              logs.map((line) => line.content),
              logsFilters,
            ).map((line, index) => ({
              content: line,
              lid: index,
            })),
          );
          msgOk("Поиск закончен");
        }}
      >
        Локальный поиск
      </Button>
      <Button
        appearance="primary"
        onClick={() => {
          setLogs(localLogs);
          msgOk("Отменено");
        }}
      >
        Отменить
      </Button>
      <Button appearance="primary" onClick={() => setModal(true)}>
        Настроить фильтры
      </Button>
      <Button
        appearance="primary"
        onClick={() => {
          navigator.clipboard.readText().then((logsText) => {
            setLogs(
              logsText
                .split("\n")
                .toSorted()
                .map((line, index) => ({
                  content: line,
                  lid: index,
                })),
            );
            msgOk("Вставлено");
          });
        }}
      >
        Вставить
      </Button>
      <Button
        appearance="primary"
        onClick={() => {
          navigator.clipboard.writeText(
            // eslint-disable-next-line react/prop-types
            logs.map((line) => line.content.trim()).join("\n"),
          );
          msgOk("Скопировано в буфер обмена");
        }}
      >
        Скопировать
      </Button>
      <ModalFinder
        logsFiltersOriginal={logsFilters}
        setLogsFiltersOriginal={setLogsFilters}
        open={modal}
        setOpen={setModal}
      />
    </div>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export default observer(FindPanel);
