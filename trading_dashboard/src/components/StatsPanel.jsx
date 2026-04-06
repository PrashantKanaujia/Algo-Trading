import { useEffect, useState } from "react";
import { getStats } from "../services/api";
import "./StatsPanel.css";

function StatsPanel() {
  const [stats, setStats] = useState({
    total_trades: 0,
    win_rate: 0,
    total_pnl: 0
  });

  const fetchStats = async () => {
    try {
      const res = await getStats();
      setStats(res.data);
    } catch {
      console.error("Stats fetch error");
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="db-stats-panel">
      <div className="db-stat-card">
        <h3>Total Trades</h3>
        <p>{stats.total_trades}</p>
      </div>

      <div className={`db-stat-card ${stats.win_rate >= 50 ? "db-stat-positive" : "db-stat-negative"}`}>
        <h3>Win Rate</h3>
        <p>{(stats.win_rate).toFixed(3)}%</p>
      </div>

      <div className={`db-stat-card ${stats.total_pnl >= 0 ? "db-stat-positive" : "db-stat-negative"}`}>
        <h3>Total PnL</h3>
        <p>
          {stats.total_pnl >= 0 ? `+${(stats.total_pnl).toFixed(4)}` : (stats.total_pnl).toFixed(4)}
        </p>
      </div>
    </div>
  );
}

export default StatsPanel;