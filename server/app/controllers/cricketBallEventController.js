const { getCricketBallEventsByGameId } = require("../models/cricketBallEventModel");

const getCricketBallEvents = async (req, res) => {
  const { game_id } = req.params;

  try {
    const ballEvents = await getCricketBallEventsByGameId(game_id);

    if (!ballEvents || ballEvents.length === 0) {
      return res.status(404).json({ error: "No cricket ball events found for the given game ID" });
    }

    res.status(200).json(ballEvents);
  } catch (error) {
    console.error(error.message);
    res.status(500).json({ error: "Failed to fetch cricket ball events" });
  }
};

module.exports = { getCricketBallEvents };
