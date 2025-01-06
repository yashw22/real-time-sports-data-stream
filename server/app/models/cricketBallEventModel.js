const pool = require("../config/postgres");

const getCricketBallEventsByGameId = async (gameId) => {
  const query = `
    SELECT * 
    FROM cricket_ball_event 
    WHERE game_id = $1
    ORDER BY "over" DESC, ball DESC
  `;
  const values = [gameId];
  const result = await pool.query(query, values);
  return result.rows;
};

module.exports = { getCricketBallEventsByGameId };
