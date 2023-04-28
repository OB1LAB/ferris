import React, { useState } from "react";
import classes from "./Parser.module.scss";
import { observer } from "mobx-react-lite";
import { AutoComplete, InputGroup } from "rsuite";
import Send from "@rsuite/icons/legacy/Send";
import ParserService from "../../services/ParserService";

const SendMessage = ({ msg, setMsg, macros }) => {
  const [helpWords, setHelpWords] = useState([]);
  const [sending, setSending] = useState(false);
  const send = async () => {
    if (msg !== "" && sending === false) {
      setSending(true);
      setMsg("");
      await ParserService.sendMsg(msg);
      setSending(false);
    }
  };
  const handleChange = (value) => {
    setMsg(value);
    let matches = [];
    if (value.lastIndexOf("<") > value.lastIndexOf(">")) {
      const inputMacros = value.split("<").pop();
      matches =
        inputMacros !== ""
          ? Object.keys(macros).filter((item) =>
              item.toLowerCase().includes(inputMacros.toLowerCase())
            )
          : [];
    }
    setHelpWords(
      matches
        .map((item) => `${value.split("<")[0]}${macros[item]}`)
        .splice(0, 3)
    );
  };
  return (
    <InputGroup size="lg" className={classes.sendMsg}>
      <AutoComplete
        data={helpWords}
        size="lg"
        value={msg}
        onChange={handleChange}
        placeholder="Отправить сообщение"
        filterBy={() => true}
        onKeyPress={(e) =>
          e.key === "Enter" && helpWords.length === 0 && send()
        }
      />
      <InputGroup.Button onClick={send}>
        <Send />
      </InputGroup.Button>
    </InputGroup>
  );
};

export default observer(SendMessage);
