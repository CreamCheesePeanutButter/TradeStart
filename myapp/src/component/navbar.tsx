import "./navbar.css";

export function Navbar() {
  return (
    <nav className="navbar">
      <span className="navbar-brand">TRADESTART</span>
      <ul className="navbar-links">
        <li>
          <a href="/" className="nav-link">Home</a>
        </li>
        <li>
          <a href="/about" className="nav-link">About</a>
        </li>
        <li>
          <a href="/login" className="nav-link nav-link-cta">Login</a>
        </li>
      </ul>
    </nav>
  );
}
