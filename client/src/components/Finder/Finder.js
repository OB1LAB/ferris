export const LocalFinder = (logs, logsFilters) => {
  let whiteList = logsFilters[logsFilters.selectedTypeFind].whiteList
    .toLowerCase()
    .replace(", ", ",")
    .split("\n");
  let blackList = logsFilters[logsFilters.selectedTypeFind].blackList
    .toLowerCase()
    .replace(", ", ",")
    .split("\n");
  const isWhiteList =
    whiteList.length > 0 && !(whiteList.length === 1 && whiteList[0] === "");
  const isBlackList =
    blackList.length > 0 && !(blackList.length === 1 && blackList[0] === "");
  let x1, x2, z1, z2, x_r, z_r, r;
  const isSquare =
    logsFilters["dropPrivate"]["type"] === "square" &&
    logsFilters["dropPrivate"]["pos1"]["x"] &&
    logsFilters["dropPrivate"]["pos2"]["x"] &&
    logsFilters["dropPrivate"]["pos1"]["z"] &&
    logsFilters["dropPrivate"]["pos2"]["z"] &&
    true;
  const isRadius =
    logsFilters["dropPrivate"]["type"] === "radius" &&
    logsFilters["dropPrivate"]["pos"]["x"] &&
    logsFilters["dropPrivate"]["pos"]["z"] &&
    logsFilters["dropPrivate"]["radius"] &&
    true;
  if (isSquare) {
    x1 = parseInt(logsFilters["dropPrivate"]["pos1"]["x"]);
    x2 = parseInt(logsFilters["dropPrivate"]["pos2"]["x"]);
    z1 = parseInt(logsFilters["dropPrivate"]["pos1"]["z"]);
    z2 = parseInt(logsFilters["dropPrivate"]["pos2"]["z"]);
  }
  if (isRadius) {
    x_r = parseInt(logsFilters["dropPrivate"]["pos"]["x"]);
    z_r = parseInt(logsFilters["dropPrivate"]["pos"]["z"]);
    r = parseInt(logsFilters["dropPrivate"]["radius"]);
  }
  return logs.filter((line) => {
    if (isBlackList) {
      for (const blackLine of blackList) {
        let isBlack = true;
        for (const blackWord of blackLine.split(",")) {
          if (!line.toLowerCase().includes(blackWord)) {
            isBlack = false;
            break;
          }
        }
        if (isBlack) {
          return false;
        }
      }
    }
    if (isWhiteList) {
      let isWhite = false;
      for (const whiteLine of whiteList) {
        let isWhiteLine = true;
        for (const whiteWord of whiteLine.split(",")) {
          if (!line.toLowerCase().includes(whiteWord)) {
            isWhiteLine = false;
            break;
          }
        }
        if (isWhiteLine) {
          isWhite = true;
          break;
        }
      }
      if (!isWhite) {
        return false;
      }
    }
    if (logsFilters.selectedTypeFind === "dropPrivate") {
      const world = line.split("Мир: ")[1].split(" ")[0];
      const x = parseInt(line.split("x=")[1].split(",")[0]);
      const z = parseInt(line.split("z=")[1].split("]")[0]);
      if (
        logsFilters["dropPrivate"]["worlds"].length &&
        !logsFilters["dropPrivate"]["worlds"].includes(world)
      ) {
        return false;
      }
      if (isSquare && !(x1 <= x && x <= x2 && z1 <= z && z <= z2)) {
        return false;
      }
      if (
        isRadius &&
        !(x_r - r <= x && x <= x_r + r && z_r - r <= z && z <= z_r + r)
      ) {
        return false;
      }
    }
    return true;
  });
};
