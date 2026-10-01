import React, { useState } from 'react';
import { useLanguage } from '../../i18n';
import {
  Sprout,
  CloudSun,
  TrendingUp,
  ShieldCheck,
  Send,
  Calendar,
  MapPin,
  Maximize2,
  Droplets,
  Layers,
  ArrowRight,
  CheckCircle,
  AlertCircle
} from 'lucide-react';

export default function FarmOverview({
  farmer,
  weatherData,
  marketData,
  recommendedActions = [],
  onTriggerAgentPrompt,
  onNavigateView,
  onConfirmAction
}) {
  const { t } = useLanguage();
  const [copilotQuery, setCopilotQuery] = useState('');

  // Determine time of day greeting
  const hour = new Date().getHours();
  const greetingText = hour < 12 ? t('goodMorning') : hour < 17 ? t('goodAfternoon') : t('goodEvening');
  const farmerName = farmer?.name || t('defaultFarmerName');
  const currentCrop = farmer?.current_crop || 'Paddy';
  const cropDisplay = t(`crops.${currentCrop.toLowerCase()}`) || currentCrop;
  const stageDisplay = farmer?.crop_stage || 'Tillering & Panicle Initiation (40-45 days)';
  const location = farmer?.district || farmer?.location || 'Vijayawada, Andhra Pradesh';
  const landArea = farmer?.land_area || `2.0 ${t('acres')}`;

  // Live weather parameters
  const temp = weatherData?.temperature_c ? `${Math.round(weatherData.temperature_c)}°C` : '31°C';
  const rainProb = weatherData?.rainfall_probability_pct !== undefined ? `${weatherData.rainfall_probability_pct}%` : '37%';
  const humidity = weatherData?.humidity_pct !== undefined ? `${weatherData.humidity_pct}%` : '54%';

  // Market parameters
  const modalPrice = marketData?.markets?.[0]?.modal_price_per_quintal || '2,340';

  // Crop Stage Timeline Steps
  const stages = [
    { id: 'seedling', label: t('stageSeedling'), completed: true },
    { id: 'tillering', label: t('stageTillering'), current: true },
    { id: 'panicle', label: t('stagePanicle'), upcoming: true },
    { id: 'flowering', label: t('stageFlowering'), upcoming: true },
    { id: 'harvest', label: t('stageHarvest'), upcoming: true }
  ];

  // Dynamic weekly plan chip label
  const weeklyPlanLabel = `${t('quickActionPlan')} (${cropDisplay})`;

  const handleCopilotSubmit = (e) => {
    e?.preventDefault();
    if (!copilotQuery.trim()) return;
    onTriggerAgentPrompt(copilotQuery);
    setCopilotQuery('');
  };

  return (
    <div className="dashboard-container">
      {/* 1. Top Greeting Banner */}
      <div className="overview-greeting-banner">
        <div>
          <h1 className="greeting-headline">
            {greetingText}, {farmerName} 👋
          </h1>
          <p className="greeting-subtext">
            {t('whatsHappeningToday')}
          </p>
        </div>
        <div className="greeting-time-badge">
          <Calendar size={14} />
          <span>{new Date().toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })}</span>
        </div>
      </div>

      {/* 2. 4 Major KPI Cards */}
      <div className="kpi-cards-grid">
        {/* Card 1: Current Crop */}
        <div className="kpi-card" onClick={() => onNavigateView('crops')} style={{ cursor: 'pointer' }}>
          <div className="kpi-top-row">
            <span className="kpi-label">{t('kpiCurrentCrop')}</span>
            <div className="kpi-icon-pill" style={{ background: 'var(--emerald-50)', color: 'var(--emerald-800)' }}>
              <Sprout size={18} />
            </div>
          </div>
          <div>
            <div className="kpi-val-primary">{cropDisplay}</div>
            <div className="kpi-val-sub">40 {t('daysUnit') || 'days'} • {farmer?.crop_variety || 'BPT-5204'}</div>
          </div>
          <div className="kpi-badge healthy">
            ✓ {t('stageTillering')}
          </div>
        </div>

        {/* Card 2: Weather */}
        <div className="kpi-card" onClick={() => onNavigateView('weather')} style={{ cursor: 'pointer' }}>
          <div className="kpi-top-row">
            <span className="kpi-label">{t('kpiWeather')}</span>
            <div className="kpi-icon-pill" style={{ background: 'var(--blue-50)', color: 'var(--blue-600)' }}>
              <CloudSun size={18} />
            </div>
          </div>
          <div>
            <div className="kpi-val-primary">{temp}</div>
            <div className="kpi-val-sub">{rainProb} {t('rainChance') || 'Rain Chance'} • {humidity} {t('humidity') || 'Humidity'}</div>
          </div>
          <div className="kpi-badge healthy">
            🌦 {t('sprayFavorable')}
          </div>
        </div>

        {/* Card 3: Mandi Market */}
        <div className="kpi-card" onClick={() => onNavigateView('market')} style={{ cursor: 'pointer' }}>
          <div className="kpi-top-row">
            <span className="kpi-label">{t('kpiMarket')}</span>
            <div className="kpi-icon-pill" style={{ background: 'var(--emerald-50)', color: 'var(--emerald-800)' }}>
              <TrendingUp size={18} />
            </div>
          </div>
          <div>
            <div className="kpi-val-primary">₹{modalPrice}</div>
            <div className="kpi-val-sub">{t('perQuintalAtMandi')}</div>
          </div>
          <div className="kpi-badge healthy">
            ▲ {t('marketHighDemand')}
          </div>
        </div>

        {/* Card 4: Farm Status */}
        <div className="kpi-card" onClick={() => onNavigateView('agent')} style={{ cursor: 'pointer' }}>
          <div className="kpi-top-row">
            <span className="kpi-label">{t('kpiFarmStatus')}</span>
            <div className="kpi-icon-pill" style={{ background: 'var(--amber-50)', color: 'var(--amber-500)' }}>
              <AlertCircle size={18} />
            </div>
          </div>
          <div>
            <div className="kpi-val-primary" style={{ fontSize: '20px' }}>{t('statusAttention')}</div>
            <div className="kpi-val-sub">{t('actionShortSummary')}</div>
          </div>
          <div className="kpi-badge amber">
            ⚡ 3 {t('actionsPending')}
          </div>
        </div>
      </div>

      {/* 3. YOUR FARM Status Section with Visual Crop-Stage Timeline */}
      <section className="farm-status-section">
        <div className="section-header-row">
          <h2 className="section-title">
            <Sprout size={20} color="var(--emerald-800)" />
            {t('yourFarm')}
          </h2>
          <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            {location}
          </span>
        </div>

        {/* Farm Metadata Chips */}
        <div className="farm-meta-chips-bar">
          <div className="meta-chip">
            <MapPin size={14} color="var(--emerald-700)" />
            <span>{t('districtField')}: <strong>{location}</strong></span>
          </div>
          <div className="meta-chip">
            <Maximize2 size={14} color="var(--emerald-700)" />
            <span>{t('landAreaField')}: <strong>{landArea}</strong></span>
          </div>
          <div className="meta-chip">
            <Droplets size={14} color="var(--emerald-700)" />
            <span>{t('irrigationTypeField')}: <strong>{t('irrigationCanal')}</strong></span>
          </div>
          <div className="meta-chip">
            <Layers size={14} color="var(--emerald-700)" />
            <span>{t('soilTypeField')}: <strong>{t('soilClayLoam')}</strong></span>
          </div>
        </div>

        {/* Visual Crop Stage Timeline */}
        <div style={{ marginTop: '16px' }}>
          <div style={{ fontSize: '12.5px', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '8px' }}>
            {t('cropStageTimeline')} ({cropDisplay} • 40 {t('daysUnit') || 'days'})
          </div>
          <div className="crop-stage-timeline">
            {stages.map((st, idx) => (
              <div
                key={st.id}
                className={`timeline-step ${st.completed ? 'completed' : ''} ${st.current ? 'current' : ''}`}
              >
                <div className="timeline-dot">
                  {st.completed ? '✓' : idx + 1}
                </div>
                <span className="timeline-label">{st.label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 4. Prominent AI Copilot Card */}
      <section className="copilot-card">
        <div className="copilot-header">
          <div className="copilot-badge">
            <Sprout size={16} />
            <span>{t('aiCopilotTitle')}</span>
          </div>
          <span style={{ fontSize: '12px', color: 'var(--emerald-800)', fontWeight: 600 }}>
            ⚡ {t('groundedTrust')}
          </span>
        </div>

        <h3 className="copilot-prompt-title">
          {t('aiCopilotPrompt')}
        </h3>

        {/* Quick Action Chips that call the REAL Agent */}
        <div className="copilot-chips-grid">
          <button
            className="copilot-action-chip"
            onClick={() => onTriggerAgentPrompt(t('farmPlanPrompt'))}
          >
            📋 {weeklyPlanLabel}
          </button>
          <button
            className="copilot-action-chip"
            onClick={() => onTriggerAgentPrompt(`Check current weather forecast and agricultural implications for ${location}`)}
          >
            {t('quickActionWeather')}
          </button>
          <button
            className="copilot-action-chip"
            onClick={() => onTriggerAgentPrompt(`What are the current mandi market prices and selling advisory for ${cropDisplay}?`)}
          >
            {t('quickActionMarket')}
          </button>
          <button
            className="copilot-action-chip"
            onClick={() => onTriggerAgentPrompt(`Provide pest and disease monitoring checklist for ${cropDisplay} at tillering stage`)}
          >
            {t('quickActionMyCrop')}
          </button>
          <button
            className="copilot-action-chip"
            onClick={() => onTriggerAgentPrompt(t('servicesPrompt'))}
          >
            {t('quickActionServices')}
          </button>
        </div>

        {/* Inline Prompt Input */}
        <form className="copilot-input-row" onSubmit={handleCopilotSubmit}>
          <input
            type="text"
            placeholder={t('askAgentPlaceholder')}
            value={copilotQuery}
            onChange={(e) => setCopilotQuery(e.target.value)}
          />
          <button type="submit" className="copilot-send-btn">
            <span>{t('send')}</span>
            <Send size={14} />
          </button>
        </form>
      </section>

      {/* 5. Recommended Actions / This Week's Action Plan */}
      <section>
        <div className="section-header-row">
          <h2 className="section-title">
            <CheckCircle size={20} color="var(--emerald-800)" />
            {t('recommendedActions')}
          </h2>
          <button
            className="btn-review-action"
            onClick={() => onNavigateView('agent')}
          >
            {t('navAgent')} <ArrowRight size={14} style={{ display: 'inline', verticalAlign: 'middle' }} />
          </button>
        </div>

        <div className="recommended-actions-grid">
          {/* Action 1 */}
          <div className="action-card">
            <div>
              <div className="action-card-header">
                <span className="action-priority-badge high">{t('priorityHigh')}</span>
                <span style={{ fontSize: '11.5px', color: 'var(--text-muted)' }}>{t('next24h')}</span>
              </div>
              <h4 className="action-card-title">
                {t('action1Title')}
              </h4>
              <p className="action-card-desc">
                {t('action1Desc')}
              </p>
              <div className="action-card-source">
                {t('action1Source')}
              </div>
            </div>
            <div className="action-card-buttons">
              <button
                className="btn-confirmAction btn-confirm-action"
                onClick={() => onConfirmAction?.('act-nutrient-001', true)}
              >
                ✓ {t('confirmAction')}
              </button>
              <button
                className="btn-review-action"
                onClick={() => onTriggerAgentPrompt(`Explain dosage and timing for Nitrogen + Potash top dressing on ${cropDisplay}`)}
              >
                {t('reviewAction')}
              </button>
            </div>
          </div>

          {/* Action 2 */}
          <div className="action-card">
            <div>
              <div className="action-card-header">
                <span className="action-priority-badge high">{t('priorityHigh')}</span>
                <span style={{ fontSize: '11.5px', color: 'var(--text-muted)' }}>{t('daily')}</span>
              </div>
              <h4 className="action-card-title">
                {t('action2Title')}
              </h4>
              <p className="action-card-desc">
                {t('action2Desc')}
              </p>
              <div className="action-card-source">
                {t('action2Source')}
              </div>
            </div>
            <div className="action-card-buttons">
              <button
                className="btn-confirmAction btn-confirm-action"
                onClick={() => onConfirmAction?.('act-water-002', true)}
              >
                ✓ {t('confirmAction')}
              </button>
              <button
                className="btn-review-action"
                onClick={() => onTriggerAgentPrompt(`How to practice Alternate Wetting and Drying AWD water management for ${cropDisplay}?`)}
              >
                {t('reviewAction')}
              </button>
            </div>
          </div>

          {/* Action 3 */}
          <div className="action-card">
            <div>
              <div className="action-card-header">
                <span className="action-priority-badge medium">{t('priorityMedium')}</span>
                <span style={{ fontSize: '11.5px', color: 'var(--text-muted)' }}>{t('weekend')}</span>
              </div>
              <h4 className="action-card-title">
                {t('action3Title')}
              </h4>
              <p className="action-card-desc">
                {t('action3Desc')}
              </p>
              <div className="action-card-source">
                {t('action3Source')}
              </div>
            </div>
            <div className="action-card-buttons">
              <button
                className="btn-confirmAction btn-confirm-action"
                onClick={() => onConfirmAction?.('act-ipm-003', true)}
              >
                ✓ {t('confirmAction')}
              </button>
              <button
                className="btn-review-action"
                onClick={() => onTriggerAgentPrompt(`What are the ETL thresholds and symptoms for Stem Borer in ${cropDisplay}?`)}
              >
                {t('reviewAction')}
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
