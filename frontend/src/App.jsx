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
    <div className="App">
      <h1>Latest Game Data</h1>
      {latestMessage ? (
        <div>
          <p>
            <strong>Game ID:</strong> {latestMessage.game_id}
          </p>
          <p>
            <strong>Count:</strong> {latestMessage.count}
          </p>
          <p>
            <strong>Timestamp:</strong> {latestMessage.timestamp}
          </p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;
