/* eslint-disable react/prop-types */
export const CricketSingleBallEvent = ({ event }) => {
  const getBoxInfo = () => {
    const append = !("extras" in event.delivery)
      ? ""
      : "wides" in event.delivery.extras
      ? "w"
      : "noballs" in event.delivery.extras
      ? "nb"
      : "legbyes" in event.delivery.extras
      ? "lb"
      : "";
    const common =
      "mx-2 w-8 h-8 flex items-center rounded-md justify-center font-bold ";
    if ("wickets" in event.delivery)
      return <div className={common + "bg-red-500 text-white"}>W</div>;
    else if (event.delivery.runs.batter === 6)
      return (
        <div className={common + "bg-blue-500 text-white"}>
          {event.delivery.runs.total}
          {append}
        </div>
      );
    else if (event.delivery.runs.batter === 4)
      return (
        <div className={common + "bg-green-600 text-white"}>
          {event.delivery.runs.total}
          {append}
        </div>
      );
    else if (event.delivery.runs.total === 0)
      return (
        <div className={common + "bg-gray-300"}>
          <span className="w-1 h-1 bg-black rounded-full"></span>
        </div>
      );
    else
      return (
        <div className={common + "bg-gray-300"}>
          {event.delivery.runs.total}
          {append}
        </div>
      );
  };

  const getStringInfo = () => {
    var returnVal = event.delivery.bowler + " to " + event.delivery.batter;
    if ("wickets" in event.delivery) {
      returnVal +=
        ", " +
        event.delivery.wickets[0].player_out +
        " OUT (" +
        event.delivery.wickets[0].kind;
      if (["stumped", "caught"].includes(event.delivery.wickets[0].kind)) {
        returnVal += " by " + event.delivery.wickets[0].fielders[0].name;
      }
      returnVal += ")";
    } else if (event.delivery.runs.batter === 6) returnVal += ", SIX RUNS";
    else if (event.delivery.runs.batter === 4) returnVal += ", FOUR RUNS";
    else if (event.delivery.runs.total === 0) returnVal += ", no run";
    else {
      const runs = event.delivery.runs.total;

      returnVal += ", " + runs + (runs === 1 ? " run" : " runs");
    }

    if ("extras" in event.delivery) {
      const extra_runs = Object.values(event.delivery.extras)[0];
      returnVal +=
        ", (" +
        Object.keys(event.delivery.extras)[0] +
        ") " +
        extra_runs +
        (extra_runs === 1 ? " run" : " runs");
    }

    return returnVal;
  };

  return (
    <div className="flex flex-wrap row items-center">
      <div className="w-[4ch] text-center">
        {event.over}.{event.ball}
      </div>
      {getBoxInfo()}
      <div>{getStringInfo()}</div>
    </div>
  );
};
