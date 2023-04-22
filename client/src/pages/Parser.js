import React from "react";
import { observer } from "mobx-react-lite";
import ParserWindow from "../components/Parser/ParserWindow";

const Parser = () => {
  return (
    <div className="content">
      <ParserWindow />
    </div>
  );
};
export default observer(Parser);
