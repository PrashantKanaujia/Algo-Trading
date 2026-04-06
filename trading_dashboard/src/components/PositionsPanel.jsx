import { useEffect, useState } from "react";
import { getPositions } from "../services/api";
import "./PositionsPanel.css";

function PositionsPanel() {
  const [positions, setPositions] = useState([]);

  const fetchPositions = async () => {
    try {
      const res = await getPositions();
      setPositions(res.data || []);
    } catch (err) {
      console.error("Error fetching positions", err);
    }
  };

  useEffect(() => {
    fetchPositions();
    const interval = setInterval(fetchPositions, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="pos-v2-panel">
      <h2>Open Positions</h2>

      {positions.length === 0 ? (
        <p className="pos-v2-empty-msg">No open positions</p>
      ) : (
        <table className="pos-v2-table">
          <thead className="pos-v2-thead">
            <tr>
              <th>Symbol</th>
              <th>Size</th>
            </tr>
          </thead>

          <tbody className="pos-v2-tbody">
            {positions.map((pos, index) => (
              <tr key={index}>
                <td>{pos.symbol}</td>
                <td>{pos.size}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default PositionsPanel;