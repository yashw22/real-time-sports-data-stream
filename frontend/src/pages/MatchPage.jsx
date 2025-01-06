import { useParams } from "react-router-dom";

import CricketMatchPage from "./CricketMatchPage";

const MatchPage = () => {
  const { topic, gameId } = useParams();
  if (topic === "cricket") {
    return <CricketMatchPage gameId={gameId} />;
  }
};

export default MatchPage;
