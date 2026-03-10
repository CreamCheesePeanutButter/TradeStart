import "./aboutpage.css";

function AboutPage() {
  return (
    <div className="about-page">
      <div className="bg-grid" />
      <div className="about-content">
        <h1 className="about-title">About TradeStart</h1>
        <p className="about-subtitle">
          A real-time stock trading platform.
        </p>

        <div className="about-section">
          <h2 className="about-section-title">What is TradeStart?</h2>
          <p className="about-body">
            TradeStart is a ...
          </p>
        </div>

        <div className="about-section">
          <h2 className="about-section-title">Stack</h2>
          <div className="about-grid">
            <div className="about-card">
              <span className="about-card-label">Frontend</span>
              <span className="about-card-value">React 19 + TypeScript</span>
            </div>
            <div className="about-card">
              <span className="about-card-label">Bundler</span>
              <span className="about-card-value">Vite</span>
            </div>
            <div className="about-card">
              <span className="about-card-label">Backend</span>
              <span className="about-card-value">Python Flask</span>
            </div>
            <div className="about-card">
              <span className="about-card-label">Database</span>
              <span className="about-card-value">MySQL</span>
            </div>
            <div className="about-card">
              <span className="about-card-label">Data</span>
              <span className="about-card-value">Finnhub API</span>
            </div>
            <div className="about-card">
              <span className="about-card-label">Course</span>
              <span className="about-card-value">CSCI 2040</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AboutPage;