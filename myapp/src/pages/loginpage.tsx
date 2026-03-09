import React, { useState } from "react";
import "./loginpage.css";

function LoginPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const validateEmail = (value: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  };

  const handleLogin = async () => {
    if (!email || !password) {
      setErrorMessage("Email and password are required.");
      return;
    }
    if (!validateEmail(email)) {
      setErrorMessage("Enter a valid email address.");
      return;
    }

    setIsLoading(true);
    setErrorMessage("");
    setSuccessMessage("");

    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    setIsLoading(false);

    if (response.ok) {
      setSuccessMessage("Signed in successfully.");
    } else if (response.status === 400) {
      setErrorMessage("Email and password are required.");
    } else if (response.status === 401) {
      setErrorMessage("Incorrect email or password.");
    } else {
      setErrorMessage(data.message || "Something went wrong.");
    }
  };

  const handleRegister = async () => {
    if (!email || !password || !confirmPassword) {
      setErrorMessage("All fields are required.");
      return;
    }
    if (!validateEmail(email)) {
      setErrorMessage("Enter a valid email address.");
      return;
    }
    if (password !== confirmPassword) {
      setErrorMessage("Passwords do not match.");
      return;
    }
    if (password.length < 6) {
      setErrorMessage("Password must be at least 6 characters.");
      return;
    }

    setIsLoading(true);
    setErrorMessage("");
    setSuccessMessage("");

    const response = await fetch("http://127.0.0.1:5000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    setIsLoading(false);

    if (response.ok) {
      setSuccessMessage("Account created. You can now sign in.");
      setIsLogin(true);
      setEmail("");
      setPassword("");
      setConfirmPassword("");
    } else if (response.status === 400) {
      setErrorMessage("Email already in use or invalid data.");
    } else {
      setErrorMessage(data.message || "Registration failed.");
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (isLogin) {
      handleLogin();
    } else {
      handleRegister();
    }
  };

  const switchMode = (toLogin: boolean) => {
    setIsLogin(toLogin);
    setErrorMessage("");
    setSuccessMessage("");
    setEmail("");
    setPassword("");
    setConfirmPassword("");
    setShowPassword(false);
  };

  return (
    <div className="page-root">
      <div className="bg-grid" />
      <div className="bg-glow" />

      <div className="card">
        <div className="brand-row">
          <div className="xbox-icon">
            <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="20" cy="20" r="19" stroke="#107C10" strokeWidth="2" />
              <path
                d="M10 14c2-3 5-5 10-5s8 2 10 5c-2 3-5 8-10 11C15 22 12 17 10 14z"
                fill="#107C10"
                opacity="0.3"
              />
              <path
                d="M13 28c-2-2-3-5-3-8 0-2 0-4 1-6 1 2 4 7 9 10-2 2-5 4-7 4z"
                fill="#107C10"
              />
              <path
                d="M27 28c2-2 3-5 3-8 0-2 0-4-1-6-1 2-4 7-9 10 2 2 5 4 7 4z"
                fill="#107C10"
              />
              <circle cx="20" cy="20" r="4" fill="#107C10" />
            </svg>
          </div>
          <span className="brand-label">TradeStart</span>
        </div>

        <div className="tab-row">
          <button
            type="button"
            className={`tab-btn ${isLogin ? "tab-active" : ""}`}
            onClick={() => switchMode(true)}
          >
            SIGN IN
          </button>
          <button
            type="button"
            className={`tab-btn ${!isLogin ? "tab-active" : ""}`}
            onClick={() => switchMode(false)}
          >
            CREATE ACCOUNT
          </button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form" noValidate>
          <div className="field-group">
            <label className="field-label">EMAIL</label>
            <input
              className="text-input"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
            />
          </div>

          <div className="field-group">
            <label className="field-label">PASSWORD</label>
            <div className="password-wrap">
              <input
                className="text-input"
                type={showPassword ? "text" : "password"}
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete={isLogin ? "current-password" : "new-password"}
              />
              <button
                type="button"
                className="toggle-vis"
                onClick={() => setShowPassword(!showPassword)}
                tabIndex={-1}
              >
                {showPassword ? (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94" />
                    <path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19" />
                    <line x1="1" y1="1" x2="23" y2="23" />
                  </svg>
                ) : (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                )}
              </button>
            </div>
          </div>

          {!isLogin && (
            <div className="field-group">
              <label className="field-label">CONFIRM PASSWORD</label>
              <input
                className="text-input"
                type={showPassword ? "text" : "password"}
                placeholder="Re-enter password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                autoComplete="new-password"
              />
            </div>
          )}

          {errorMessage && (
            <div className="msg msg-error">{errorMessage}</div>
          )}
          {successMessage && (
            <div className="msg msg-success">{successMessage}</div>
          )}

          <button type="submit" className="submit-btn" disabled={isLoading}>
            {isLoading ? (
              <span className="spinner" />
            ) : isLogin ? (
              "SIGN IN"
            ) : (
              "CREATE ACCOUNT"
            )}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;