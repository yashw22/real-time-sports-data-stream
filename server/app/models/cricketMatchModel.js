const pool = require("../config/postgres");

const getAllCricketMatches = async () => {
  const query = "SELECT * FROM cricket_match";
  const result = await pool.query(query);
  return result.rows;
};

const getCricketMatchByGameId = async (gameId) => {
  const query = "SELECT * FROM cricket_match WHERE game_id = $1";
  const values = [gameId];
  const result = await pool.query(query, values);
  return result.rows[0];
};

module.exports = { getAllCricketMatches, getCricketMatchByGameId };
