import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [latestMessage, setLatestMessage] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/latest");
        setLatestMessage(response.data);
      } catch (error) {
        console.error("Error fetching latest message:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-gray-100 min-h-screen p-6">
      <div className="max-w-3xl mx-auto bg-white shadow-md rounded-md p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">
          Latest Game Data
        </h1>
        {latestMessage ? (
          <div className="space-y-4">
            <div>
              <p className="font-semibold text-gray-700">
                <span className="text-blue-600">Game ID:</span>{" "}
                {latestMessage.game_id}
              </p>
            </div>
            <div>
              <p className="font-semibold text-gray-700">
                <span className="text-blue-600">Inning:</span>{" "}
                {latestMessage.inning}
              </p>
            </div>
            <div>
              <p className="font-semibold text-gray-700">
                <span className="text-blue-600">Team:</span>{" "}
                {latestMessage.team}
              </p>
            </div>
            <div>
              <p className="font-semibold text-gray-700">
                <span className="text-blue-600">Over:</span>{" "}
                {latestMessage.over}
              </p>
              <p className="font-semibold text-gray-700">
                <span className="text-blue-600">Ball:</span>{" "}
                {latestMessage.ball}
              </p>
            </div>
            <div>
              <h3 className="font-bold text-lg text-gray-800 mb-2">
                Delivery Details:
              </h3>
              <div className="ml-4">
                {latestMessage.delivery ? (
                  <>
                    <p className="text-gray-700">
                      <span className="font-semibold text-blue-600">
                        Batter:
                      </span>{" "}
                      {latestMessage.delivery.batter}
                    </p>
                    <p className="text-gray-700">
                      <span className="font-semibold text-blue-600">
                        Bowler:
                      </span>{" "}
                      {latestMessage.delivery.bowler}
                    </p>
                    <p className="text-gray-700">
                      <span className="font-semibold text-blue-600">
                        Non-Striker:
                      </span>{" "}
                      {latestMessage.delivery.non_striker}
                    </p>
                    <p className="text-gray-700">
                      <span className="font-semibold text-blue-600">Runs:</span>
                    </p>
                    <ul className="list-disc ml-6 text-gray-700">
                      <li>
                        <span className="font-semibold">Batter:</span>{" "}
                        {latestMessage.delivery.runs.batter}
                      </li>
                      <li>
                        <span className="font-semibold">Extras:</span>{" "}
                        {latestMessage.delivery.runs.extras}
                      </li>
                      <li>
                        <span className="font-semibold">Total:</span>{" "}
                        {latestMessage.delivery.runs.total}
                      </li>
                    </ul>
                    {/* Check for wickets if present */}
                    {latestMessage.delivery.wickets &&
                      latestMessage.delivery.wickets.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-gray-700 mt-4">
                            Wickets:
                          </h4>
                          {latestMessage.delivery.wickets.map(
                            (wicket, index) => (
                              <div key={index} className="ml-6 text-gray-700">
                                <p>
                                  <span className="font-semibold text-blue-600">
                                    Player Out:
                                  </span>{" "}
                                  {wicket.player_out}
                                </p>
                                <p>
                                  <span className="font-semibold text-blue-600">
                                    Fielders:
                                  </span>{" "}
                                  {wicket.fielders.map((f, idx) => (
                                    <span key={idx}>{f.name}</span>
                                  ))}
                                </p>
                                <p>
                                  <span className="font-semibold text-blue-600">
                                    Kind:
                                  </span>{" "}
                                  {wicket.kind}
                                </p>
                              </div>
                            )
                          )}
                        </div>
                      )}
                    {/* Check for extras field if present */}
                    {latestMessage.delivery.extras && (
                      <div className="mt-4">
                        <h4 className="font-semibold text-gray-700">Extras:</h4>
                        {Object.entries(latestMessage.delivery.extras).map(
                          ([key, value], index) => (
                            <p key={index} className="text-gray-700">
                              <span className="font-semibold text-blue-600">
                                {key}:
                              </span>{" "}
                              {value}
                            </p>
                          )
                        )}
                      </div>
                    )}
                  </>
                ) : (
                  <p className="text-gray-600">No delivery details available</p>
                )}
              </div>
            </div>
            <div>
              <p className="font-semibold text-gray-700">
                <span className="text-blue-600">Timestamp:</span>{" "}
                {latestMessage.timestamp}
              </p>
            </div>
          </div>
        ) : (
          <p className="text-gray-600">Loading...</p>
        )}
      </div>
    </div>
  );
}

export default App;
