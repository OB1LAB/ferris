import React, { useState, useContext, useEffect } from "react";
import { observer } from "mobx-react-lite";
import { Button, Progress } from "rsuite";
import Pc from "@rsuite/icons/legacy/Pc";
import Commenting from "@rsuite/icons/legacy/Commenting";
import Search from "@rsuite/icons/legacy/Search";
import LogsService from "../services/LogsService";
import InfoService from "../services/InfoService";
import { Context } from "../main";

const Index = () => {
  const myVersion = "1.05";
  const { store } = useContext(Context);
  const [loading, setLoading] = useState(false);
  const [percent, setPercent] = useState(0);
  const status = percent === 100 ? "success" : null;
  const color = percent === 100 ? "#52c41a" : "#3385ff";
  const downloadLogs = async () => {
    setPercent(0);
    setLoading(true);
    await LogsService.downloadLogs(store.selected_server);
    setLoading(false);
    const info = await InfoService.get();
    store.setLastLogsUpdate(info.data.last_update)
  };
  const openLogsFolder = () => {
    LogsService.openLogsFolder();
  };
  useEffect(() => {
    if (store.socketIsConnected) {
      store.socket.on("percent", setPercent);
      return () => {
        store.socket.off("percent");
      };
    }
  }, [store.socketIsConnected]);
  useEffect(() => {
    if (!loading) {
      setPercent(0);
    }
  }, [store.selected_server]);
  return (
    <div className="infoPage">
      <div className="about">
        <br />
        Мои контакты: Дискорд
        {" ->"} OB1CHAM,{" "}
        <a href="https://t.me/OB1CHAM" target="_blank">
          Телеграмм
        </a>
        ,{" "}
        <a href="https://vk.com/OB1CHAM" target="_blank">
          Вк
        </a>
        .
        <br />
        Исходный код находится на{" "}
        <a href="https://github.com/OB1LAB/ferris" target="_blank">
          GitHub
        </a>
        .
        <br />
        Перед тем, как начать использовать этот проект, вам нужно загрузить
        логи. Публичные логи можно скачать, нажав на кнопку ниже. Если у вас уже
        есть загруженные логи, то последний лог будет перезаписан, таким образом
        никакая информация не будет потеряна. <br /> После запуска сервера, он
        автоматически создаст папку "logs" в своей директории, в которой будут
        находиться три сервера. <br />
        Каждый сервер будет иметь три дополнительные папки: "chat_public",
        "chat_private" и "drop_private".
        <br />
        Если вам нужно использовать приватные логи, переместите их в
        соответствующую папку (В случае использования файла "latest.log",
        переименуйте его в соответствии с датой и номером рестарта).
      </div>
      <div className="func">
        <div className="infoButtons">
          <Button appearance="primary" onClick={downloadLogs} loading={loading}>
            Скачать публичные логи
          </Button>
          <Button appearance="primary" onClick={openLogsFolder}>
            Открыть директорию с логами
          </Button>
        </div>
        <div className="progressBar">
          <Progress.Circle
            percent={percent}
            strokeColor={color}
            status={status}
          />
        </div>
      </div>
      <div className="activityPage">
        <Pc /> Игровая активность - страница для просмотра игровой статистики.
        Выберите справа сверху сервер и при необходимости дату. (Она
        автоматически ставится на текущую неделю)
        <br />
        Про AVG и Total:
        <div className="list">
          1.AVG - average (Средний). Это средний онлайн за выбранный период.{" "}
          <br />
          Верхняя строка - Средний онлайн с учётом ваниша.
          <br />
          Нижняя строка - Средний онлайн в ванише.
          <br />
          2. Total - Общий. Это общий онлайн за выбранный период.
          <br />
          Верхняя строка - Общий онлайн с учётом ваниша.
          <br />
          Нижняя строка - Общий онлайн в ванише.
          <br />
          Если навестись курсором (Тыкнуть с телефоном пальцем) в этой зоне, то
          высветится подсказка, в которой будет написан чистый онлайн. (Без
          ваниша)
        </div>
      </div>
      <div className="parserPage">
        <Commenting /> Парсер - страница для просмотра локальных логов в
        реальном времени и отправки сообщений. Для того чтобы отправлять
        сообщения, необходимо сделать:
        <div className="list">
          1. Зайти в игру.
          <br />
          2. Зажать левый shift и ` (ё), после откроется окно с биндами.
          <br />
          3. Нажать на правый alt.
          <br />
          4. Вписать {"$$<OB1LAB.txt>"}.
          <br />
          5. Сохранить.
          <br />
          6. Зажать одновременно F3 + P.(Активация режима, при котором майнкрафт
          не будет уходить в паузу, если окно с ним неактивно. Это необходимо
          для того, чтобы сигналы о нажатии на клавишу доходили в игру, именно
          для этого мы и делали бинд на клавишу)
          <br />
          7. Если нужно проскроллить в чат, то введите любое сообщение, но не
          отправляйте его. Когда в инпуте есть текст, чат не будет скроллится.
          <br />
          8. Не открывать в игре чат. (Чтобы срабатывал бинд)
        </div>
        Как это работает? При отправке сообщения, оно записывается в файл{" "}
        {"OB1LAB.txt"}. После нажимается левый alt, и срабатывает бинд, который
        отправляет содержимое файла в чат.
        <br />
        Также есть поддержка макросов и никнеймов, в виде всплывающей подсказки.
        <br />
        Чтобы использовать подсказку с макросом, введите символ {"<"}, после
        начните писать его название.
        <br />
        Чтобы использовать подсказку с никнеймом, начните писать ник игрока с
        большого регистра. Если он во время работы программы был в чате, то ник
        игрока появится в подсказках.
      </div>
      <div className="finderPage">
        <Search /> Поиск - страница для поиска информации в логах (Без учёта
        регистра). При помощи белого и чёрного списка можно создавать гибкие
        запросы. Работают они следующим образом:
        <div className="list">
          1. Белый список - каждая новая строка будет искаться в значение "ИЛИ".
          К примеру у нас есть в белом списке 2 строки "OB1CHAM" и "Ksena", на
          выходе мы получим все строки с "OB1CHAM" и "Ksena".
          <br />
          Для каждой строки можно задать свой список (при помощи разделения их
          запятой с пробелом ", "), который будет искаться в значении "И". К
          примеру у нас есть в белом списке 2 строки "OB1CHAM, [G], продам" и
          "Ksena, [L], куплю". На выходе мы получим строки с OB1CHAM, который в
          глобальном чате что-то продаёт, и с Ksena, которая что-то покупает в
          локальном чате.
          <br />
          2. Чёрный список - каждая новая строка будет искаться в значении
          "ИЛИ". К примеру у нас есть в чёрном списке "[G]", тогда мы на выходе
          не получим строки, содержащие глобальный чат. В отличии от белого
          списка, чёрный список не имеет поиска в значении "И", т.е тут не
          работают ", " из-за отсутствия необходимости в этом.
        </div>
        Для того, чтобы активировать поиск предметов по координатам, необходимо
        заполнить все поля (Первую точку, вторую точку/Точку и радиус).
      </div>
      <div>
        Текущая версия:{" "}
        <span
          style={{
            color: myVersion === store.actualVersion ? "#52c41a" : "red",
          }}
        >
          {myVersion}
        </span>
        {myVersion !== store.actualVersion && (
          <>
            {" "}
            (Скачать новую версию можно с{" "}
            <a href="https://github.com/OB1LAB/ferris" target="_blank">
              GitHub
            </a>
            )
          </>
        )}
        <br />
        Актуальная версия:{" "}
        <span style={{ color: "#52c41a" }}>{store.actualVersion}</span>
        <br />
        Время обновление логов на сервере: <span className="updateTime">{store.lastLogsUpdate}</span>
        <br />
        Планируемые обновления:
        <div className="list">
          1. Добавить вкладку настройки, в которой можно было бы включать
          уведомления (Как звуковые, так и справа внизу) в парсере, в том числе
          под каждый тип лога.
          <br />
          Как это будет примерно выглядеть - Тип лога и белый список. Если лог
          удовлетворяет условиям белого списка, то будет приходить уведомление
          <br />
          Отдельно будет пункт с нарушением 3.8. (Коммерция и реклама варпов)
          <br />
          2. Настраивать какие типы логи отображать.
        </div>
      </div>
    </div>
  );
};
export default observer(Index);
