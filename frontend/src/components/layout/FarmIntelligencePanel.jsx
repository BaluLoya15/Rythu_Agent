import React from 'react';
import { useLanguage } from '../../i18n';
import {
  Sprout,
  CloudSun,
  TrendingUp,
  Clock
} from 'lucide-react';

export default function FarmIntelligencePanel({
  farmer,
  weatherData,
  marketData,
  activeActionsCount = 0,
  onNavigateView
}) {
  const { t } = useLanguage();

  const currentCrop = farmer?.current_crop || 'Paddy';
  const cropDisplay = t(`crops.${currentCrop.toLowerCase()}`) || currentCrop;
  const stageDisplay = farmer?.crop_stage || 'Tillering (40 days)';
  const location = farmer?.district || farmer?.location || 'Vijayawada, AP';

  // Live weather parameters
  const temp = weatherData?.temperature_c ? `${Math.round(weatherData.temperature_c)}°C` : '31°C';
  const rainProb = weatherData?.rainfall_probability_pct !== undefined ? `${weatherData.rainfall_probability_pct}%` : '37%';
  const humidity = weatherData?.humidity_pct !== undefined ? `${weatherData.humidity_pct}%` : '54%';
  const sprayAdvice = t('sprayWindowStatus');

  // Market parameters
  const modalPrice = marketData?.markets?.[0]?.modal_price_per_quintal || '2,340';
  const bestMandi = marketData?.best_market || 'Vijayawada AMCO Market';

  return (
    <aside className="farm-intelligence-panel">
      {/* Header with live pulse */}
      <div className="intel-panel-header">
        <span className="intel-panel-title">
          <span className="live-pulse-dot" />
          {t('farmToday')}
        </span>
        <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
          {new Date().toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
        </span>
      </div>

      {/* Widget 1: Current Crop Status */}
      <div className="intel-widget-card" style={{ cursor: 'pointer' }} onClick={() => onNavigateView?.('crops')}>
        <div className="widget-title-row">
          <span>{t('kpiCurrentCrop')}</span>
          <Sprout size={15} color="var(--emerald-700)" />
        </div>
        <div className="widget-main-value">
          🌾 {cropDisplay}
        </div>
        <div className="widget-sub-info">
          <strong>40 {t('daysUnit') || 'days'}</strong> • {stageDisplay}
        </div>
        <div style={{ fontSize: '11.5px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
          <span>{farmer?.crop_variety || 'BPT-5204'}</span> • <span>{farmer?.land_area || `2.0 ${t('acres')}`}</span>
        </div>
      </div>

      {/* Widget 2: Live Weather */}
      <div className="intel-widget-card" style={{ cursor: 'pointer' }} onClick={() => onNavigateView?.('weather')}>
        <div className="widget-title-row">
          <span>{t('kpiWeather')}</span>
          <CloudSun size={15} color="var(--emerald-700)" />
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
          <span className="widget-main-value">{temp}</span>
          <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>{t('rain') || 'Rain'}: <strong>{rainProb}</strong></span>
        </div>
        <div className="widget-sub-info">
          {t('humidity') || 'Humidity'}: <strong>{humidity}</strong> • {location}
        </div>
        <div style={{
          fontSize: '11px',
          fontWeight: 600,
          color: 'var(--emerald-800)',
          background: 'var(--emerald-50)',
          padding: '4px 8px',
          borderRadius: 'var(--radius-sm)',
          border: '1px solid var(--border-emerald)'
        }}>
          🌦 {sprayAdvice}
        </div>
      </div>

      {/* Widget 3: Mandi Market Status */}
      <div className="intel-widget-card" style={{ cursor: 'pointer' }} onClick={() => onNavigateView?.('market')}>
        <div className="widget-title-row">
          <span>{t('kpiMarket')}</span>
          <TrendingUp size={15} color="var(--emerald-700)" />
        </div>
        <div className="widget-main-value">
          ₹{modalPrice} <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>/ {t('unit') || 'quintal'}</span>
        </div>
        <div className="widget-sub-info">
          {bestMandi}
        </div>
        <div style={{ fontSize: '11px', color: 'var(--emerald-700)', fontWeight: 600 }}>
          ▲ {t('mandiModalFavorable')}
        </div>
      </div>

      {/* Widget 4: Active Recommendations Counter */}
      <div className="intel-widget-card" style={{ cursor: 'pointer' }} onClick={() => onNavigateView?.('agent')}>
        <div className="widget-title-row">
          <span>{t('activeAdvisories')}</span>
          <Clock size={15} color="var(--emerald-700)" />
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{
            fontSize: '16px',
            fontWeight: 800,
            color: 'var(--emerald-900)'
          }}>
            ⚡ {activeActionsCount > 0 ? activeActionsCount : 3} {t('recommendedActions')}
          </span>
        </div>
        <div className="widget-sub-info">
          {t('statusAttention')} • {t('activeAdvisoriesSub')}
        </div>
      </div>
    </aside>
  );
}
