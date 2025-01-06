const pool = require("../config/postgres");

const getCricketMatchByGameId = async (gameId) => {
  const query = "SELECT * FROM cricket_match WHERE game_id = $1";
  const values = [gameId];
  const result = await pool.query(query, values);
  return result.rows[0];
};

module.exports = { getCricketMatchByGameId };
