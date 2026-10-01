import React from 'react';
import { TrendingUp, MapPin, ShieldAlert, CheckCircle2, Info } from 'lucide-react';
import { useLanguage } from '../i18n';

export default function MarketIntelView({ marketData }) {
  const { t, normalizeCropKey } = useLanguage();

  if (!marketData) {
    return (
      <div className="market-empty">
        <TrendingUp size={44} className="empty-icon" />
        <p>{t('noMarketData')}</p>
      </div>
    );
  }

  const cropKey = normalizeCropKey(marketData.crop);
  const localizedCrop = t(`crops.${cropKey}`) || marketData.crop;

  // Transparent Handling of Live Market Unavailability
  if (marketData.data_status === 'UNAVAILABLE' || !marketData.markets || marketData.markets.length === 0) {
    return (
      <div className="market-unavailable-container">
        <div className="market-unavailable-card">
          <div className="card-header">
            <ShieldAlert size={22} color="#f87171" />
            <h3>{t('liveDataUnavailable')}</h3>
          </div>
          <p className="card-desc">
            {marketData.recommended_strategy || t('liveDataUnavailable')}
          </p>
          <div className="provenance-notice">
            <strong>{t('provenance')}:</strong> {t('disclaimerText')}
          </div>
        </div>
      </div>
    );
  }

  // Live Market Data Display
  return (
    <div className="market-intel-container">
      {/* Header Strategy Banner */}
      <div className="market-header-banner">
        <div className="banner-top">
          <h3>
            <TrendingUp size={18} color="#10b981" />
            <span>{t('marketIntelligenceTitle')} ({localizedCrop})</span>
          </h3>
          <span className={`status-pill ${marketData.data_status.toLowerCase()}`}>
            {marketData.data_status === 'LIVE' ? `● ${t('liveData')}` : t('offlineStatus')}
          </span>
        </div>
        {marketData.recommended_strategy && (
          <p className="strategy-text">{marketData.recommended_strategy}</p>
        )}
      </div>

      {/* Mandi Comparison Table */}
      <div className="mandi-table-wrapper">
        <table className="mandi-table">
          <thead>
            <tr>
              <th>{t('marketName')}</th>
              <th>{t('district')}</th>
              <th>{t('modalPrice')}</th>
              <th>{t('transportCost')}</th>
              <th>{t('netRealization')}</th>
              <th>{t('date')}</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {marketData.markets.map((m, idx) => {
              const isBest = m.market_name === marketData.best_market;
              return (
                <tr key={idx} className={isBest ? 'best-mandi-row' : ''}>
                  <td>
                    <div className="mandi-name">
                      {m.market_name}
                      {isBest && <span className="best-badge">BEST NET</span>}
                    </div>
                    <div className="mandi-sub">{m.variety || localizedCrop}</div>
                  </td>
                  <td>
                    <div className="mandi-dist">
                      <MapPin size={12} />
                      <span>{m.district || m.distance_km + ' km'}</span>
                    </div>
                  </td>
                  <td className="price-cell">₹{m.modal_price_per_quintal?.toLocaleString()} / q</td>
                  <td className="transport-cell">-₹{m.estimated_transport_cost_per_quintal || 0}</td>
                  <td>
                    <div className="net-price">
                      ₹{m.net_effective_price_per_quintal?.toLocaleString() || m.modal_price_per_quintal?.toLocaleString()}
                    </div>
                  </td>
                  <td className="date-cell">{m.date || t('today')}</td>
                  <td>
                    <span className={`data-badge ${m.data_status === 'LIVE' ? 'live' : 'test'}`}>
                      {m.data_status === 'LIVE' ? t('liveData') : m.data_status}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="market-footer-info">
        <span><strong>{t('source')}:</strong> {marketData.source}</span>
        <span className="dot">•</span>
        <span><strong>{t('lastUpdated')}:</strong> {marketData.markets[0]?.date || t('today')}</span>
      </div>
    </div>
  );
}
