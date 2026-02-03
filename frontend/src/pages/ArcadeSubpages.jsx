import { Link } from "react-router-dom";
import { useArcade, CANONS } from "../context/ArcadeContext";
import "../styles/Arcade.css";

const ArcadeSessions = () => {
  const { sessions, tokens } = useArcade();

  return (
    <div className="arcade-container" data-testid="arcade-sessions">
      <div className="arcade-grid-bg"></div>
      
      <header className="arcade-header">
        <div className="arcade-header-left">
          <Link to="/arcade" className="arcade-back">← Back to Hub</Link>
          <h1 className="arcade-title">
            <span className="neon-text">SESSIONS</span>
          </h1>
        </div>
        <div className="arcade-header-right">
          <div className="token-display">
            <span className="token-icon">🪙</span>
            <span className="token-amount">{tokens.toLocaleString()}</span>
          </div>
        </div>
      </header>

      <section className="sessions-section">
        {sessions.length === 0 ? (
          <div className="empty-sessions">
            <span className="empty-icon">📋</span>
            <h3>No Sessions Yet</h3>
            <p>Play some machines to see your history here</p>
            <Link to="/arcade" className="back-to-arcade-btn">Go to Arcade</Link>
          </div>
        ) : (
          <div className="sessions-list" data-testid="sessions-list">
            {sessions.map((session, i) => {
              const canon = CANONS[session.canon];
              return (
                <div 
                  key={session.id || i}
                  className="session-card"
                  style={{ '--canon-color': canon?.colors.primary || '#666' }}
                >
                  <div className="session-header">
                    <div className="session-machine">
                      <span className="session-canon-icon">{canon?.icon}</span>
                      <span className="session-machine-name">{session.machine}</span>
                    </div>
                    <span className="session-time">
                      {new Date(session.timestamp).toLocaleString()}
                    </span>
                  </div>
                  <div className="session-input">
                    <strong>Input:</strong> {session.input?.slice(0, 100)}...
                  </div>
                  <div className="session-meta">
                    <span className="session-cost">🪙 {session.cost}</span>
                    <span className="session-duration">{(session.duration / 1000).toFixed(1)}s</span>
                    {session.jackpot && (
                      <span className="session-jackpot">🎰 +{session.jackpot.amount}</span>
                    )}
                  </div>
                  <details className="session-output">
                    <summary>View Output</summary>
                    <pre>{JSON.stringify(session.output, null, 2)}</pre>
                  </details>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
};

const ArcadeWallet = () => {
  const { tokens, addTokens, jackpotPool, recentJackpots } = useArcade();

  const buyTokens = (amount) => {
    addTokens(amount);
  };

  return (
    <div className="arcade-container" data-testid="arcade-wallet">
      <div className="arcade-grid-bg"></div>
      
      <header className="arcade-header">
        <div className="arcade-header-left">
          <Link to="/arcade" className="arcade-back">← Back to Hub</Link>
          <h1 className="arcade-title">
            <span className="neon-text">WALLET</span>
          </h1>
        </div>
      </header>

      <section className="wallet-section">
        <div className="wallet-balance">
          <span className="wallet-icon">🪙</span>
          <span className="wallet-amount">{tokens.toLocaleString()}</span>
          <span className="wallet-label">TOKENS</span>
        </div>

        <div className="wallet-actions">
          <h3>Get More Tokens</h3>
          <div className="token-packages">
            <button className="token-package" onClick={() => buyTokens(100)}>
              <span className="package-amount">100</span>
              <span className="package-bonus">Free</span>
            </button>
            <button className="token-package" onClick={() => buyTokens(500)}>
              <span className="package-amount">500</span>
              <span className="package-bonus">Free</span>
            </button>
            <button className="token-package" onClick={() => buyTokens(1000)}>
              <span className="package-amount">1000</span>
              <span className="package-bonus">Free</span>
            </button>
          </div>
        </div>

        <div className="jackpot-info">
          <h3>Jackpot Pool</h3>
          <div className="jackpot-pool-display">
            <span className="pool-icon">💎</span>
            <span className="pool-amount">{jackpotPool.toLocaleString()}</span>
          </div>
        </div>

        <div className="recent-wins">
          <h3>Your Recent Wins</h3>
          {recentJackpots.length > 0 ? (
            <div className="wins-list">
              {recentJackpots.slice(0, 5).map((win, i) => (
                <div key={i} className="win-item">
                  <span>{win.name}</span>
                  <span>+{win.amount.toLocaleString()} 🪙</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-wins">No jackpots yet!</p>
          )}
        </div>
      </section>
    </div>
  );
};

const ArcadeTeams = () => {
  const { tokens } = useArcade();

  const aiTeams = [
    { id: "horror_squad", name: "Horror Squad", members: ["Monster Builder", "Fear Engine", "Curse Generator"], bonus: "1.5x Horror outputs" },
    { id: "anime_crew", name: "Anime Crew", members: ["Character Engine", "Lore Engine", "Episode Engine"], bonus: "Complete anime packages" },
    { id: "business_team", name: "Business Team", members: ["Strategy Engine", "Pricing Engine", "Blueprint Engine"], bonus: "Full business plans" }
  ];

  return (
    <div className="arcade-container" data-testid="arcade-teams">
      <div className="arcade-grid-bg"></div>
      
      <header className="arcade-header">
        <div className="arcade-header-left">
          <Link to="/arcade" className="arcade-back">← Back to Hub</Link>
          <h1 className="arcade-title">
            <span className="neon-text">AI TEAMS</span>
          </h1>
        </div>
        <div className="arcade-header-right">
          <div className="token-display">
            <span className="token-icon">🪙</span>
            <span className="token-amount">{tokens.toLocaleString()}</span>
          </div>
        </div>
      </header>

      <section className="teams-section">
        <p className="teams-intro">Combine multiple engines for powerful chain outputs</p>
        <div className="teams-grid">
          {aiTeams.map(team => (
            <div key={team.id} className="team-card">
              <h3>{team.name}</h3>
              <div className="team-members">
                {team.members.map((member, i) => (
                  <span key={i} className="team-member">{member}</span>
                ))}
              </div>
              <p className="team-bonus">{team.bonus}</p>
              <button className="activate-team-btn">Activate Team</button>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

const ArcadePacks = () => {
  const { sessions, tokens } = useArcade();

  const outputPacks = sessions.reduce((acc, session) => {
    const canon = session.canon;
    if (!acc[canon]) acc[canon] = [];
    acc[canon].push(session);
    return acc;
  }, {});

  return (
    <div className="arcade-container" data-testid="arcade-packs">
      <div className="arcade-grid-bg"></div>
      
      <header className="arcade-header">
        <div className="arcade-header-left">
          <Link to="/arcade" className="arcade-back">← Back to Hub</Link>
          <h1 className="arcade-title">
            <span className="neon-text">OUTPUT PACKS</span>
          </h1>
        </div>
        <div className="arcade-header-right">
          <div className="token-display">
            <span className="token-icon">🪙</span>
            <span className="token-amount">{tokens.toLocaleString()}</span>
          </div>
        </div>
      </header>

      <section className="packs-section">
        <p className="packs-intro">Bundle your outputs into sellable packs</p>
        
        {Object.keys(outputPacks).length === 0 ? (
          <div className="empty-packs">
            <span className="empty-icon">📦</span>
            <h3>No Outputs Yet</h3>
            <p>Generate some outputs to create packs</p>
          </div>
        ) : (
          <div className="packs-grid">
            {Object.entries(outputPacks).map(([canon, outputs]) => {
              const canonData = CANONS[canon];
              return (
                <div 
                  key={canon} 
                  className="pack-card"
                  style={{ '--canon-color': canonData?.colors.primary }}
                >
                  <div className="pack-header">
                    <span className="pack-icon">{canonData?.icon}</span>
                    <h3>{canonData?.name} Pack</h3>
                  </div>
                  <p className="pack-count">{outputs.length} outputs</p>
                  <div className="pack-actions">
                    <button className="export-pack-btn">Export JSON</button>
                    <button className="share-pack-btn">Share Pack</button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
};

export { ArcadeSessions, ArcadeWallet, ArcadeTeams, ArcadePacks };
