import React from "react";
import "./portfolio.css";

type Holding = {
  companyName: string;
  symbol: string;
  shares: number;
  avgPrice: number;
  currentPrice: number;
};

type User = {
  username: string;
  portfolio: Holding[];
};

type PortfolioProps = {
  user: User | null;
};

export function Portfolio({ user }: PortfolioProps) {
  if (!user) return <div className="portfolio-empty">You dont have any active trades</div>;

  return (
    <div className="portfolio-container">
      <h2 className="portfolio-title">Portfolio</h2>

      <table className="portfolio-table">
        <thead>
          <tr>
            <th>Company Name</th>
            <th>Symbol</th>
            <th>Shares</th>
            <th>Funds Invested</th>
            <th>Current Price</th>
            <th>Up/Down</th>
          </tr>
        </thead>

        <tbody>
          {user.portfolio.map((holding, index) => {
            const profit =
              (holding.currentPrice - holding.avgPrice) * holding.shares;

            return (
              <tr key={index}>
                <td>{holding.companyName}</td>
                <td>{holding.symbol}</td>
                <td>{holding.shares}</td>
                <td>${holding.avgPrice.toFixed(2)}</td>
                <td>${holding.currentPrice.toFixed(2)}</td>
                <td className={profit >= 0 ? "profit" : "loss"}>
                  ${profit.toFixed(2)}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}