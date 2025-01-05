const express = require('express');
const cors = require('cors');
const { consumeMessages } = require('./services/consumer');
const latestMessageRoute = require('./routes/latestMessage');

const app = express();
app.use(cors());
// app.use(cors({ origin: 'http://localhost:5173' }));

app.use('/api', latestMessageRoute);

app.listen(5000, () => {
  console.log('Server running on http://localhost:5000');
  consumeMessages().catch(console.error);
});
