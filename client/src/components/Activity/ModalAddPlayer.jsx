import React, { useState, useContext } from "react";
import classes from "./Activity.module.scss";
import { observer } from "mobx-react-lite";
import { Button, Input, Modal } from "rsuite";
import { Context } from "../../main";

const ModalAddPlayer = ({ open, setOpen, server }) => {
  const { store } = useContext(Context);
  const [nickName, setNickName] = useState("");
  const close = () => {
    setOpen(false);
  };
  const addPlayer = () => {
    let hasPlayer = false;
    store.staff[server].map((player) => {
      if (player.Player === nickName) {
        hasPlayer = true;
      }
    });
    if (!hasPlayer) {
      const staffList = [
        ...store.staff[server],
        { Player: nickName, Group: "player" },
      ];
      store.setStaff({ ...store.staff, [server]: staffList });
      setNickName("");
    }
    close();
  };
  return (
    <Modal
      onClose={close}
      keyboard={true}
      open={open}
      size="xs"
      overflow={false}
    >
      <Modal.Header closeButton={false}>
        <Modal.Title style={{ textAlign: "center" }}>
          Добавление игрока
        </Modal.Title>
      </Modal.Header>
      <Modal.Body className={classes.addPlayer}>
        <img
          className={classes.skin}
          alt=""
          src={`https://skins.mcskill.net/?name=${
            nickName.length > 2 ? nickName : "11"
          }&mode=7&fx=96&fy=192`}
        />
        <Input
          placeholder="Введите никнейм игрока"
          value={nickName}
          onChange={setNickName}
          className={classes.nickInput}
          onPressEnter={addPlayer}
        />
      </Modal.Body>
      <Modal.Footer className={classes.modalFooter}>
        <Button color="red" appearance="primary" onClick={close}>
          Отмена
        </Button>
        <Button color="green" appearance="primary" onClick={addPlayer}>
          Добавить
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default observer(ModalAddPlayer);
