import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./setupfunds.css";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:5000";
const MIN = 0;
const MAX = 10000;
const STEP = 50;

function SetupFundsPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const userId: number =
    (location.state as { userId: number } | null)?.userId ?? 0;

  const [amount, setAmount] = useState(1000);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSlider = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAmount(Number(e.target.value));
  };

  const handleInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const v = Math.min(MAX, Math.max(MIN, Number(e.target.value) || 0));
    setAmount(v);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userId) {
      setError("Session expired. Please sign up again.");
      return;
    }
    setIsLoading(true);
    setError("");

    const res = await fetch(`${API_URL}/add-funds`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, amount }),
    });

    setIsLoading(false);

    if (res.ok) {
      navigate("/login", { replace: true });
    } else {
      setError("Could not set balance. Please try again.");
    }
  };

  const pct = ((amount - MIN) / (MAX - MIN)) * 100;

  return (
    <div className="sf-page">
      <div className="bg-grid" />
      <div className="bg-glow" />

      <div className="card sf-card">
        <div className="sf-header">
          <h2 className="sf-title">SET STARTING BALANCE</h2>
          <p className="sf-sub">Choose how much to start trading with.</p>
        </div>

        <form onSubmit={handleSubmit} className="sf-form">
          <div className="sf-amount-display">${amount.toLocaleString()}</div>

          <div className="sf-slider-wrap">
            <div className="sf-track">
              <div className="sf-fill" style={{ width: `${pct}%` }} />
              <div className="sf-thumb" style={{ left: `${pct}%` }} />
            </div>
            <input
              className="sf-range"
              type="range"
              min={MIN}
              max={MAX}
              step={STEP}
              value={amount}
              onChange={handleSlider}
            />
          </div>

          <div className="sf-range-labels">
            <span>$0</span>
            <span>$10,000</span>
          </div>

          <div className="field-group">
            <label className="field-label">OR ENTER AN AMOUNT</label>
            <input
              className="text-input"
              type="number"
              min={MIN}
              max={MAX}
              value={amount}
              onChange={handleInput}
            />
          </div>

          {error && <div className="msg msg-error">{error}</div>}

          <button type="submit" className="submit-btn" disabled={isLoading}>
            {isLoading ? (
              <span className="spinner" />
            ) : (
              "CONFIRM & CONTINUE TO LOGIN"
            )}
          </button>
        </form>
      </div>
    </div>
  );
}

export default SetupFundsPage;
