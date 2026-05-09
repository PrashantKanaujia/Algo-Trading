import axios from "axios";

const api = axios.create({
  baseURL: "https://algo-trading-oq5l.onrender.com/"
  // baseURL: "http://localhost:8000"
});

export const getPositions = () => api.get("/positions");
export const getTrades = () => api.get("/trades");
export const getEquity = () => api.get("/equity");
export const getSignal = () => api.get("/signals");
export const getBotStatus = () => api.get("/bot-status");

export const getStats = () => api.get("/stats");

export const startBot = () => api.post("/start");
export const stopBot = () => api.post("/stop");
export const closePosition = () => api.post("/close-position");

export default api;