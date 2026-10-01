import React from 'react';
import {
  Sprout, TrendingUp, CloudSun, AlertTriangle,
  CheckCircle, Calendar, BookOpen, Clock, ShieldCheck, Info
} from 'lucide-react';
import { useLanguage } from '../i18n';

export default function ActionPlanView({ actionPlan, marketData, weatherData }) {
  const { t, normalizeCropKey } = useLanguage();

  if (!actionPlan) {
    return (
      <div className="action-plan-empty">
        <Sprout size={48} className="empty-icon" />
        <h4>{t('noPlanYet')}</h4>
        <p>{t('askForPlanTip')}</p>
      </div>
    );
  }

  const isMarketUnavailable = !marketData || marketData.data_status === 'UNAVAILABLE' || marketData.markets?.length === 0;
  const cropKey = normalizeCropKey(actionPlan.crop);
  const localizedCrop = t(`crops.${cropKey}`) || actionPlan.crop;

  return (
    <div className="action-plan-grid">
      {/* Top Header Card */}
      <div className="action-header-card">
        <div>
          <div className="plan-title-row">
            <Sprout size={22} color="#10b981" />
            <h3>{t('navActionPlan')}</h3>
          </div>
          <div className="plan-badges">
            <span className="plan-badge">🌱 {t('crop')}: <strong>{localizedCrop}</strong></span>
            <span className="plan-badge">📍 {actionPlan.location}</span>
            <span className="plan-badge">⏳ {t('cropStage')}: <strong>{actionPlan.stage}</strong></span>
            {actionPlan.generated_at && (
              <span className="plan-badge timestamp">{actionPlan.generated_at}</span>
            )}
          </div>
        </div>
      </div>

      {/* Market & Weather Twin Cards */}
      <div className="plan-summary-grid">
        <div className="summary-card">
          <h4>
            <TrendingUp size={16} />
            <span>{t('market')}</span>
          </h4>
          <p>{actionPlan.market_summary}</p>
          {isMarketUnavailable && (
            <div className="unavailable-notice">
              <Info size={12} />
              <span>{t('liveDataUnavailable')}</span>
            </div>
          )}
        </div>

        <div className="summary-card">
          <h4>
            <CloudSun size={16} />
            <span>{t('weather')}</span>
          </h4>
          <p>{actionPlan.weather_summary}</p>
        </div>
      </div>

      {/* Critical Considerations & Field Risks */}
      {actionPlan.critical_considerations && actionPlan.critical_considerations.length > 0 && (
        <div className="summary-card warning-card">
          <h4>
            <AlertTriangle size={16} />
            <span>{t('importantNotes')}</span>
          </h4>
          <ul>
            {actionPlan.critical_considerations.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommended Action Checklist */}
      {actionPlan.recommended_actions && actionPlan.recommended_actions.length > 0 && (
        <div className="checklist-section">
          <h4>
            <CheckCircle size={18} color="#10b981" />
            <span>{t('recommendedActions')}</span>
          </h4>
          <div className="checklist-container">
            {actionPlan.recommended_actions.map((act) => {
              const priorityText = act.priority === 'HIGH' ? t('priorityHigh') :
                                   act.priority === 'MEDIUM' ? t('priorityMedium') : t('priorityLow');
              return (
                <div key={act.step} className="action-item-card">
                  <div className="step-num-badge">{act.step}</div>
                  <div className="action-details">
                    <div className="action-title-row">
                      <h5>{act.title}</h5>
                      <span className={`priority-tag ${act.priority || 'standard'}`}>{priorityText}</span>
                    </div>
                    <div className="action-desc">{act.detail}</div>
                    {act.timeline && (
                      <div className="action-timeline">
                        <Clock size={13} />
                        <span>{act.timeline}</span>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Next Monitoring & Follow-Up Tasks */}
      {actionPlan.monitoring_tasks && actionPlan.monitoring_tasks.length > 0 && (
        <div className="summary-card">
          <h4>
            <Calendar size={16} />
            <span>{t('nextSteps')}</span>
          </h4>
          <ul>
            {actionPlan.monitoring_tasks.map((task, idx) => (
              <li key={idx}>{task}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Authoritative Sources */}
      {actionPlan.sources_cited && actionPlan.sources_cited.length > 0 && (
        <div className="summary-card sources-card">
          <h4>
            <BookOpen size={16} />
            <span>{t('sources')}</span>
          </h4>
          <div className="sources-list">
            {actionPlan.sources_cited.map((src, idx) => (
              <div key={idx} className="source-item">
                <ShieldCheck size={14} color="#10b981" />
                <span>{src}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
