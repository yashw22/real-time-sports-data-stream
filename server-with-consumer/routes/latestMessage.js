const express = require('express');
const { getLatestMessage } = require('../services/consumer');

const router = express.Router();

router.get('/latest', async (req, res) => {
  try {
    const message = await getLatestMessage();
    res.json(message);
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch latest message' });
  }
});

module.exports = router;
