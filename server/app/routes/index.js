const express = require("express");
const router = express.Router();

const { getLiveMatches } = require("../controllers/liveMatchController");
const {
  getCricketMatches,
  getCricketMatch,
} = require("../controllers/cricketMatchController");
const {
  getCricketBallEvents,
} = require("../controllers/cricketBallEventController");
const {
  getCricketMatchState,
} = require("../controllers/cricketMatchStateController");

router.get("/live-match", getLiveMatches);
router.get("/cricket-match", getCricketMatches);
router.get("/cricket-match/:game_id", getCricketMatch);
router.get("/cricket-ball-event/:game_id", getCricketBallEvents);
router.get("/cricket-match-state/:game_id", getCricketMatchState);

module.exports = router;
