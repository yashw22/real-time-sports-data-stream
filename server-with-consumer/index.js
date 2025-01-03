const express = require('express');
const { consumeMessages } = require('./services/consumer');
const latestMessageRoute = require('./routes/latestMessage');

const app = express();

app.use('/api', latestMessageRoute);

app.listen(5000, () => {
  console.log('Server running on http://localhost:5000');
  consumeMessages().catch(console.error);
});
