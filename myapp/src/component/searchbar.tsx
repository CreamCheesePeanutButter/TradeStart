import React, { useState, useEffect, useRef } from "react";
import "./searchbar.css";
import { useAuth } from "../context/AuthContext";
import { useRefresh } from "../context/RefreshContext";
import { LineChart } from "@mui/x-charts/LineChart";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:5000";

// Shape of one stock entry returned by GET /stocks
interface StockData {
  stock_key: string;
  name: string;
  current_price: number;
  high_today: number;
  low_today: number;
  open_price: number;
  previous_close: number;
}

const fmt = (val: number | undefined) =>
  val != null ? `$${val.toFixed(2)}` : "—";

const pctChange = (current: number, prev: number) => {
  if (!prev) return null;
  return ((current - prev) / prev) * 100;
};

function SearchBar() {
  // All stocks fetched once from the backend
  const [allStocks, setAllStocks] = useState<Record<string, StockData>>({});
  // What the user has typed
  const [query, setQuery] = useState("");
  // Whether the dropdown is visible
  const [open, setOpen] = useState(false);
  // The stock the user clicked — shown in the detail modal
  const [selected, setSelected] = useState<StockData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { user } = useAuth();
  const { triggerRefresh } = useRefresh();
  const [tradeShares, setTradeShares] = useState("");
  const [tradeLoading, setTradeLoading] = useState(false);
  const [tradeMsg, setTradeMsg] = useState<string | null>(null);
  const [tradeMsgType, setTradeMsgType] = useState<"success" | "error">(
    "success",
  );

  const containerRef = useRef<HTMLDivElement>(null);

  // Fetch all stocks once on mount — same endpoint as homepage
  useEffect(() => {
    const fetchStocks = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_URL}/stocks`);
        if (!res.ok) throw new Error("Could not fetch stocks");
        const data = await res.json();
        setAllStocks(data.stocks);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    };
    fetchStocks();
  }, []);

  // Close dropdown when clicking outside the component
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Filter stocks by ticker (stock_key) or company name — case-insensitive
  const filtered = query.trim()
    ? Object.values(allStocks).filter(
        (s) =>
          s.stock_key.toLowerCase().includes(query.toLowerCase()) ||
          s.name.toLowerCase().includes(query.toLowerCase()),
      )
    : [];

  // Reset trade state when a different stock is selected
  useEffect(() => {
    setTradeShares("");
    setTradeMsg(null);
    setTradeLoading(false);
  }, [selected?.stock_key]);

  const handleBuy = async () => {
    const qty = parseInt(tradeShares, 10);
    if (!qty || qty < 1) {
      setTradeMsg("Enter a valid number of shares.");
      setTradeMsgType("error");
      return;
    }
    if (!user || !selected) return;
    setTradeLoading(true);
    setTradeMsg(null);
    try {
      const res = await fetch(`${API_URL}/user/${user.id}/buy`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ num_share: qty, stock_key: selected.stock_key }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        setTradeMsg((data as any).message ?? "Buy failed.");
        setTradeMsgType("error");
      } else {
        const price = (data as any).price;
        setTradeMsg(
          `Bought ${qty} share${qty > 1 ? "s" : ""}${price != null ? ` at ${fmt(price)}` : ""}`,
        );
        setTradeMsgType("success");
        setTradeShares("");
        triggerRefresh();
      }
    } catch {
      setTradeMsg("Network error — check your connection.");
      setTradeMsgType("error");
    } finally {
      setTradeLoading(false);
    }
  };

  const handleSelect = (stock: StockData) => {
    setSelected(stock);
    setQuery("");
    setOpen(false);
  };

  return (
    <>
      {/* Search input + dropdown */}
      <div className="sb-wrap" ref={containerRef}>
        <div className="sb-input-row">
          <svg className="sb-icon" viewBox="0 0 20 20" fill="none">
            <circle
              cx="8.5"
              cy="8.5"
              r="5.5"
              stroke="currentColor"
              strokeWidth="1.5"
            />
            <path
              d="M13 13l3.5 3.5"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
          </svg>
          <input
            className="sb-input"
            type="text"
            placeholder={
              loading
                ? "Loading..."
                : error
                  ? "Unavailable"
                  : "Search ticker or name..."
            }
            value={query}
            disabled={loading || !!error}
            onChange={(e) => {
              setQuery(e.target.value);
              setOpen(true);
            }}
            onFocus={() => query.trim() && setOpen(true)}
          />
          {query && (
            <button
              className="sb-clear"
              onClick={() => {
                setQuery("");
                setOpen(false);
              }}
            >
              ✕
            </button>
          )}
        </div>

        {open && filtered.length > 0 && (
          <ul className="sb-dropdown">
            {filtered.map((stock) => {
              const pct = pctChange(stock.current_price, stock.previous_close);
              const up = pct != null && pct >= 0;
              return (
                <li
                  key={stock.stock_key}
                  className="sb-result"
                  onMouseDown={() => handleSelect(stock)}
                >
                  <div className="sb-result-left">
                    <span className="sb-result-ticker">{stock.stock_key}</span>
                    <span className="sb-result-name">{stock.name}</span>
                  </div>
                  <div className="sb-result-right">
                    <span className="sb-result-price">
                      {fmt(stock.current_price)}
                    </span>
                    {pct != null && (
                      <span
                        className={`sb-result-pct ${up ? "sb-up" : "sb-down"}`}
                      >
                        {up ? "▲" : "▼"} {Math.abs(pct).toFixed(2)}%
                      </span>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
        )}

        {open && query.trim() && filtered.length === 0 && !loading && (
          <div className="sb-no-results">No results for "{query}"</div>
        )}
      </div>

      {/* Full stock detail modal */}
      {selected && (
        <div className="sb-modal-backdrop" onClick={() => setSelected(null)}>
          <div className="sb-modal" onClick={(e) => e.stopPropagation()}>
            <button
              className="sb-modal-close"
              onClick={() => setSelected(null)}
            >
              ✕
            </button>

            <div className="sb-modal-header">
              <span className="sb-modal-ticker">{selected.stock_key}</span>
              <span className="sb-modal-name">{selected.name}</span>
            </div>

            <div className="sb-modal-price-row">
              <span className="sb-modal-current">
                {fmt(selected.current_price)}
              </span>
              {(() => {
                const pct = pctChange(
                  selected.current_price,
                  selected.previous_close,
                );
                if (pct == null) return null;
                const up = pct >= 0;
                return (
                  <span className={`sb-modal-pct ${up ? "sb-up" : "sb-down"}`}>
                    {up ? "▲" : "▼"} {Math.abs(pct).toFixed(2)}%
                  </span>
                );
              })()}
            </div>

            <div className="sb-modal-grid">
              <div className="sb-modal-stat">
                <span className="sb-stat-label">OPEN</span>
                <span className="sb-stat-value">
                  {fmt(selected.open_price)}
                </span>
              </div>
              <div className="sb-modal-stat">
                <span className="sb-stat-label">PREV CLOSE</span>
                <span className="sb-stat-value">
                  {fmt(selected.previous_close)}
                </span>
              </div>
              <div className="sb-modal-stat">
                <span className="sb-stat-label">HIGH</span>
                <span className="sb-stat-value sb-up">
                  {fmt(selected.high_today)}
                </span>
              </div>
              <div className="sb-modal-stat">
                <span className="sb-stat-label">LOW</span>
                <span className="sb-stat-value sb-down">
                  {fmt(selected.low_today)}
                </span>
              </div>
            </div>

            {/* Day range bar */}
            {selected.low_today > 0 &&
              selected.high_today > selected.low_today && (
                <div className="sb-range-wrap">
                  <span className="sb-range-label">Day range</span>
                  <div className="sb-range-bar">
                    <div
                      className="sb-range-fill"
                      style={{
                        left: "0%",
                        width: `${
                          ((selected.current_price - selected.low_today) /
                            (selected.high_today - selected.low_today)) *
                          100
                        }%`,
                      }}
                    />
                    <div
                      className="sb-range-dot"
                      style={{
                        left: `${
                          ((selected.current_price - selected.low_today) /
                            (selected.high_today - selected.low_today)) *
                          100
                        }%`,
                      }}
                    />
                  </div>
                  <div className="sb-range-ends">
                    <span>{fmt(selected.low_today)}</span>
                    <span>{fmt(selected.high_today)}</span>
                  </div>
                </div>
              )}

            {/* Trade section */}
            <div className="sb-trade-section">
              <span className="sb-stat-label">TRADE</span>
              {user ? (
                <div className="sb-trade-row">
                  <input
                    type="number"
                    className="sb-trade-input"
                    min="1"
                    value={tradeShares}
                    onChange={(e) => setTradeShares(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleBuy()}
                    placeholder="Shares"
                  />
                  <button
                    className="sb-trade-buy"
                    onClick={handleBuy}
                    disabled={tradeLoading}
                  >
                    {tradeLoading ? "..." : "BUY"}
                  </button>
                </div>
              ) : (
                <p className="sb-trade-msg sb-trade-info">Log in to trade</p>
              )}
              {tradeMsg && (
                <p
                  className={`sb-trade-msg ${tradeMsgType === "error" ? "sb-trade-error" : "sb-trade-success"}`}
                >
                  {tradeMsg}
                </p>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default SearchBar;
