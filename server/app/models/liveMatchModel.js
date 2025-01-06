const pool = require("../config/postgres");

const getAllLiveMatches = async () => {
  const query = "SELECT * FROM live_match";
  const result = await pool.query(query);
  return result.rows;
};

module.exports = { getAllLiveMatches };
