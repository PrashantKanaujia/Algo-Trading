import PositionsPanel from "../components/PositionsPanel";
import SignalsPanel from "../components/SignalsPanel"
import EquityChart from "../components/EquityChart"
import Trades from "../components/Trades1"
import StatsPanel from "../components/StatsPanel"
import BotControls from "../components/BotControls";
import "./Dashboard.css"
import "../variables.css"

function Dashboard() {
  return (
    <div className="container">
      <h1 style={{ textAlign: 'center' }}>Real-Time Crypto Algorithmic Trading System</h1>
      <div className="dashboard-row">
        <BotControls />
        <SignalsPanel />
    </div>
      <PositionsPanel />
      <EquityChart />
      <Trades />
      <StatsPanel/>
    </div>
  );
}

export default Dashboard;