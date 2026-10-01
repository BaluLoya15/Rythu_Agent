import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, CheckCircle2, XCircle, Mic, Sparkles } from 'lucide-react';
import { useLanguage } from '../i18n';

export default function ChatPanel({
  farmer,
  messages = [],
  onSendMessage,
  isLoading,
  onConfirmAction,
  actionStatusMap = {}
}) {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);

  const { t, getFarmPlanChip, getServicesChip } = useLanguage();

  // Determine if farmer has multi-crop
  const isMultiCrop = Array.isArray(farmer?.crops) && farmer.crops.length > 1;
  const currentCrop = farmer?.current_crop || (Array.isArray(farmer?.crops) ? farmer.crops[0] : 'Paddy');
  const farmPlanChipLabel = getFarmPlanChip(currentCrop, isMultiCrop);
  const servicesChipLabel = getServicesChip();

  const farmPlanPrompt = t('farmPlanPrompt');
  const servicesPrompt = t('servicesPrompt');

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;
    onSendMessage(inputText);
    setInputText('');
  };

  const handleSuggestionClick = (query) => {
    if (isLoading) return;
    onSendMessage(query);
  };

  const formatInlineMarkdown = (text) => {
    if (!text) return '';
    let formatted = text
      .replace(
        /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,
        '<a href="$2" target="_blank" rel="noopener noreferrer" style="color: #065f46; background: #ecfdf5; padding: 2px 8px; border-radius: 4px; border: 1px solid #a7f3d0; text-decoration: none; font-weight: 700; display: inline-flex; align-items: center; gap: 4px; margin: 1px 2px; word-break: break-all;">$1 ↗</a>'
      )
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`([^`]+)`/g, '<code style="background: rgba(255,255,255,0.1); padding: 1px 4px; border-radius: 4px; font-size: 0.85em;">$1</code>');
    return formatted;
  };

  const renderSimpleMarkdown = (text) => {
    if (!text) return null;
    const lines = text.split('\n');
    return lines.map((line, idx) => {
      let trimmed = line.trim();

      if (trimmed.startsWith('### ')) {
        return <h3 key={idx} style={{ margin: '10px 0 6px', color: '#10b981', fontSize: '1.02rem', fontWeight: 600 }}>{trimmed.replace('### ', '')}</h3>;
      }
      if (trimmed.startsWith('#### ')) {
        return <h4 key={idx} style={{ margin: '8px 0 4px', color: '#34d399', fontSize: '0.92rem', fontWeight: 600 }}>{trimmed.replace('#### ', '')}</h4>;
      }
      if (trimmed.startsWith('> ')) {
        return (
          <blockquote key={idx} style={{
            borderLeft: '3px solid #f59e0b',
            background: 'rgba(245, 158, 11, 0.08)',
            padding: '8px 12px',
            margin: '8px 0',
            fontSize: '0.82rem',
            color: '#fbbf24',
            borderRadius: '0 6px 6px 0'
          }}>
            {trimmed.replace('> ', '')}
          </blockquote>
        );
      }
      if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
        const itemContent = trimmed.replace(/^[-*]\s+/, '');
        return (
          <li key={idx} style={{ marginLeft: '16px', marginBottom: '4px', fontSize: '0.85rem' }}>
            <span dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(itemContent) }} />
          </li>
        );
      }
      if (/^\d+\.\s+/.test(trimmed)) {
        return (
          <div key={idx} style={{ marginLeft: '8px', marginBottom: '6px', fontSize: '0.85rem' }}>
            <span dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(trimmed) }} />
          </div>
        );
      }
      if (trimmed === '---') {
        return <hr key={idx} style={{ borderColor: 'rgba(255, 255, 255, 0.08)', margin: '10px 0' }} />;
      }
      if (!trimmed) {
        return <div key={idx} style={{ height: '4px' }} />;
      }

      return (
        <p key={idx} style={{ marginBottom: '6px', fontSize: '0.86rem' }}>
          <span dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(trimmed) }} />
        </p>
      );
    });
  };

  return (
    <div className="chat-panel">
      {/* Messages Scroll Area */}
      <div className="messages-container">
        {messages.length === 0 && (
          <div className="empty-chat-state">
            <div className="empty-icon-wrap">
              <Bot size={36} color="#10b981" />
            </div>
            <h2>{t('emptyChatTitle')}</h2>
            <p>{t('emptyChatSubtitle')}</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={msg.id || index} className={`message-row ${msg.role}`}>
            <div className={`message-avatar ${msg.role}`}>
              {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
            </div>

            <div className={`message-bubble ${msg.role}`}>
              <div className="message-content">
                {msg.role === 'assistant' ? renderSimpleMarkdown(msg.content) : msg.content}
              </div>

              {/* Consequential Action Cards Embedded in Assistant Response */}
              {msg.proposed_actions && msg.proposed_actions.length > 0 && (
                <div className="action-cards-container">
                  {msg.proposed_actions.map((act) => {
                    const status = actionStatusMap[act.action_id] || act.status || 'PENDING';
                    const isExecuted = status === 'EXECUTED';
                    const isRejected = status === 'REJECTED';

                    return (
                      <div key={act.action_id} className={`action-card ${status.toLowerCase()}`}>
                        <div className="action-card-header">
                          <span className="action-tag">{t('proposedAction')}</span>
                          <span className={`action-badge ${status.toLowerCase()}`}>
                            {isExecuted ? t('actionCompleted') : isRejected ? t('decline') : t('pendingApproval')}
                          </span>
                        </div>
                        <h4 className="action-title">{act.title}</h4>
                        <p className="action-desc">
                          <strong>{t('why')}:</strong> {act.description}
                        </p>

                        {/* Action Buttons */}
                        {isExecuted ? (
                          <div className="action-status-banner success">
                            <CheckCircle2 size={14} />
                            <span>{t('recordedInNotebook')}</span>
                          </div>
                        ) : isRejected ? (
                          <div className="action-status-banner rejected">
                            <XCircle size={14} />
                            <span>{t('decline')}</span>
                          </div>
                        ) : (
                          <div>
                            <div className="action-confirm-prompt" style={{ fontSize: '0.85rem', fontWeight: 600, color: '#34d399', margin: '8px 0 6px' }}>
                              {t('confirmActionPrompt')}
                            </div>
                            <div className="action-btn-group">
                              <button
                                className="btn-confirm"
                                onClick={() => onConfirmAction(act.action_id, true)}
                              >
                                <CheckCircle2 size={14} />
                                <span>{t('confirmActionYes')}</span>
                              </button>
                              <button
                                className="btn-decline"
                                onClick={() => onConfirmAction(act.action_id, false)}
                              >
                                <span>{t('confirmActionNo')}</span>
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
          </div>
        ))}

        {isLoading && (
          <div className="message-row agent">
            <div className="message-avatar agent">
              <Bot size={16} />
            </div>
            <div className="message-bubble agent" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Sparkles size={16} color="#10b981" />
              <span style={{ fontSize: '0.82rem', color: '#94a39b' }}>
                {t('loading')}
              </span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Contextual Quick Actions (Dynamic & Multilingual) */}
      <div className="quick-actions-bar">
        <span className="quick-actions-label">
          <Sparkles size={13} color="#10b981" />
          <span>{t('quickActionsLabel')}</span>
        </span>

        {/* Dynamic Farm Plan Chip */}
        <button
          id="quick-action-farm-plan"
          className="quick-chip-btn farm-plan"
          onClick={() => handleSuggestionClick(farmPlanPrompt)}
          disabled={isLoading}
          title={farmPlanPrompt}
        >
          {farmPlanChipLabel}
        </button>

        {/* Relevant Agricultural Services Chip */}
        <button
          id="quick-action-services"
          className="quick-chip-btn services"
          onClick={() => handleSuggestionClick(servicesPrompt)}
          disabled={isLoading}
          title={servicesPrompt}
        >
          {servicesChipLabel}
        </button>
      </div>

      {/* Message Input Bar */}
      <div className="chat-input-area">
        <form className="chat-form" onSubmit={handleSubmit}>
          <input
            id="farmer-message-input"
            type="text"
            className="chat-input"
            placeholder={t('inputPlaceholder')}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={isLoading}
          />
          <button
            type="button"
            className="demo-toggle-btn voice-btn"
            title={t('voiceInputTooltip')}
            aria-label="Voice input"
          >
            <Mic size={16} color="#64746d" />
          </button>
          <button
            id="chat-send-btn"
            type="submit"
            className="send-btn"
            disabled={isLoading || !inputText.trim()}
          >
            <Send size={15} />
            <span>{t('send')}</span>
          </button>
        </form>
      </div>
    </div>
  );
}
