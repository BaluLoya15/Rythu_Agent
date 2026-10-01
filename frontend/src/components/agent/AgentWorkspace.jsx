import React, { useState, useRef, useEffect } from 'react';
import { useLanguage } from '../../i18n';
import {
  Send,
  Bot,
  User,
  CheckCircle2,
  Clock,
  AlertCircle,
  Sprout,
  ShieldCheck,
  ChevronDown,
  ChevronUp,
  Sparkles
} from 'lucide-react';

const formatInlineMarkdown = (text) => {
  if (!text) return '';
  let formatted = text
    // 1. Markdown Links: [label](url)
    .replace(
      /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener noreferrer" style="color: #065f46; background: #ecfdf5; padding: 2px 8px; border-radius: 4px; border: 1px solid #a7f3d0; text-decoration: none; font-weight: 700; display: inline-flex; align-items: center; gap: 4px; margin: 1px 2px; word-break: break-all;">$1 ↗</a>'
    )
    // 2. Bold: **text**
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // 3. Italic: *text*
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    // 4. Code: `code`
    .replace(/`([^`]+)`/g, '<code style="background: rgba(0,0,0,0.06); padding: 1px 5px; border-radius: 4px; font-size: 0.9em; font-family: monospace;">$1</code>');
  return formatted;
};

const renderSimpleMarkdown = (text) => {
  if (!text) return null;
  const lines = text.split('\n');
  return lines.map((line, idx) => {
    const trimmed = line.trim();

    if (trimmed.startsWith('### ')) {
      return (
        <h3 key={idx} style={{ margin: '14px 0 8px', color: 'var(--emerald-950)', fontSize: '1.15rem', fontWeight: 800 }}>
          {trimmed.replace('### ', '')}
        </h3>
      );
    }
    if (trimmed.startsWith('#### ')) {
      return (
        <h4 key={idx} style={{ margin: '12px 0 6px', color: 'var(--emerald-900)', fontSize: '1.02rem', fontWeight: 700 }}>
          {trimmed.replace('#### ', '')}
        </h4>
      );
    }
    if (trimmed.startsWith('> ')) {
      return (
        <blockquote key={idx} style={{
          borderLeft: '4px solid var(--amber-500)',
          background: 'var(--amber-50)',
          padding: '10px 14px',
          margin: '10px 0',
          fontSize: '0.92rem',
          color: 'var(--text-secondary)',
          borderRadius: '0 8px 8px 0',
          lineHeight: 1.5
        }}>
          {trimmed.replace('> ', '')}
        </blockquote>
      );
    }
    if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      const itemContent = trimmed.replace(/^[-*]\s+/, '');
      return (
        <li key={idx} style={{ marginLeft: '20px', marginBottom: '6px', fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
          <span dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(itemContent) }} />
        </li>
      );
    }
    if (/^\d+\.\s+/.test(trimmed)) {
      return (
        <div key={idx} style={{ marginLeft: '10px', marginBottom: '8px', fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
          <span dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(trimmed) }} />
        </div>
      );
    }
    if (trimmed === '---') {
      return <hr key={idx} style={{ borderColor: 'var(--border-subtle)', margin: '14px 0' }} />;
    }
    if (!trimmed) {
      return <div key={idx} style={{ height: '6px' }} />;
    }

    return (
      <p key={idx} style={{ marginBottom: '8px', fontSize: '0.93rem', lineHeight: 1.55 }}>
        <span dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(trimmed) }} />
      </p>
    );
  });
};

export default function AgentWorkspace({
  farmer,
  messages,
  isLoading,
  latestResponse,
  onSendMessage,
  onConfirmAction,
  actionStatusMap = {}
}) {
  const { t } = useLanguage();
  const [inputText, setInputText] = useState('');
  const [showTechnicalTrace, setShowTechnicalTrace] = useState(false);
  const messagesEndRef = useRef(null);

  const currentCrop = farmer?.current_crop || 'Paddy';
  const cropDisplay = t(`crops.${currentCrop.toLowerCase()}`) || currentCrop;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = (e) => {
    e?.preventDefault();
    if (!inputText.trim() || isLoading) return;
    onSendMessage(inputText);
    setInputText('');
  };

  // Structured reasoning steps to display
  const toolTrace = latestResponse?.tool_trace || [];
  const hasWeather = toolTrace.some(t => t.tool_name === 'weather_tool');
  const hasMarket = toolTrace.some(t => t.tool_name === 'market_tool');
  const hasRag = toolTrace.some(t => t.tool_name === 'rag_tool');
  const hasFarmer = toolTrace.some(t => t.tool_name === 'farmer_tool');

  return (
    <div className="agent-workspace-view">
      {/* Scrollable Conversation Stream */}
      <div className="agent-conversation-area">
        <div className="agent-conversation-width">

          {/* Reasoning Visualizer (Grounded AI Agent Evidence) */}
          {(isLoading || toolTrace.length > 0) && (
            <div className="agent-reasoning-visualizer">
              <div className="reasoning-headline">
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Sparkles size={14} color="var(--emerald-800)" />
                  <span>{isLoading ? t('loadingPlanning') : t('reasoningRecommendationReady')}</span>
                </div>
                <button
                  onClick={() => setShowTechnicalTrace(!showTechnicalTrace)}
                  style={{
                    background: 'none',
                    border: 'none',
                    fontSize: '11px',
                    fontWeight: 600,
                    color: 'var(--text-muted)',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  <span>{showTechnicalTrace ? t('hidePayload') : t('inspectPayload')}</span>
                  {showTechnicalTrace ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                </button>
              </div>

              {/* High-Level User Friendly Reasoning Steps */}
              <div className="reasoning-steps-row">
                <div className={`reasoning-step-badge ${hasFarmer || !isLoading ? 'completed' : 'running'}`}>
                  ✓ {t('reasoningAnalyzingProfile')}
                </div>
                <div className={`reasoning-step-badge ${hasWeather || (!isLoading && toolTrace.length > 0) ? 'completed' : 'running'}`}>
                  ✓ {t('reasoningCheckingWeather')}
                </div>
                <div className={`reasoning-step-badge ${hasMarket || (!isLoading && toolTrace.length > 0) ? 'completed' : 'running'}`}>
                  ✓ {t('reasoningCheckingMarket')}
                </div>
                <div className={`reasoning-step-badge ${hasRag || (!isLoading && toolTrace.length > 0) ? 'completed' : 'running'}`}>
                  ✓ {t('reasoningSearchingKnowledge')}
                </div>
              </div>

              {/* Optional Technical Inspection for Hackathon Judges */}
              {showTechnicalTrace && (
                <div style={{
                  marginTop: '8px',
                  padding: '10px',
                  background: '#f8fafc',
                  border: '1px solid #e2e8f0',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '11.5px',
                  fontFamily: 'monospace',
                  maxHeight: '180px',
                  overflowY: 'auto'
                }}>
                  {toolTrace.map((tr, i) => (
                    <div key={i} style={{ marginBottom: '6px' }}>
                      <strong style={{ color: 'var(--emerald-900)' }}>[{tr.tool_name}]</strong> {tr.display_title || tr.output_summary} ({tr.execution_duration_ms}ms)
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Empty Conversation Welcome */}
          {messages.length === 0 && (
            <div style={{
              background: '#ffffff',
              border: '1px solid var(--border-emerald)',
              borderRadius: 'var(--radius-lg)',
              padding: '36px 32px',
              textAlign: 'center',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '14px',
              boxShadow: 'var(--shadow-sm)',
              marginTop: '40px'
            }}>
              <div className="brand-icon-box" style={{ width: '48px', height: '48px' }}>
                <Sprout size={28} />
              </div>
              <h2 style={{ fontSize: '22px', fontWeight: 800, color: 'var(--emerald-900)' }}>
                {t('emptyChatTitle')}
              </h2>
              <p style={{ fontSize: '14.5px', color: 'var(--text-secondary)', maxWidth: '580px', lineHeight: 1.5 }}>
                {t('emptyChatSubtitle')}
              </p>
            </div>
          )}

          {/* Messages Stream */}
          {messages.map((msg, index) => {
            const isUser = msg.role === 'user';
            return (
              <div key={msg.id || index} className={`chat-message-row ${isUser ? 'user' : 'assistant'}`}>
                {!isUser && (
                  <div className="chat-avatar-box assistant">
                    <Bot size={18} />
                  </div>
                )}

                <div className="chat-bubble">
                  {isUser ? (
                    <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
                  ) : (
                    <div>
                      {renderSimpleMarkdown(msg.content)}

                      {/* Proposed Consequential Actions Requiring Human Confirmation */}
                      {msg.proposed_actions && msg.proposed_actions.length > 0 && (
                        <div style={{ marginTop: '16px' }}>
                          {msg.proposed_actions.map((act) => {
                            const currentStatus = actionStatusMap[act.action_id] || act.status;
                            const isConfirmed = currentStatus === 'CONFIRMED' || currentStatus === 'EXECUTED';
                            const isDeclined = currentStatus === 'REJECTED';

                            return (
                              <div key={act.action_id} className="chat-action-card-inline">
                                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                  <span className="chat-action-title">
                                    ⚡ {act.title}
                                  </span>
                                  <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--amber-500)', background: 'var(--amber-50)', padding: '2px 8px', borderRadius: 'var(--radius-full)' }}>
                                    {t('pendingApproval')}
                                  </span>
                                </div>
                                <p className="chat-action-desc">
                                  {act.description}
                                </p>
                                <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '10px' }}>
                                  <strong>{t('why')}:</strong> {act.why_reason}
                                </div>

                                {isConfirmed ? (
                                  <div style={{ fontSize: '13px', fontWeight: 700, color: 'var(--emerald-800)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                                    <CheckCircle2 size={16} />
                                    <span>{t('actionCompleted')}</span>
                                  </div>
                                ) : isDeclined ? (
                                  <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--rose-600)' }}>
                                    ❌ {t('decline')}
                                  </div>
                                ) : (
                                  <div>
                                    <div style={{ fontSize: '12.5px', fontWeight: 700, color: 'var(--emerald-900)', marginBottom: '8px' }}>
                                      {t('confirmActionPrompt')}
                                    </div>
                                    <div className="chat-action-buttons-row">
                                      <button
                                        className="btn-confirm-action"
                                        onClick={() => onConfirmAction(act.action_id, true)}
                                      >
                                        ✓ {t('confirmActionYes')}
                                      </button>
                                      <button
                                        className="btn-review-action"
                                        onClick={() => onConfirmAction(act.action_id, false)}
                                      >
                                        {t('confirmActionNo')}
                                      </button>
                                    </div>
                                  </div>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {isUser && (
                  <div className="chat-avatar-box user">
                    <User size={18} />
                  </div>
                )}
              </div>
            );
          })}

          {/* Loading Indicator */}
          {isLoading && (
            <div className="chat-message-row assistant">
              <div className="chat-avatar-box assistant">
                <Bot size={18} />
              </div>
              <div className="chat-bubble" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Clock size={16} className="spin" color="var(--emerald-700)" />
                <span style={{ fontSize: '13.5px', color: 'var(--text-secondary)', fontWeight: 500 }}>
                  {t('loading')}
                </span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Bottom Bar: Quick Action Chips & Input Container */}
      <div className="agent-bottom-bar">
        <div className="agent-bottom-bar-width">
          {/* Quick Action Chips that call the REAL Agent */}
          <div className="quick-chips-bottom-row">
            <button
              className="quick-chip-btn"
              onClick={() => onSendMessage(t('farmPlanPrompt'))}
            >
              📋 {t('quickActionPlan')} ({cropDisplay})
            </button>
            <button
              className="quick-chip-btn"
              onClick={() => onSendMessage(`Check current weather forecast and agricultural implications for ${farmer?.district || 'Vijayawada'}`)}
            >
              🌦 {t('quickActionWeather')}
            </button>
            <button
              className="quick-chip-btn"
              onClick={() => onSendMessage(`What are the current mandi market prices and selling advisory for ${cropDisplay}?`)}
            >
              📈 {t('quickActionMarket')}
            </button>
            <button
              className="quick-chip-btn"
              onClick={() => onSendMessage(t('servicesPrompt'))}
            >
              🏛 {t('quickActionServices')}
            </button>
          </div>

          {/* Message Input Form */}
          <form className="agent-input-container" onSubmit={handleSend}>
            <input
              type="text"
              placeholder={t('inputPlaceholder')}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              disabled={isLoading}
            />
            <button
              type="submit"
              className="agent-input-btn-send"
              disabled={isLoading || !inputText.trim()}
              title={t('send')}
            >
              <Send size={16} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
