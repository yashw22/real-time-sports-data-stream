const express = require("express");
const cors = require("cors");
const routes = require("./app/routes");

const app = express();
app.use(cors());
// app.use(cors({ origin: 'http://localhost:5173' }));

app.use(express.json()); 
app.use("/api", routes);

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
