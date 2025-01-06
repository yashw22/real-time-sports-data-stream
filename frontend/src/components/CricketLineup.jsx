/* eslint-disable react/prop-types */
export const CricketLineup = ({ match }) => {
  return (
    <div className="mt-8">
      <h2 className="text-xl font-bold mb-4">Cricket Lineup</h2>
      <div className="flex row space-x-2">
        <div className="m-2">
          <h2 className="text-lg font-bold mb-4">{match.team_a}</h2>
          <ul>
            {match.players_a.map((player, index) => (
              <li key={index} className="p-2 bg-gray-100 mb-2 rounded-md">
                {player}
              </li>
            ))}
          </ul>
        </div>
        <div className="m-2">
          <h2 className="text-lg font-bold mb-4">{match.team_b}</h2>

          <ul>
            {match.players_b.map((player, index) => (
              <li key={index} className="p-2 bg-gray-100 mb-2 rounded-md">
                {player}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
