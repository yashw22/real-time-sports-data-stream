/* eslint-disable react/prop-types */
import { formatTime } from "../utils/dateUtils";

const CricketMatchList = ({ matches, onMatchClick }) => (
  <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
    {matches.map((match) => (
      <div
        key={match.game_id}
        className="p-4 bg-gray-200 rounded-lg shadow-md cursor-pointer"
        onClick={() => onMatchClick(match.game_id)}
      >
        <p>
          <span className="font-bold">Start time:</span>&nbsp;{" "}
          {formatTime(match.starts_at)}
        </p>
        <h3 className="text-lg font-bold">{match.match_name}</h3>
        <h3 className="text-md font-bold">
          {match.team_a} V.S. {match.team_b}
        </h3>

        <br />
        <p>
          <span className="font-bold">Date:</span>&nbsp;&nbsp;&nbsp;{" "}
          {match.match_date}
        </p>
        <p>
          <span className="font-bold">City:</span>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {match.match_city}
        </p>
        <p>
          <span className="font-bold">Venue:</span>&nbsp; {match.match_venue}
        </p>
      </div>
    ))}
  </div>
);

export default CricketMatchList;
