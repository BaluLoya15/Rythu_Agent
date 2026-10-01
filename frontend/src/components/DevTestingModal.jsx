import React from 'react';
import { X, Wrench, PlayCircle, ShieldCheck, Database, RefreshCw } from 'lucide-react';

export default function DevTestingModal({ isOpen, onClose, onRunScenario, forceDemo, setForceDemo }) {
  if (!isOpen) return null;

  const testSuites = [
    {
      id: 'sc-1',
      title: 'Test Scenario 1: Primary Cultivation & Market Query',
      query: 'I have 2 acres of tomato near Vijayawada. What should I do this week and where should I check for better market prices?'
    },
    {
      id: 'sc-2',
      title: 'Test Scenario 2: Welfare Schemes & Subsidies',
      query: 'What agricultural government services may be relevant to me?'
    },
    {
      id: 'sc-3',
      title: 'Test Scenario 3: Chilli Crop Diagnostic Query',
      query: 'My chilli plants have yellow leaves. What should I check?'
    },
    {
      id: 'sc-4',
      title: 'Test Scenario 4: Groundnut 40-Day Pegging Planning',
      query: 'My groundnut crop is 40 days old. What should I do now?'
    }
  ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '620px' }}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Wrench size={20} color="#f59e0b" />
            <h3 style={{ fontSize: '1.15rem' }}>Developer & Automated Testing Harness</h3>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'transparent', border: 'none', color: '#94a39b', cursor: 'pointer' }}
          >
            <X size={20} />
          </button>
        </div>

        <div style={{ fontSize: '0.82rem', color: '#94a39b', marginBottom: '16px', lineHeight: 1.5 }}>
          This testing panel is reserved for developers and hackathon judges to verify edge cases, mock fallback baselines, and test automated query pipelines.
        </div>

        {/* Development Baseline Toggle */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.03)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          borderRadius: '8px',
          padding: '12px 16px',
          marginBottom: '18px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div>
            <div style={{ fontSize: '0.86rem', fontWeight: 600, color: '#f3fbf6' }}>
              Test Baseline Archive Mode
            </div>
            <div style={{ fontSize: '0.74rem', color: '#94a39b' }}>
              When enabled, forces deterministic historical sample data for offline environments. (Default: OFF / Live First)
            </div>
          </div>
          <button
            className={`demo-toggle-btn ${forceDemo ? 'active' : ''}`}
            onClick={() => setForceDemo(!forceDemo)}
          >
            <Database size={14} />
            {forceDemo ? 'Test Mode Enabled' : 'Live Gateway Default'}
          </button>
        </div>

        {/* Automated Test Queries */}
        <div style={{ marginBottom: '14px' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#f3fbf6', marginBottom: '10px' }}>
            Automated Acceptance Test Queries:
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {testSuites.map((ts) => (
              <div
                key={ts.id}
                style={{
                  background: '#13221b',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                  borderRadius: '8px',
                  padding: '10px 14px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}
              >
                <div>
                  <div style={{ fontSize: '0.82rem', fontWeight: 600, color: '#f3fbf6' }}>{ts.title}</div>
                  <div style={{ fontSize: '0.74rem', color: '#94a39b' }}>"{ts.query}"</div>
                </div>
                <button
                  className="send-btn"
                  style={{ padding: '6px 12px', fontSize: '0.76rem' }}
                  onClick={() => {
                    onRunScenario(ts.query);
                    onClose();
                  }}
                >
                  <PlayCircle size={14} />
                  <span>Execute Query</span>
                </button>
              </div>
            ))}
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
          <button className="btn-decline" onClick={onClose}>
            Close Test Panel
          </button>
        </div>
      </div>
    </div>
  );
}
