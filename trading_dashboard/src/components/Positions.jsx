import React from "react";

export default function Positions({ positions }) {
  return (
    <div>
      <h2>Current Positions</h2>
      {positions.length === 0 ? (
        <p>No open positions</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Side</th>
              <th>Quantity</th>
              <th>Entry Price</th>
            </tr>
          </thead>
          <tbody>
            {positions.map((p, idx) => (
              <tr key={idx}>
                <td>{p.symbol}</td>
                <td>{p.side}</td>
                <td>{p.quantity}</td>
                <td>{p.entry_price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}