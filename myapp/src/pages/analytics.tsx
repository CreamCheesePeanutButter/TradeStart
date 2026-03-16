import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";

import "./analytics.css";

function AnalyticsPage() {
  const [stocks, setStocks] = useState<any[]>([]);

  const COLORS = ["#52B043", "#107C10", "#0f5e0f", "#74d866"];

  const fetchStocks = async () => {
    const response = await fetch("http://127.0.0.1:5000/stocks");
    const data = await response.json();

    const formatted = Object.entries(data.stocks).map(([ticker, info]: any) => ({
      ticker,
      price: info.current_price,
      high: info.high_today,
      low: info.low_today,
      open: info.open_price
    }));

    setStocks(formatted);
  };

  useEffect(() => {
    fetchStocks();
  }, []);

  return (
    <div className="analytics-page">
      <div className="bg-grid" />

      <div className="analytics-content">
        <h1 className="analytics-title">Market Analytics</h1>

        <div className="chart-grid">

          {/* STOCK PRICE LINE GRAPH */}
          <div className="chart-card">
            <h2>Stock Prices</h2>

            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={stocks}>
                <XAxis dataKey="ticker" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="price"
                  stroke="#52B043"
                  strokeWidth={3}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* MARKET DISTRIBUTION PIE */}
          <div className="chart-card">
            <h2>Market Distribution</h2>

            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={stocks}
                  dataKey="price"
                  nameKey="ticker"
                  outerRadius={100}
                  label
                >
                  {stocks.map((entry, index) => (
                    <Cell
                      key={index}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>

        </div>
      </div>
    </div>
  );
}

export default AnalyticsPage;