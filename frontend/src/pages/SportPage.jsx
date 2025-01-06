import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { firstCharCap } from "../utils/stringUtils";
import CricketMatchList from "../components/CricketMatchList";
import { fetchCricketMatches } from "../api";

const SportPage = () => {
  const { topic } = useParams();
  const [matches, setMatches] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const loadMatches = async () => {
      if (topic === "cricket") {
        const data = await fetchCricketMatches();
        setMatches(data);
      }
    };

    loadMatches();
  }, [topic]);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6 flex justify-center">
        {firstCharCap(topic)} Matches
      </h1>
      {topic === "cricket" && (
        <CricketMatchList
          matches={matches}
          onMatchClick={(gameId) => navigate(`/match/${topic}/${gameId}`)}
        />
      )}
    </div>
  );
};

export default SportPage;
