const {
  getAllCricketMatches,
  getCricketMatchByGameId,
} = require("../models/cricketMatchModel");

const getCricketMatches = async (req, res) => {
  try {
    const cricketMatch = await getAllCricketMatches();
    res.status(200).json(cricketMatch);
  } catch (error) {
    console.error(error.message);
    res.status(500).json({ error: "Failed to fetch cricket match" });
  }
};

const getCricketMatch = async (req, res) => {
  const { game_id } = req.params;

  try {
    const cricketMatch = await getCricketMatchByGameId(game_id);

    if (!cricketMatch) {
      return res.status(404).json({ error: "Cricket match not found" });
    }
    res.status(200).json(cricketMatch);
  } catch (error) {
    console.error(error.message);
    res.status(500).json({ error: "Failed to fetch cricket match" });
  }
};

module.exports = { getCricketMatches, getCricketMatch };
