import { useEffect, useState } from "react";
import { getSignal } from "../services/api";
import "./SignalsPanel.css";

function SignalsPanel() {
  const [signal, setSignal] = useState("NONE");
  const [time, setTime] = useState(null);

  const fetchSignal = async () => {
    try {
      const res = await getSignal();
      setSignal(res.data.signal || "NONE");
      setTime(res.data.timestamp);
    } catch (err) {
      console.error("Signal fetch error");
    }
  };

  useEffect(() => {
    fetchSignal();
    const interval = setInterval(fetchSignal, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="panel sig-panel-container">
      <h2>Current Signal</h2>
      
      <p className={`sig-value-text ${signal}`}>
        {signal}
      </p>

      {time && (
        <small className="sig-timestamp">
          Last Updated: {new Date(time * 1000).toLocaleString()}
        </small>
      )}
    </div>
  );
}

export default SignalsPanel;