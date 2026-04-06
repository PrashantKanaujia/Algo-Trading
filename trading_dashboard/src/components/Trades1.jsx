import { useEffect, useState } from "react";
import { getTrades } from "../services/api";
import "./Trades.css";

function Trades() {
  const [trades, setTrades] = useState([]);
  const [showAll, setShowAll] = useState(false);

  const fetchTrades = async () => {
    try {
      const res = await getTrades();
      setTrades(res.data || []); 
    } catch (err) {
      console.error("Trades fetch error");
    }
  };

  useEffect(() => {
    fetchTrades();
    const interval = setInterval(fetchTrades, 5000);
    return () => clearInterval(interval);
  }, []);

  const sortedTrades = [...trades].sort(
    (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
  );

  const displayedTrades = showAll ? sortedTrades : sortedTrades.slice(0, 5);

  return (
    <div className="panel trades-v2-container">
      <h2>Trades</h2>

      {trades.length === 0 ? (
        <p>No trades yet</p>
      ) : (
        <>
          <table className="trades-v2-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Symbol</th>
                <th>Side</th>
                <th>Qty</th>
                <th>Avg Price</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {displayedTrades.map((trade, index) => (
                <tr key={index}>
                  <td>{new Date(trade.timestamp).toLocaleString()}</td>
                  <td>{trade.symbol}</td>
                  <td className={trade.side === "BUY" ? "trades-v2-side-buy" : "trades-v2-side-sell"}>
                    {trade.side}
                  </td>
                  <td>{trade.quantity}</td>
                  <td>
                    {trade.avgPrice ? parseFloat(trade.avgPrice).toFixed(2) : "0.00"}
                  </td>
                  <td>
                    {trade.cumQuote ? parseFloat(trade.cumQuote).toFixed(3) : "0.00"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {trades.length > 5 && (
            <div className="trades-v2-footer">
              <button className="trades-v2-more-btn" onClick={() => setShowAll(!showAll)}>
                {showAll ? "Show Less" : `Show More (${trades.length - 5} more)`}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Trades;