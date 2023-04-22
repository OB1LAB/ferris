import React, { useState } from "react";
import classes from "./Parser.module.scss";
import { observer } from "mobx-react-lite";

const ParserWindow = ({ messages, chatRef }) => {
  return (
    <div className={classes.chat} ref={chatRef}>
      {messages.map((value) => {
        return (
          <div className={classes.msg} key={value.lid}>
            {value.content}
          </div>
        );
      })}
    </div>
  );
};

export default observer(ParserWindow);
