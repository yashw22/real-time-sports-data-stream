import axios from "axios";

// const API_BASE = import.meta.env.VITE_POSTGRES_API;
const API_BASE = "http://localhost:5000/api";

export const fetchLiveMatches = async () => {
  const { data } = await axios.get(`${API_BASE}/live-match`);
  return data;
};

export const fetchCricketMatches = async () => {
  const { data } = await axios.get(`${API_BASE}/cricket-match`);
  return data;
};

export const fetchCricketMatchById = async (gameId) => {
  const { data } = await axios.get(`${API_BASE}/cricket-match/${gameId}`);
  return data;
};

export const fetchCricketMatchState = async (gameId) => {
  const { data } = await axios.get(
    `${API_BASE}/cricket-match-state/${gameId}`
  );
  return data;
};

export const fetchBallEvents = async (gameId) => {
  const { data } = await axios.get(`${API_BASE}/cricket-ball-event/${gameId}`);
  return data;
};
