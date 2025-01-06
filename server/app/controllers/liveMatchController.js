const { getAllLiveMatches } = require("../models/liveMatchModel");

const getLiveMatches = async (req, res) => {
  try {
    const liveMatches = await getAllLiveMatches();
    res.status(200).json(liveMatches);
  } catch (error) {
    console.error(error.message);
    res.status(500).json({ error: "Failed to fetch live matches" });
  }
};

module.exports = { getLiveMatches };
