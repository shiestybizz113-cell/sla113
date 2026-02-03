import { useState } from "react";
import axios from "axios";
import { useArcade } from "../context/ArcadeContext";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

// Map machine IDs to actual backend endpoints
const MACHINE_ENDPOINTS = {
  // Anime
  character_engine: { endpoint: "/anime/character", payloadKey: "concept" },
  lore_engine: { endpoint: "/anime/lore", payloadKey: "world_concept" },
  episode_engine: { endpoint: "/anime/story", payloadKey: "concept" },
  art_direction: { endpoint: "/art-direction", payloadKey: "project" },
  
  // General engines that work for all canons
  monster_builder: { endpoint: "/persona", payloadKey: "audience", transform: (input, canon) => ({ audience: `${canon} monster: ${input}` }) },
  fear_engine: { endpoint: "/strategy", payloadKey: "goal", transform: (input) => ({ goal: `Create horror scenario: ${input}` }) },
  survival_blueprint: { endpoint: "/blueprint", payloadKey: "system_description" },
  curse_generator: { endpoint: "/strategy", payloadKey: "goal", transform: (input) => ({ goal: `Design curse: ${input}` }) },
  
  // Southern
  sl_blueprint: { endpoint: "/blueprint", payloadKey: "system_description" },
  sl_persona: { endpoint: "/persona", payloadKey: "audience" },
  chrome_bloom: { endpoint: "/art-direction", payloadKey: "project" },
  bayou_tales: { endpoint: "/strategy", payloadKey: "goal" },
  
  // Cyberpunk
  augment_engine: { endpoint: "/blueprint", payloadKey: "system_description" },
  hack_engine: { endpoint: "/strategy", payloadKey: "goal" },
  neon_blueprint: { endpoint: "/blueprint", payloadKey: "system_description" },
  corp_builder: { endpoint: "/persona", payloadKey: "audience" },
  
  // Fantasy
  quest_forge: { endpoint: "/strategy", payloadKey: "goal" },
  spell_weaver: { endpoint: "/blueprint", payloadKey: "system_description" },
  realm_builder: { endpoint: "/blueprint", payloadKey: "system_description" },
  creature_codex: { endpoint: "/persona", payloadKey: "audience" },
  
  // Romance
  meet_cute: { endpoint: "/strategy", payloadKey: "goal" },
  tension_engine: { endpoint: "/strategy", payloadKey: "goal" },
  arc_weaver: { endpoint: "/plan", payloadKey: "goal" },
  dialogue_spark: { endpoint: "/strategy", payloadKey: "goal" },
  
  // Urban
  street_tales: { endpoint: "/strategy", payloadKey: "goal" },
  hood_builder: { endpoint: "/blueprint", payloadKey: "system_description" },
  hustle_engine: { endpoint: "/strategy", payloadKey: "goal" },
  crew_forge: { endpoint: "/persona", payloadKey: "audience" },
  
  // Mythic
  pantheon_forge: { endpoint: "/blueprint", payloadKey: "system_description" },
  hero_engine: { endpoint: "/persona", payloadKey: "audience" },
  prophecy_weaver: { endpoint: "/strategy", payloadKey: "goal" },
  artifact_smith: { endpoint: "/blueprint", payloadKey: "system_description" }
};

const SAMPLE_INPUTS = {
  character_engine: "A mysterious transfer student with hidden powers",
  lore_engine: "A world where dreams become physical reality",
  episode_engine: "A tournament arc with high stakes",
  art_direction: "Dark fantasy anime with painterly backgrounds",
  monster_builder: "A creature that feeds on memories",
  fear_engine: "Abandoned hospital with something in the basement",
  survival_blueprint: "Escape from a haunted mansion",
  curse_generator: "A curse that makes you forget loved ones",
  sl_blueprint: "Small town with dark secrets",
  sl_persona: "Mysterious bayou fortune teller",
  chrome_bloom: "Decaying plantation at twilight",
  bayou_tales: "What lurks in the swamp",
  augment_engine: "Neural interface for hacking",
  hack_engine: "Breaking into a megacorp database",
  neon_blueprint: "Underground nightclub district",
  corp_builder: "Biotech corporation with dark agenda",
  quest_forge: "Retrieve the stolen crown",
  spell_weaver: "Magic system based on emotions",
  realm_builder: "Floating island kingdom",
  creature_codex: "Guardian spirit of the forest",
  meet_cute: "Two rivals stuck in an elevator",
  tension_engine: "Forbidden romance between rival families",
  arc_weaver: "Enemies to lovers journey",
  dialogue_spark: "Confession scene in the rain",
  street_tales: "Coming up from nothing",
  hood_builder: "Gentrifying neighborhood",
  hustle_engine: "From corner to boardroom",
  crew_forge: "Loyal squad of five",
  pantheon_forge: "Gods of a dying world",
  hero_engine: "Demigod seeking their place",
  prophecy_weaver: "The chosen one prophecy",
  artifact_smith: "Sword that grants wishes"
};

const MachineModal = ({ machine, canon, onClose }) => {
  const { tokens, spendTokens, checkJackpot, saveSession } = useArcade();
  const [input, setInput] = useState(SAMPLE_INPUTS[machine.id] || "");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [jackpot, setJackpot] = useState(null);

  const canAfford = tokens >= machine.cost;

  const runMachine = async () => {
    if (!canAfford || !input.trim()) return;
    
    // Spend tokens
    if (!spendTokens(machine.cost)) {
      setError("Insufficient tokens!");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setJackpot(null);

    const startTime = Date.now();

    try {
      const machineConfig = MACHINE_ENDPOINTS[machine.id];
      if (!machineConfig) {
        throw new Error("Machine not configured");
      }

      let payload;
      if (machineConfig.transform) {
        payload = machineConfig.transform(input, canon.name);
      } else {
        payload = { [machineConfig.payloadKey]: input };
      }
      
      // Add canon context and model
      payload.model = "gemini-3-flash";
      payload.context = `Canon: ${canon.name}. Style: ${canon.description}`;

      const response = await axios.post(
        `${API}${machineConfig.endpoint}`,
        payload,
        { timeout: 120000 }
      );

      const duration = Date.now() - startTime;
      setResult(response.data);

      // Check for jackpot
      const jackpotResult = checkJackpot(response.data);
      if (jackpotResult) {
        setJackpot(jackpotResult);
      }

      // Save session
      saveSession({
        id: `${machine.id}_${Date.now()}`,
        machine: machine.name,
        machineId: machine.id,
        canon: canon.id,
        input,
        output: response.data,
        cost: machine.cost,
        duration,
        jackpot: jackpotResult,
        timestamp: new Date().toISOString()
      });

    } catch (e) {
      setError(e.response?.data?.detail || e.message || "Machine malfunction!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="machine-modal-overlay" onClick={onClose} data-testid="machine-modal">
      <div 
        className="machine-modal" 
        onClick={e => e.stopPropagation()}
        style={{
          '--canon-primary': canon.colors.primary,
          '--canon-neon': canon.colors.neon
        }}
      >
        {/* Jackpot Animation */}
        {jackpot && (
          <div className="jackpot-animation" data-testid="jackpot-win">
            <div className="jackpot-burst"></div>
            <div className="jackpot-content">
              <span className="jackpot-star">⭐</span>
              <h2>JACKPOT!</h2>
              <p className="jackpot-type">{jackpot.name}</p>
              <p className="jackpot-amount">+{jackpot.amount.toLocaleString()} 🪙</p>
            </div>
          </div>
        )}

        <div className="modal-header">
          <div className="modal-machine-info">
            <span className="modal-machine-icon">{machine.icon}</span>
            <div>
              <h2>{machine.name}</h2>
              <span className="modal-canon-badge">{canon.icon} {canon.name}</span>
            </div>
          </div>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          <p className="machine-description">{machine.desc}</p>
          
          <div className="machine-stats-row">
            <div className="machine-stat">
              <span className="stat-label">Cost</span>
              <span className="stat-value">🪙 {machine.cost}</span>
            </div>
            <div className="machine-stat">
              <span className="stat-label">Difficulty</span>
              <span className="stat-value">{machine.difficulty}</span>
            </div>
            <div className="machine-stat">
              <span className="stat-label">Your Tokens</span>
              <span className={`stat-value ${!canAfford ? 'insufficient' : ''}`}>
                🪙 {tokens.toLocaleString()}
              </span>
            </div>
          </div>

          {!result && (
            <>
              <div className="input-section">
                <label>Input Prompt</label>
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Enter your creative prompt..."
                  rows={4}
                  disabled={loading}
                  data-testid="machine-input"
                />
              </div>

              <button
                className={`start-run-btn ${loading ? 'loading' : ''} ${!canAfford ? 'disabled' : ''}`}
                onClick={runMachine}
                disabled={loading || !canAfford || !input.trim()}
                data-testid="start-run-btn"
              >
                {loading ? (
                  <>
                    <span className="run-spinner"></span>
                    GENERATING...
                  </>
                ) : !canAfford ? (
                  <>INSUFFICIENT TOKENS</>
                ) : (
                  <>
                    <span className="play-icon">▶</span>
                    START RUN (-{machine.cost} 🪙)
                  </>
                )}
              </button>
            </>
          )}

          {error && (
            <div className="machine-error" data-testid="machine-error">
              <span>⚠️</span> {error}
            </div>
          )}

          {result && (
            <div className="result-section" data-testid="machine-result">
              <div className="result-header">
                <h3>✨ Output Generated</h3>
                <button 
                  className="run-again-btn"
                  onClick={() => { setResult(null); setJackpot(null); }}
                >
                  Run Again
                </button>
              </div>
              <div className="result-panel">
                <pre>{JSON.stringify(result, null, 2)}</pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MachineModal;
