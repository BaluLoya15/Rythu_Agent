import React, { useState, useEffect } from 'react';
import { useLanguage } from '../../i18n';
import { getMarketPrices } from '../../api/client';
import {
  TrendingUp,
  MapPin,
  Calendar,
  AlertCircle,
  Truck,
  DollarSign,
  ArrowUpRight,
  ShieldCheck
} from 'lucide-react';

export default function MarketDashboard({ farmer, onTriggerAgentPrompt }) {
  const { t } = useLanguage();
  const [marketData, setMarketData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isUnavailable, setIsUnavailable] = useState(false);

  const currentCrop = farmer?.current_crop || 'Paddy';
  const cropDisplay = t(`crops.${currentCrop.toLowerCase()}`) || currentCrop;
  const location = farmer?.district || 'Vijayawada';

  useEffect(() => {
    async function fetchMarket() {
      setIsLoading(true);
      try {
        const data = await getMarketPrices(currentCrop.toLowerCase(), location, false);
        if (data && data.markets && data.markets.length > 0) {
          setMarketData(data);
          setIsUnavailable(false);
        } else {
          setIsUnavailable(true);
        }
      } catch (err) {
        setIsUnavailable(true);
      } finally {
        setIsLoading(false);
      }
    }
    fetchMarket();
  }, [currentCrop, location]);

  return (
    <div className="view-content-wrapper">
      <div className="view-header-block">
        <h1 className="view-headline">
          📊 {t('marketIntelligenceTitle')}
        </h1>
        <p className="view-subheadline">
          {t('marketHeadlineDesc')}
        </p>
      </div>

      {/* Disclosures when live data is unavailable */}
      {isUnavailable ? (
        <div style={{
          background: '#ffffff',
          border: '1.5px solid var(--amber-500)',
          borderRadius: 'var(--radius-lg)',
          padding: '24px 28px',
          display: 'flex',
          gap: '14px',
          alignItems: 'flex-start',
          boxShadow: 'var(--shadow-sm)'
        }}>
          <AlertCircle size={24} color="var(--amber-500)" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div>
            <h3 style={{ fontSize: '16px', fontWeight: 800, color: 'var(--text-main)', marginBottom: '4px' }}>
              {t('liveDataUnavailable')}
            </h3>
            <p style={{ fontSize: '13.5px', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
              {t('liveDataUnavailableDesc')}
            </p>
            <button
              className="btn-review-action"
              style={{ marginTop: '12px' }}
              onClick={() => onTriggerAgentPrompt(`Analyze regional market trends and expected pricing for ${cropDisplay}`)}
            >
              {t('askAgentPricingModel')}
            </button>
          </div>
        </div>
      ) : (
        <>
          {/* Top KPI Cards for Market */}
          <div className="kpi-cards-grid">
            <div className="kpi-card">
              <span className="kpi-label">{t('commodity')}</span>
              <div className="kpi-val-primary">{cropDisplay}</div>
              <div className="kpi-val-sub">{location} {t('districtField')}</div>
            </div>

            <div className="kpi-card">
              <span className="kpi-label">{t('bestMandiModalRate')}</span>
              <div className="kpi-val-primary">₹{marketData?.markets?.[0]?.modal_price_per_quintal || '2,340'}</div>
              <div className="kpi-val-sub">{t('perQuintalUnit')}</div>
            </div>

            <div className="kpi-card">
              <span className="kpi-label">{t('sellingRecommendation')}</span>
              <div className="kpi-val-primary" style={{ fontSize: '18px', color: 'var(--emerald-800)' }}>
                {marketData?.best_market || 'Vijayawada APMC'}
              </div>
              <div className="kpi-val-sub">{t('highestNetMargin')}</div>
            </div>

            <div className="kpi-card">
              <span className="kpi-label">{t('source')}</span>
              <div className="kpi-val-primary" style={{ fontSize: '18px' }}>
                AGMARKNET
              </div>
              <div className="kpi-val-sub">{t('verifiedGovtFeed')}</div>
            </div>
          </div>

          {/* Mandi Comparison Table */}
          <div className="table-card-container">
            <h3 style={{ fontSize: '16px', fontWeight: 800, color: 'var(--text-main)', marginBottom: '14px' }}>
              {t('mandiComparison')}
            </h3>
            <table className="custom-data-table">
              <thead>
                <tr>
                  <th>{t('marketName')}</th>
                  <th>{t('modalPrice')}</th>
                  <th>{t('transportCost')}</th>
                  <th>{t('netRealization')}</th>
                  <th>{t('distanceKm')}</th>
                </tr>
              </thead>
              <tbody>
                {(marketData?.markets || [
                  { market_name: 'Vijayawada AMCO Mandi', modal_price_per_quintal: 2340, transport_cost_per_quintal: 45, net_effective_price_per_quintal: 2295, distance_km: 18 },
                  { market_name: 'Guntur Mirchi Yard / Grain', modal_price_per_quintal: 2310, transport_cost_per_quintal: 75, net_effective_price_per_quintal: 2235, distance_km: 36 },
                  { market_name: 'Tenali Regulated Market', modal_price_per_quintal: 2280, transport_cost_per_quintal: 60, net_effective_price_per_quintal: 2220, distance_km: 28 }
                ]).map((m, idx) => (
                  <tr key={idx}>
                    <td><strong>{m.market_name}</strong></td>
                    <td style={{ fontWeight: 700, color: 'var(--text-main)' }}>₹{m.modal_price_per_quintal}</td>
                    <td style={{ color: 'var(--rose-600)' }}>-₹{m.transport_cost_per_quintal}</td>
                    <td style={{ fontWeight: 800, color: 'var(--emerald-800)' }}>₹{m.net_effective_price_per_quintal}</td>
                    <td>{m.distance_km} km</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
