import React, { useState } from "react";
import { observer } from "mobx-react-lite";
import {
  Button,
  Input,
  Modal,
  InputPicker,
  InputNumber,
  CheckPicker,
  Radio,
  RadioGroup,
} from "rsuite";
import Pos from "./Pos";
import classes from "./Finder.module.scss";

const dataLogs = [
  {
    label: "Публичные логи чата",
    value: "chatPublic",
  },
  {
    label: "Приватные логи чата",
    value: "chatPrivate",
  },
  {
    label: "Приватные логи подбора",
    value: "dropPrivate",
  },
];

const dataWorlds = [
  {
    label: "Строительный",
    value: "world",
  },
  {
    label: "Копательный",
    value: "mining",
  },
  {
    label: "Ад",
    value: "DIM-1",
  },
  {
    label: "Энд",
    value: "DIM1",
  },
  {
    label: "Спавн",
    value: "spawn",
  },
  {
    label: "Тестовый",
    value: "test",
  },
];

const ModalFinder = ({
  open,
  setOpen,
  logsFiltersOriginal,
  setLogsFiltersOriginal,
}) => {
  const close = () => {
    setOpen(false);
    setLogsFilters(JSON.parse(JSON.stringify(logsFiltersOriginal)));
  };
  const [logsFilters, setLogsFilters] = useState(
    JSON.parse(JSON.stringify(logsFiltersOriginal))
  );
  return (
    <Modal
      onClose={close}
      keyboard={true}
      open={open}
      size="sm"
      overflow={false}
    >
      <Modal.Header closeButton={false}>
        <Modal.Title style={{ textAlign: "center" }}>Фильтры</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <InputPicker
          size="lg"
          placeholder="Large"
          data={dataLogs}
          value={logsFilters.selectedTypeFind}
          onChange={(logType) => {
            setLogsFilters({ ...logsFilters, selectedTypeFind: logType });
          }}
          className={classes.selector}
          cleanable={false}
          searchable={false}
        />
        {logsFilters.selectedTypeFind === "dropPrivate" ? (
          <div className={classes.content}>
            <div className={classes.underContent}>
              <div className={classes.pickupTypes}>
                <RadioGroup
                  name="radioList"
                  inline
                  value={logsFilters[logsFilters.selectedTypeFind].type}
                  onChange={(pickUpType) => {
                    setLogsFilters({
                      ...logsFilters,
                      [logsFilters.selectedTypeFind]: {
                        ...logsFilters[logsFilters.selectedTypeFind],
                        type: pickUpType,
                      },
                    });
                  }}
                  appearance="picker"
                  className={classes.radioSelector}
                >
                  <span className={classes.radioSelectorText}>
                    Тип поиска:{" "}
                  </span>
                  <Radio value="square">Площадь</Radio>
                  <Radio value="radius">Радиус</Radio>
                </RadioGroup>
                <CheckPicker
                  data={dataWorlds}
                  searchable={false}
                  placeholder="Выбрать миры"
                  value={logsFilters[logsFilters.selectedTypeFind].worlds || []}
                  onChange={(worlds) => {
                    setLogsFilters({
                      ...logsFilters,
                      [logsFilters.selectedTypeFind]: {
                        ...logsFilters[logsFilters.selectedTypeFind],
                        worlds: worlds,
                      },
                    });
                  }}
                  className={classes.selectWorlds}
                />
              </div>
              {logsFilters[logsFilters.selectedTypeFind].type === "square" ? (
                <div className={classes.coordinates}>
                  <Pos
                    logsFilters={logsFilters}
                    setLogsFilters={setLogsFilters}
                    posNumber={"first"}
                  />
                  <Pos
                    logsFilters={logsFilters}
                    setLogsFilters={setLogsFilters}
                    posNumber={"second"}
                  />
                </div>
              ) : (
                <div className={classes.coordinates}>
                  <Pos
                    logsFilters={logsFilters}
                    setLogsFilters={setLogsFilters}
                    posNumber={"other"}
                  />
                  <InputNumber
                    value={logsFilters.dropPrivate.radius}
                    onChange={(radius) => {
                      setLogsFilters({
                        ...logsFilters,
                        dropPrivate: {
                          ...logsFilters.dropPrivate,
                          radius,
                        },
                      });
                    }}
                    placeholder="Радиус"
                  />
                </div>
              )}
            </div>
            <div className={classes.filters}>
              <div>
                <h6>Чёрный список</h6>
                <Input
                  as="textarea"
                  className={classes.filter}
                  value={logsFilters[logsFilters.selectedTypeFind].blackList}
                  onChange={(data) => {
                    setLogsFilters({
                      ...logsFilters,
                      [logsFilters.selectedTypeFind]: {
                        ...logsFilters[logsFilters.selectedTypeFind],
                        blackList: data,
                      },
                    });
                  }}
                />
              </div>
              <div>
                <h6>Белый список</h6>
                <Input
                  as="textarea"
                  className={classes.filter}
                  value={logsFilters[logsFilters.selectedTypeFind].whiteList}
                  onChange={(data) => {
                    setLogsFilters({
                      ...logsFilters,
                      [logsFilters.selectedTypeFind]: {
                        ...logsFilters[logsFilters.selectedTypeFind],
                        whiteList: data,
                      },
                    });
                  }}
                />
              </div>
            </div>
          </div>
        ) : (
          <div className={classes.content}>
            <div className={classes.filters}>
              <div>
                <h6>Чёрный список</h6>
                <Input
                  as="textarea"
                  className={classes.filter}
                  value={logsFilters[logsFilters.selectedTypeFind].blackList}
                  onChange={(data) => {
                    setLogsFilters({
                      ...logsFilters,
                      [logsFilters.selectedTypeFind]: {
                        ...logsFilters[logsFilters.selectedTypeFind],
                        blackList: data,
                      },
                    });
                  }}
                />
              </div>
              <div>
                <h6>Белый список</h6>
                <Input
                  as="textarea"
                  className={classes.filter}
                  value={logsFilters[logsFilters.selectedTypeFind].whiteList}
                  onChange={(data) => {
                    setLogsFilters({
                      ...logsFilters,
                      [logsFilters.selectedTypeFind]: {
                        ...logsFilters[logsFilters.selectedTypeFind],
                        whiteList: data,
                      },
                    });
                  }}
                />
              </div>
            </div>
          </div>
        )}
      </Modal.Body>
      <Modal.Footer className={classes.modalFooter}>
        <div className={classes.buttons}>
          <Button color="red" appearance="primary" onClick={close}>
            Отмена
          </Button>
          <Button
            color="green"
            appearance="primary"
            onClick={() => {
              setLogsFiltersOriginal(JSON.parse(JSON.stringify(logsFilters)));
              setOpen(false);
            }}
            disabled={
              JSON.stringify(logsFilters) ===
              JSON.stringify(logsFiltersOriginal)
            }
          >
            Сохранить
          </Button>
        </div>
      </Modal.Footer>
    </Modal>
  );
};

export default observer(ModalFinder);
