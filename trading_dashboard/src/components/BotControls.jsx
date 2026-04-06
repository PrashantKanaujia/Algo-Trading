import { startBot, stopBot, closePosition, getBotStatus } from "../services/api";
import { useEffect, useState } from "react";
import "./BotControl.css";

function BotControls() {
  const [status, setStatus] = useState("stopped");

  const fetchStatus = async () => {
    try {
      const res = await getBotStatus();
      setStatus(res.data.status);
    } catch {
      console.error("status error");
    }
  };

  const handleStart = async () => {
    await startBot();
    fetchStatus();
  };

  const handleStop = async () => {
    await stopBot();
    fetchStatus();
  };

  const handleClose = async () => {
    if (window.confirm("Are you sure you want to close all positions?")) {
      await closePosition();
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000); // Keep status updated
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="panel bot-ctrl-panel">
      <h2>Bot Controls</h2>

      <p className="bot-ctrl-status">
        Status: <span className={`status-${status}`}>{status}</span>
      </p>

      <div className="bot-ctrl-actions">
        <button 
          className="bot-ctrl-btn bot-ctrl-btn-start" 
          onClick={handleStart}
        >
          Start Bot
        </button>

        <button 
          className="bot-ctrl-btn bot-ctrl-btn-stop" 
          onClick={handleStop}
        >
          Stop Bot
        </button>

        <button 
          className="bot-ctrl-btn bot-ctrl-btn-close" 
          onClick={handleClose}
        >
          Close Position
        </button>
      </div>
    </div>
  );
}

export default BotControls;