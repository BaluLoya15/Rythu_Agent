import React, { useState } from 'react';
import {
  CheckCircle2, Clock, Code, User, TrendingUp,
  CloudSun, BookOpen, Landmark, Brain, ShieldCheck
} from 'lucide-react';
import { useLanguage } from '../i18n';

export default function AgentTracePanel({ toolTrace = [], taskPlan = [], intent, isRunning }) {
  const [expandedTrace, setExpandedTrace] = useState({});
  const { t } = useLanguage();

  const toggleExpand = (stepId) => {
    setExpandedTrace((prev) => ({ ...prev, [stepId]: !prev[stepId] }));
  };

  const getToolIcon = (toolName) => {
    switch (toolName) {
      case 'farmer_tool':
        return <User size={16} />;
      case 'market_tool':
        return <TrendingUp size={16} />;
      case 'weather_tool':
        return <CloudSun size={16} />;
      case 'rag_tool':
        return <BookOpen size={16} />;
      case 'services_tool':
        return <Landmark size={16} />;
      case 'reasoning_engine':
        return <Brain size={16} />;
      default:
        return <CheckCircle2 size={16} />;
    }
  };

  const getStatusBadge = (status, dataStatus) => {
    if (status === 'FAILED' || dataStatus === 'UNAVAILABLE') {
      return (
        <span className="trace-status-pill unavailable">
          {t('unavailable')}
        </span>
      );
    }
    if (dataStatus === 'LIVE') {
      return (
        <span className="trace-status-pill live">
          ● {t('liveData')}
        </span>
      );
    }
    if (dataStatus === 'VERIFIED_RESEARCH' || dataStatus === 'VERIFIED_KNOWLEDGE') {
      return (
        <span className="trace-status-pill verified">
          {t('verifiedResearch')}
        </span>
      );
    }
    return (
      <span className="trace-status-pill local">
        {dataStatus || 'LOCAL'}
      </span>
    );
  };

  return (
    <div className="trace-panel-container">
      {/* Panel Top Title */}
      <div className="trace-top-header">
        <h4>
          <Brain size={18} color="#10b981" />
          <span>{t('navTimeline')}</span>
        </h4>
        {intent && (
          <div className="trace-intent-tag">
            Intent: {intent}
          </div>
        )}
      </div>

      {/* Task Plan Checklist */}
      {taskPlan && taskPlan.length > 0 && (
        <div className="task-plan-box">
          <div className="task-plan-title">
            📋 {t('dynamicTaskPlan')} {t('stepsCount', { count: taskPlan.length })}
          </div>
          <div className="task-plan-steps">
            {taskPlan.map((p) => (
              <div key={p.step_number} className="task-step-chip">
                <CheckCircle2 size={13} color="#10b981" />
                <span className="step-num">{t('step')} {p.step_number}:</span>
                <span className="step-name">{p.title}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Real Tool Traces */}
      {toolTrace && toolTrace.length > 0 ? (
        toolTrace.map((trace) => {
          const isExp = expandedTrace[trace.step_id];
          const localizedTitle = (trace.event_key && t(trace.event_key)) || trace.display_title;
          return (
            <div key={trace.step_id} className="trace-step-item">
              <div className={`trace-icon ${trace.status?.toLowerCase()}`}>
                {getToolIcon(trace.tool_name)}
              </div>
              <div className="trace-body">
                <div className="trace-header">
                  <h5>{localizedTitle}</h5>
                  <div className="trace-meta">
                    {getStatusBadge(trace.status, trace.data_status)}
                    <span className="duration-tag">
                      <Clock size={11} />
                      {trace.execution_duration_ms}ms
                    </span>
                    <span className="timestamp-tag">{trace.timestamp}</span>
                  </div>
                </div>
                <div className="trace-summary">{trace.output_summary}</div>

                {trace.raw_output && (
                  <div>
                    <button
                      className="trace-toggle-raw"
                      onClick={() => toggleExpand(trace.step_id)}
                    >
                      <Code size={11} style={{ display: 'inline', marginRight: '4px' }} />
                      {isExp ? t('hidePayload') : t('inspectPayload')}
                    </button>
                    {isExp && (
                      <pre className="trace-raw-viewer">
                        {JSON.stringify(trace.raw_output, null, 2)}
                      </pre>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })
      ) : (
        <div className="trace-empty">
          <Brain size={36} className="empty-icon" />
          <p style={{ fontWeight: 600, color: '#e2e8f0', marginBottom: '4px' }}>{t('noActivity')}</p>
          <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>{t('waitingPrompt')}</span>
        </div>
      )}
    </div>
  );
}
