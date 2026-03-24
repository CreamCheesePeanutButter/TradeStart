import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./loginpage.css";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:5000";

function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [isLogin, setIsLogin] = useState(true);
  const [identifier, setIdentifier] = useState(""); // email or username for login
  const [email, setEmail] = useState(""); // email for signup
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [username, setUsername] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const validateEmail = (value: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  };

  const handleLogin = async () => {
    if (!identifier || !password) {
      setErrorMessage("Email/username and password are required.");
      return;
    }

    setIsLoading(true);
    setErrorMessage("");

    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      //add token
      body: JSON.stringify({ identifier, password }),
    });

    const data = await response.json();
    setIsLoading(false);

    if (response.ok) {
      login({
        id: data.user.userID,
        username: data.user.username,
        email: data.user.email,
        balance: data.user.available_funds,
        //token is here
        token: data.token,
      });
      navigate("/", { replace: true });
    } else if (response.status === 400) {
      setErrorMessage("Email/username and password are required.");
    } else if (response.status === 401) {
      setErrorMessage("Incorrect email/username or password.");
    } else {
      setErrorMessage(data.message || "Something went wrong.");
    }
  };

  const handleRegister = async () => {
    if (
      !firstName ||
      !lastName ||
      !username ||
      !email ||
      !password ||
      !confirmPassword
    ) {
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

    const response = await fetch(`${API_URL}/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        password,
        first_name: firstName,
        last_name: lastName,
        username,
      }),
    });

    const data = await response.json();
    setIsLoading(false);

    if (response.ok) {
      navigate("/setup-funds", { state: { userId: data.user_id } });
    } else if (response.status === 409) {
      setErrorMessage("An account with that email already exists.");
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
    setIdentifier("");
    setEmail("");
    setPassword("");
    setConfirmPassword("");
    setFirstName("");
    setLastName("");
    setUsername("");
    setShowPassword(false);
  };

  return (
    <div className="page-root">
      <div className="bg-grid" />
      <div className="bg-glow" />

      <div className="card">
        <div className="brand-row">
          <div className="xbox-icon">
            <svg
              viewBox="0 0 40 40"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
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
          {!isLogin && (
            <>
              <div className="field-row">
                <div className="field-group">
                  <label className="field-label">FIRST NAME</label>
                  <input
                    className="text-input"
                    type="text"
                    placeholder="John"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    autoComplete="given-name"
                  />
                </div>
                <div className="field-group">
                  <label className="field-label">LAST NAME</label>
                  <input
                    className="text-input"
                    type="text"
                    placeholder="Doe"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    autoComplete="family-name"
                  />
                </div>
              </div>
              <div className="field-group">
                <label className="field-label">USERNAME</label>
                <input
                  className="text-input"
                  type="text"
                  placeholder="johndoe"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  autoComplete="username"
                />
              </div>
            </>
          )}

          <div className="field-group">
            <label className="field-label">
              {isLogin ? "EMAIL OR USERNAME" : "EMAIL"}
            </label>
            <input
              className="text-input"
              type="text"
              placeholder={
                isLogin ? "you@example.com or johndoe" : "you@example.com"
              }
              value={isLogin ? identifier : email}
              onChange={(e) =>
                isLogin
                  ? setIdentifier(e.target.value)
                  : setEmail(e.target.value)
              }
              autoComplete={isLogin ? "username" : "email"}
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
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94" />
                    <path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19" />
                    <line x1="1" y1="1" x2="23" y2="23" />
                  </svg>
                ) : (
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
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

          {errorMessage && <div className="msg msg-error">{errorMessage}</div>}

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
