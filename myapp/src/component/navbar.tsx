import React, { useState, useRef, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import SearchBar from "./searchbar";
import "./navbar.css";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:5000";
const FUNDS_MAX = 10000;
const FUNDS_STEP = 50;

export function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [menuOpen, setMenuOpen] = useState(false);
  const [fundsOpen, setFundsOpen] = useState(false);
  const [fundsAmount, setFundsAmount] = useState(500);
  const [fundsLoading, setFundsLoading] = useState(false);
  const [fundsMsg, setFundsMsg] = useState("");

  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const handleLogout = () => {
    logout();
    setMenuOpen(false);
    navigate("/login");
  };

  const openFunds = () => {
    setMenuOpen(false);
    setFundsAmount(500);
    setFundsMsg("");
    setFundsOpen(true);
  };

  const handleAddFunds = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;
    setFundsLoading(true);
    setFundsMsg("");

    const res = await fetch(`${API_URL}/add-funds`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: user.id, amount: fundsAmount }),
    });

    setFundsLoading(false);
    if (res.ok) {
      setFundsMsg("Funds added successfully!");
      setTimeout(() => {
        setFundsOpen(false);
        setFundsMsg("");
      }, 1200);
    } else {
      setFundsMsg("Failed to add funds. Please try again.");
    }
  };

  const fundsPct = (fundsAmount / FUNDS_MAX) * 100;

  return (
    <>
      <nav className="navbar">
        <span className="navbar-brand">TRADESTART</span>

        <div className="navbar-search">
          <SearchBar />
        </div>

        <ul className="navbar-links">
          <li>
            <Link to="/" className="nav-link">
              Home
            </Link>
          </li>
          <li>
            <Link to="/about" className="nav-link">
              About
            </Link>
          </li>
          <li>
            {user ? (
              <div className="nav-user" ref={menuRef}>
                <button
                  className="nav-username-btn"
                  onClick={() => setMenuOpen((o) => !o)}
                >
                  <span className="nav-user-dot" />
                  {user.username}
                  <svg className="nav-chevron" viewBox="0 0 10 6" fill="none">
                    <path
                      d="M1 1l4 4 4-4"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </button>
                {menuOpen && (
                  <div className="nav-dropdown">
                    <button className="nav-dd-item" onClick={openFunds}>
                      Add Funds
                    </button>
                    <button
                      className="nav-dd-item nav-dd-logout"
                      onClick={handleLogout}
                    >
                      Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <Link to="/login" className="nav-link nav-link-cta">
                Login
              </Link>
            )}
          </li>
        </ul>
      </nav>

      {fundsOpen && (
        <div className="nav-modal-backdrop" onClick={() => setFundsOpen(false)}>
          <div className="nav-modal" onClick={(e) => e.stopPropagation()}>
            <button
              className="nav-modal-close"
              onClick={() => setFundsOpen(false)}
            >
              ✕
            </button>
            <h3 className="nav-modal-title">ADD FUNDS</h3>

            <form onSubmit={handleAddFunds} className="nav-modal-form">
              <div className="nav-modal-amount">
                ${fundsAmount.toLocaleString()}
              </div>

              <div className="sf-slider-wrap">
                <div className="sf-track">
                  <div className="sf-fill" style={{ width: `${fundsPct}%` }} />
                  <div className="sf-thumb" style={{ left: `${fundsPct}%` }} />
                </div>
                <input
                  type="range"
                  min={0}
                  max={FUNDS_MAX}
                  step={FUNDS_STEP}
                  value={fundsAmount}
                  onChange={(e) => setFundsAmount(Number(e.target.value))}
                  className="sf-range"
                />
              </div>
              <div className="sf-range-labels">
                <span>$0</span>
                <span>$10,000</span>
              </div>

              <div className="nav-modal-field">
                <label className="nav-modal-label">OR ENTER AMOUNT</label>
                <input
                  className="nav-modal-input"
                  type="number"
                  min={0}
                  max={FUNDS_MAX}
                  value={fundsAmount}
                  onChange={(e) =>
                    setFundsAmount(
                      Math.min(
                        FUNDS_MAX,
                        Math.max(0, Number(e.target.value) || 0),
                      ),
                    )
                  }
                />
              </div>

              {fundsMsg && (
                <div
                  className={`nav-modal-msg ${fundsMsg.includes("success") ? "nav-modal-msg-ok" : "nav-modal-msg-err"}`}
                >
                  {fundsMsg}
                </div>
              )}

              <button
                type="submit"
                className="nav-modal-btn"
                disabled={fundsLoading}
              >
                {fundsLoading ? (
                  <span className="nav-modal-spinner" />
                ) : (
                  "ADD FUNDS"
                )}
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
