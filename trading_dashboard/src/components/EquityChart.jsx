import { useEffect, useState } from "react";
import { getEquity } from "../services/api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";
import "./EquityCharts.css"

function EquityChart() {
  const [data, setData] = useState([]);

  const fetchEquity = async () => {
    try {
      const res = await getEquity();
      const cleaned = (res.data || []).filter(
        (d) => d && typeof d.equity === "number" && typeof d.time !== "undefined"
      );
      setData(cleaned);
    } catch (err) {
      console.error("Equity fetch error", err);
    }
  };

  useEffect(() => {
    fetchEquity();
    const interval = setInterval(fetchEquity, 5000);
    return () => clearInterval(interval);
  }, []);

  const values = data.map((d) => d.equity);
  const min = values.length ? Math.min(...values) : 0;
  const max = values.length ? Math.max(...values) : 1;

  const formatDate = (time) =>
    time ? new Date(time * 1000).toLocaleDateString("en-IN", { day: "2-digit", month: "short" }) : "";

  const formatDateTime = (time) =>
    time ? new Date(time * 1000).toLocaleString("en-IN", {
          day: "2-digit",
          month: "short",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit"
        }) : "";

  return (
    <div className="equity-chart-panel" style={{ position: 'relative', zIndex: 1 }}>
      <h2>Equity Curve</h2>

      {data.length === 0 ? (
        <p>No data yet</p>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data} style={{ pointerEvents: 'auto' }}>
            <CartesianGrid stroke="#444" strokeDasharray="3 3" />

            <XAxis
              dataKey="time"
              tickFormatter={formatDate}
            />

            <YAxis
              domain={[min - 0.5, max + 0.5]}
              tickFormatter={(val) => (typeof val === "number" ? val.toFixed(2) : val)}
              allowDataOverflow={true}
            />


            <Tooltip
              useTranslate3d={true}
              isAnimationActive={false}
              formatter={(value) => (typeof value === "number" ? value.toFixed(4) : value)}
              labelFormatter={formatDateTime}
              contentStyle={{ backgroundColor: "#1a1a2b", border: "1px solid #444" }}
            />

            <Line
              type="monotone"
              dataKey="equity"
              stroke="#00ff88"
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
              activeDot={{ r: 6, strokeWidth: 0 }} // Ensures the dot shows on hover
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

export default EquityChart;