import React, { useState } from "react";
import { Loader } from "rsuite";
import { observer } from "mobx-react-lite";
import FindPanel from "../components/Finder/FindPanel";
import classes from "../components/Finder/Finder.module.scss";
import OutputLogs from "../components/Finder/OutputLogs";

const Finder = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  return (
    <div className={`content ${classes.finder}`}>
      <FindPanel
        logs={logs}
        setLogs={setLogs}
        loading={loading}
        setLoading={setLoading}
      />
      <OutputLogs logs={logs} loading={loading} />
      {loading && <Loader size="sm" center content="Загрузка..." />}
    </div>
  );
};
export default observer(Finder);
