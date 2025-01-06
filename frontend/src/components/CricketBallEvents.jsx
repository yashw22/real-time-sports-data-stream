/* eslint-disable react/prop-types */
import { useEffect, useState } from "react";
import { fetchBallEvents } from "../api";
import { CricketSingleBallEvent } from "./CricketSingleBallEvent";

export const CricketBallEvents = ({ gameId }) => {
  const [ballEvents, setBallEvents] = useState([]);

  useEffect(() => {
    const loadCricketBallEvent = async () => {
      const events_data = await fetchBallEvents(gameId);
      setBallEvents(events_data);
    };
    loadCricketBallEvent();
  }, [gameId]);

  return (
    <div className="mt-8">
      <h2 className="text-xl font-bold mb-4">Ball-by-Ball Events</h2>
      <ul>
        {ballEvents.map((event, index) => (
          <li key={index} className="p-2 bg-gray-100 mb-2 rounded-md">
            <CricketSingleBallEvent event={event} />
          </li>
        ))}
      </ul>
    </div>
  );
};
