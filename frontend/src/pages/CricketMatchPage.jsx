import { useEffect, useState } from "react";
import FillBar from "../components/FillBar";
import { fetchCricketMatchById, fetchCricketMatchState } from "../api";
import { CricketBallEvents } from "../components/CricketBallEvents";
import { CricketLineup } from "../components/CricketLineup";

const refreshTimeInSecs = 20;

// eslint-disable-next-line react/prop-types
const CricketMatchPage = ({ gameId }) => {
  const [match, setMatch] = useState(null);
  const [matchState, setMatchState] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const [visibleElement, setVisibleElement] = useState("");

  useEffect(() => {
    const loadCricketMatch = async () => {
      const match_data = await fetchCricketMatchById(gameId);
      setMatch(match_data);
    };

    const loadCricketMatchState = async () => {
      const state_data = await fetchCricketMatchState(gameId);
      setMatchState(state_data);
      setRefreshKey((prev) => (prev + 1) % 10);
    };

    loadCricketMatch();
    loadCricketMatchState();

    const intervalId = setInterval(
      loadCricketMatchState,
      refreshTimeInSecs * 1000
    );

    return () => clearInterval(intervalId);
  }, [gameId]);

  return (
    <div className="p-8">
      {matchState && getMatchStateCard(match, matchState, refreshKey)}
      {matchState && (
        <div className="space-x-4 mt-4">
          <button
            onClick={() => {
              setVisibleElement((prev) => {
                if (prev === "lineup") return "";
                else return "lineup";
              });
            }}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md"
          >
            {visibleElement === "lineup" ? "Hide " : "Show "}Lineup
          </button>
          <button
            onClick={() => {
              setVisibleElement((prev) => {
                if (prev === "details") return "";
                else return "details";
              });
            }}
            className=" px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md"
          >
            {visibleElement === "details" ? "Hide " : "Show "}Details
          </button>
        </div>
      )}

      {visibleElement == "details" && (
        <CricketBallEvents gameId={gameId} key={refreshKey} />
      )}
      {visibleElement == "lineup" && <CricketLineup match={match} />}
    </div>
  );
};

const getMatchStateCard = (match, matchState, refreshKey) => {
  const { team, total_runs, overs_bowled, wickets, current_run_rate } =
    matchState;
  const { match_name, team_a, team_b } = match;

  const getScore = () => (
    <span>
      ({overs_bowled}) {total_runs}/{wickets}
    </span>
  );

  return (
    <div className="max-w-96">
      <FillBar key={refreshKey} duration={refreshTimeInSecs} />
      <div className="p-6 bg-white shadow-lg rounded-md">
        <h2 className="text-2xl font-bold mb-4">
          {match_name} <span className="text-red-600 text-sm">Live</span>
        </h2>
        <div
          className={`w-full flex justify-between font-bold ${
            team_a !== team && "text-black/50"
          }`}
        >
          <span className="text-lg">{team_a}</span>
          <span>{team_a === team && getScore(matchState)}</span>
        </div>
        <div
          className={`w-full flex justify-between font-bold ${
            team_b !== team && "text-black/50"
          }`}
        >
          <span className="text-lg font-bold">{team_b}</span>
          {team_b === team && getScore(matchState)}
        </div>
        <div className="mt-2 text-sm flex justify-end">
          CRR: {current_run_rate}
        </div>
      </div>
    </div>
  );
};

export default CricketMatchPage;
