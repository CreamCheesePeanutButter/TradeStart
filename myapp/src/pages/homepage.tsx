import { useEffect, useState } from "react";
import "./homepage.css";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:5000";

const fmt = (val: number | undefined) =>
  val != null ? `$${val.toFixed(2)}` : "—";

const Homepage = () => {
  const [stocks, setStocks] = useState<
    Record<
      string,
      {
        current_price: number;
        open_price: number;
        high_today: number;
        low_today: number;
        previous_close: number;
      }
    >
  >({});
  const [currency, setCurrency] = useState("USD");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exchanging, setExchanging] = useState(false);

  const handleExchange = () => {
    if (exchanging) return;
    setExchanging(true);
    fetch(`${API_URL}/stocks/exchange`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        setCurrency(data.currency);
        return fetch(`${API_URL}/stocks`);
      })
      .then((res) => res.json())
      .then((data) => setStocks(data.stocks))
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Unknown error"),
      )
      .finally(() => setExchanging(false));
  };

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const response = await fetch(`${API_URL}/stocks`);
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
        setStocks(data.stocks);
        setCurrency(data.currency);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    };
    fetchStocks();
    const interval = setInterval(fetchStocks, 60_000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="hw-state">Loading prices...</div>;
  if (error) return <div className="hw-state hw-error">Error: {error}</div>;

  return (
    <div className="hw-page">
      <div className="bg-grid" />
      <div className="hw-content">
        <h2 className="hw-title">Market</h2>
        <div className="hw-table-wrap">
          <div className="hw-currency-bar">
            <span className="hw-currency-label">Currency</span>
            <div
              className={`hw-currency-toggle${exchanging ? " hw-toggle-busy" : ""}`}
            >
              <button
                className={`hw-toggle-opt${currency === "USD" ? " hw-toggle-active" : ""}`}
                onClick={() => currency !== "USD" && handleExchange()}
                disabled={exchanging}
              >
                USD
              </button>
              <button
                className={`hw-toggle-opt${currency === "CAD" ? " hw-toggle-active" : ""}`}
                onClick={() => currency !== "CAD" && handleExchange()}
                disabled={exchanging}
              >
                CAD
              </button>
            </div>
          </div>
          <table className="hw-table">
            <thead>
              <tr>
                <th>Ticker</th>
                <th>Current Price</th>
                <th>Open</th>
                <th>High</th>
                <th>Low</th>
                <th>Prev Close</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(stocks).map(([ticker, stock]) => (
                <tr key={ticker}>
                  <td className="hw-ticker">{ticker}</td>
                  <td className="hw-price">{fmt(stock.current_price)}</td>
                  <td>{fmt(stock.open_price)}</td>
                  <td className="hw-high">{fmt(stock.high_today)}</td>
                  <td className="hw-low">{fmt(stock.low_today)}</td>
                  <td>{fmt(stock.previous_close)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Homepage;
