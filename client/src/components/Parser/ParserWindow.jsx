import React, { useEffect, useRef, useState } from "react";
import classes from "./Parser.module.scss";
import { observer } from "mobx-react-lite";
import SendMessage from "./SendMessage";
import Chat from "./Chat";
import ParserService from "../../services/ParserService";
import io from "socket.io-client";

const limitChat = 150;

const ParserWindow = () => {
  const chatRef = useRef();
  const [connected, setConnected] = useState(false);
  const [msg, setMsg] = useState("");
  const [messages, setMessages] = useState([]);
  const [macros, setMacros] = useState({});
  const [players, setPlayers] = useState([]);
  const scrollChatToBottom = () => {
    chatRef.current.scrollTop = chatRef.current.scrollHeight;
  };
  const getMacros = async () => {
    try {
      const response = await ParserService.getMacros();
      const data = response.data;
      setMacros(data.macros);
      setPlayers(data.players);
    } catch (err) {
      console.log(err);
    }
  };
  useEffect(() => {
    const socket = io(import.meta.env.VITE_APP_SERVER_URL);
    socket.on("connect", () => {
      setConnected(true);
    });
    socket.on("new_msg", (chatMsg) => {
      setMessages((prev) => [...prev, ...chatMsg].slice(-limitChat));
      setPlayers((prev) => [
        ...prev,
        ...chatMsg.map((value) => value.player).filter((value) => value !== ""),
      ]);
    });
    getMacros();
    if (socket) return () => socket.disconnect();
  }, []);
  useEffect(() => {
    if (connected && msg === "") {
      scrollChatToBottom();
    }
  }, [messages]);
  if (!connected) {
    return <div>Загрузка...</div>;
  }
  return (
    <div className={classes.parser}>
      <Chat messages={messages} chatRef={chatRef} />
      <SendMessage
        msg={msg}
        setMsg={setMsg}
        macros={macros}
        players={players}
      />
    </div>
  );
};

export default observer(ParserWindow);
