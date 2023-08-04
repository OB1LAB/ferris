import React, { useEffect, useRef, useState, useContext } from "react";
import { observer } from "mobx-react-lite";
import SendMessage from "../components/Parser/SendMessage";
import Chat from "../components/Parser/Chat";
import ParserService from "../services/ParserService";
import classes from "../components/Parser/Parser.module.scss";
import { Context } from "../main";

const limitChat = 150;

const Parser = () => {
  const chatRef = useRef();
  const [msg, setMsg] = useState("");
  const { store } = useContext(Context);
  const [messages, setMessages] = useState([]);
  const [macros, setMacros] = useState({});
  const [players, setPlayers] = useState([]);
  const scrollChatToBottom = () => {
    chatRef.current.scrollTop = chatRef.current.scrollHeight;
  };
  const getData = async () => {
    try {
      const response = await ParserService.getData();
      const data = response.data;
      setMacros(data.macros);
      setPlayers(data.players);
      setMessages(data.logs);
    } catch (err) {
      console.log(err);
    }
  };
  useEffect(() => {
    if (store.socketIsConnected) {
      store.socket.on("new_msg", (chatMsg) => {
        setMessages((prev) => [...prev, ...chatMsg].slice(-limitChat));
        setPlayers((prev) => [
          ...prev,
          ...chatMsg
            .map((value) => value.player)
            .filter((value) => value !== ""),
        ]);
      });
      getData();
      return () => {
        store.socket.off("new_msg");
      };
    }
  }, [store.socketIsConnected]);
  useEffect(() => {
    if (store.socketIsConnected && msg === "") {
      scrollChatToBottom();
    }
  }, [messages]);
  if (!store.socketIsConnected) {
    return <div>Загрузка...</div>;
  }
  return (
    <div className={`content ${classes.parser}`}>
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
export default observer(Parser);
