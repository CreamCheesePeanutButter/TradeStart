import React, { useState, useEffect } from "react";

const Homepage = () => {
  const [stocks, setStocks] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    // Define the async function inside the effect
    const fetchStocks = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/stocks"); // Replace with your actual URL
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();

        // Accessing the "stocks" key from your jsonify object
        setStocks(data.stocks);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStocks();
  }, []);

  if (loading) return <div>Loading prices...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Market Watch</h2>
      <table>
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Current Price</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(stocks).map(([ticker, stock]) => (
            <tr key={ticker}>
              <td>{ticker}</td>
              <td>{stock.current_price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Homepage;
