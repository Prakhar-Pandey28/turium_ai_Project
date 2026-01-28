import { useEffect, useState } from "react";
import "./App.css";

const API = "https://ai-knowledge-box.onrender.com";

export default function App() {
  const [content, setContent] = useState("");
  const [url, setUrl] = useState("");
  const [items, setItems] = useState([]);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("add");

  const fetchItems = async () => {
    try {
      const res = await fetch(`${API}/items`);
      const data = await res.json();
      setItems(data);
    } catch (error) {
      console.error("Error fetching items:", error);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleIngest = async () => {
    if (!content && !url) {
      alert("Please enter a note or URL");
      return;
    }

    // Prevent double submission (exhaustMap behavior)
    if (loading) return;

    setLoading(true);
    try {
      await fetch(`${API}/ingest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content, url }),
      });

      setContent("");
      setUrl("");
      fetchItems();
      setActiveTab("knowledge");
      // Optional: alert success or just switch tabs
    } catch (error) {
      alert("Error ingesting content");
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const res = await fetch(`${API}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      setAnswer("Error getting answer. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const getItemTitle = (content, sourceType) => {
    if (sourceType === "note") {
      return content.slice(0, 60).trim() + (content.length > 60 ? "..." : "");
    }

    const titleMatch = content.match(/Title: (.+)/);
    if (titleMatch) {
      return titleMatch[1].slice(0, 80);
    }

    const lines = content.split('\n').filter(line => line.trim().length > 10);
    return lines[0]?.slice(0, 80) || "Untitled";
  };

  return (
    <div className="app">
      {/* Animated Background */}
      <div className="cyber-grid"></div>
      <div className="particles">
        {[...Array(30)].map((_, i) => (
          <div key={i} className="particle" style={{
            left: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 5}s`,
            animationDuration: `${5 + Math.random() * 10}s`
          }}></div>
        ))}
      </div>

      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="logo-container">
            <div className="logo-glow"></div>
            <img src="/turium-logo.png" alt="Turium AI" className="logo-image" />
            <h1 className="logo">
              TURIUM <span className="accent">AI</span>
            </h1>
          </div>
          <p className="tagline">Enterprise Knowledge Intelligence Platform</p>
        </header>

        {/* Tab Navigation */}
        <div className="tabs">
          <button
            className={`tab ${activeTab === "add" ? "active" : ""}`}
            onClick={() => setActiveTab("add")}
          >
            <span className="tab-icon">➕</span>
            Add Knowledge
          </button>
          <button
            className={`tab ${activeTab === "knowledge" ? "active" : ""}`}
            onClick={() => setActiveTab("knowledge")}
          >
            <span className="tab-icon">💾</span>
            Knowledge Base
            {items.length > 0 && <span className="badge">{items.length}</span>}
          </button>
          <button
            className={`tab ${activeTab === "ask" ? "active" : ""}`}
            onClick={() => setActiveTab("ask")}
          >
            <span className="tab-icon">🧠</span>
            Ask AI
          </button>
        </div>

        {/* Add Knowledge Tab */}
        {activeTab === "add" && (
          <div className="panel fade-in">
            <div className="panel-header">
              <h2>Inject New Knowledge</h2>
              <div className="header-line"></div>
            </div>
            <textarea
              placeholder="Paste your notes here..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="input-field textarea"
            />
            <div className="divider">
              <span>OR</span>
            </div>
            <input
              placeholder="https://example.com/article"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="input-field"
            />
            <button onClick={handleIngest} className="cyber-button" disabled={loading}>
              <span className="button-glow"></span>
              <span className="button-text">
                {loading ? "Ingesting..." : "Upload to Neural Net"}
              </span>
            </button>
          </div>
        )}

        {/* Knowledge Base Tab */}
        {activeTab === "knowledge" && (
          <div className="panel fade-in">
            <div className="panel-header">
              <h2>Knowledge Vault</h2>
              <div className="header-line"></div>
            </div>
            {items.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">📭</div>
                <p>No knowledge stored yet</p>
                <button onClick={() => setActiveTab("add")} className="link-button">
                  Add your first entry →
                </button>
              </div>
            ) : (
              <div className="knowledge-grid">
                {items.map((item, index) => (
                  <div key={item[0]} className="knowledge-card" style={{
                    animationDelay: `${index * 0.1}s`
                  }}>
                    <div className="card-header">
                      <span className="card-icon">
                        {item[2] === "url" ? "🔗" : "📝"}
                      </span>
                      <span className="card-type">{item[2]}</span>
                    </div>
                    <h3 className="card-title">{getItemTitle(item[1], item[2])}</h3>
                    <div className="card-footer">
                      <span className="card-date">
                        {new Date(item[3]).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric'
                        })}
                      </span>
                    </div>
                    <div className="card-shine"></div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Ask AI Tab */}
        {activeTab === "ask" && (
          <div className="panel fade-in">
            <div className="panel-header">
              <h2>Query Neural Network</h2>
              <div className="header-line"></div>
            </div>
            <div className="search-container">
              <input
                placeholder="What would you like to know?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleAsk()}
                className="input-field search-input"
              />
              <button onClick={handleAsk} className="cyber-button" disabled={loading}>
                <span className="button-glow"></span>
                <span className="button-text">
                  {loading ? "Processing..." : "Execute Query"}
                </span>
              </button>
            </div>

            {loading && (
              <div className="loader-container">
                <div className="neural-loader">
                  <div className="loader-ring"></div>
                  <div className="loader-ring"></div>
                  <div className="loader-ring"></div>
                </div>
                <p className="loader-text">Analyzing knowledge base...</p>
              </div>
            )}

            {answer && !loading && (
              <div className="answer-container">
                <div className="answer-label">
                  <span className="label-icon">✨</span>
                  Neural Response
                </div>
                <div className="answer-text">{answer}</div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
