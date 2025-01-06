const express = require("express");
const router = express.Router();

const { getLiveMatches } = require("../controllers/liveMatchController");
const { getCricketMatch } = require("../controllers/cricketMatchController");
const { getCricketBallEvents } = require("../controllers/cricketBallEventController");
const { getCricketMatchState } = require("../controllers/cricketMatchStateController");

router.get("/live-matches", getLiveMatches);
router.get("/cricket-match/:game_id", getCricketMatch);
router.get("/cricket-ball-events/:game_id", getCricketBallEvents);
router.get("/cricket-match-state/:game_id", getCricketMatchState);

module.exports = router;
