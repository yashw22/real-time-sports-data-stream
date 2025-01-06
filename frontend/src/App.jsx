import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import SportPage from "./pages/SportPage";
import MatchPage from "./pages/MatchPage";

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/sport/:topic" element={<SportPage />} />
      <Route path="/match/:topic/:gameId" element={<MatchPage />} />
    </Routes>
  </Router>
);

export default App;
