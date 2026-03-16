import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import "./stockhistory.css";

function StockHistoryPage() {
  const [ticker, setTicker] = useState("AAPL");
  const [range, setRange] = useState("1m");
  const [data, setData] = useState([]);

  const fetchHistory = async () => {
    const response = await fetch(
      `http://127.0.0.1:5000/stock-history?ticker=${ticker}&range=${range}`
    );

    const result = await response.json();

    if (result.history) {
      const formatted = result.history.map((item: any) => ({
        time: new Date(item.time * 1000).toLocaleDateString(),
        price: item.price
      }));

      setData(formatted);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [ticker, range]);

  return (
    <div className="history-page">
      <div className="bg-grid" />

      <div className="history-content">
        <h1 className="history-title">Stock Performance</h1>

        <div className="history-controls">
          <select value={ticker} onChange={(e) => setTicker(e.target.value)}>
            <option value="AAPL">AAPL</option>
            <option value="GOOGL">GOOGL</option>
            <option value="AMZN">AMZN</option>
          </select>

          <select value={range} onChange={(e) => setRange(e.target.value)}>
            <option value="1d">1D</option>
            <option value="1w">1W</option>
            <option value="1m">1M</option>
            <option value="1y">1Y</option>
          </select>
        </div>

        <div className="chart-box">
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={data}>
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="price" stroke="#52B043" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default StockHistoryPage;