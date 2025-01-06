const { getCricketMatchStateByGameId } = require("../models/cricketMatchStateModel");

const getCricketMatchState = async (req, res) => {
  const { game_id } = req.params;

  try {
    const matchState = await getCricketMatchStateByGameId(game_id);

    if (!matchState) {
      return res.status(404).json({ error: "Cricket match state not found" });
    }
    res.status(200).json(matchState);
  } catch (error) {
    console.error(error.message);
    res.status(500).json({ error: "Failed to fetch cricket match state" });
  }
};

module.exports = { getCricketMatchState };

