import React, { useEffect, useRef, useState } from "react";
import classes from "./Parser.module.scss";
import { observer } from "mobx-react-lite";
import SendMessage from "./SendMessage";
import Chat from "./Chat";
import ParserService from "../../services/ParserService";
const ParserWindow = () => {
  const chatRef = useRef();
  const [msg, setMsg] = useState("");
  const [messages, setMessages] = useState([]);
  const [offset, setOffset] = useState(0);
  const [macros, setMacros] = useState({});
  const scrollChatToBottom = () => {
    chatRef.current.scrollTop = chatRef.current.scrollHeight;
  };
  useEffect(() => {
    const getLogs = async () => {
      try {
        const response = await ParserService.getLogs(offset);
        const data = response.data;
        setMessages([...messages, ...data.messages].slice(-150));
        if (offset === 0) {
          setMacros(data.macros);
        }
        setOffset(data.offset);
        if (msg === "") {
          scrollChatToBottom();
        }
      } catch (err) {
        console.log(err);
      }
    };
    const interval = setInterval(() => {
      getLogs();
    }, 100);
    return () => clearInterval(interval);
    // eslint-disable-next-line
  }, [offset, msg, macros]);
  return (
    <div className={classes.parser}>
      <Chat messages={messages} chatRef={chatRef} />
      <SendMessage msg={msg} setMsg={setMsg} macros={macros} />
    </div>
  );
};

export default observer(ParserWindow);
