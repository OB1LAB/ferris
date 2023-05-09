import React, { useState } from "react";
import classes from "./Parser.module.scss";
import { observer } from "mobx-react-lite";
import { AutoComplete, InputGroup } from "rsuite";
import Send from "@rsuite/icons/legacy/Send";
import ParserService from "../../services/ParserService";

function startsWithCapital(str) {
  const firstChar = str.charAt(0);
  return firstChar === firstChar.toUpperCase();
}

function removeLastWord(str) {
  const words = str.split(" ");
  if (words.length === 1) {
    return [str.charAt(0) === "!" ? "!" : "", str.substring(1)];
  }
  const word = words.pop();
  return [words.join(" "), word];
}

const SendMessage = ({ msg, setMsg, macros, players }) => {
  const [helpWords, setHelpWords] = useState([]);
  const [sending, setSending] = useState(false);
  const send = async () => {
    if (msg !== "" && !sending) {
      setSending(true);
      setMsg("");
      await ParserService.sendMsg(msg);
      setSending(false);
    }
  };
  const handleChange = (value) => {
    setMsg(value);
    const currentMacros = value.split("<").pop();
    const [currentPlayerLine, currentPlayer] = removeLastWord(value);
    if (value.lastIndexOf("<") > value.lastIndexOf(">")) {
      const matches =
        currentMacros !== ""
          ? Object.keys(macros).filter((item) =>
              item.toLowerCase().includes(currentMacros.toLowerCase())
            )
          : [];
      setHelpWords(
        matches
          .map((item) => `${value.split("<")[0]}${macros[item]}`)
          .slice(0, 3)
      );
    } else if (startsWithCapital(currentPlayer) && currentPlayer.length > 0) {
      const matches = players.filter((item) =>
        item.toLowerCase().includes(currentPlayer.toLowerCase())
      );
      setHelpWords(
        matches
          .map(
            (item) =>
              `${currentPlayerLine}${
                currentPlayerLine.length > 0 && currentPlayerLine !== "!"
                  ? " "
                  : ""
              }${item}`
          )
          .slice(0, 3)
      );
    } else {
      setHelpWords([]);
    }
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
