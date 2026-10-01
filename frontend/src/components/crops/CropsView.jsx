import React, { useState } from 'react';
import { useLanguage } from '../../i18n';
import {
  Sprout,
  Calendar,
  Layers,
  TrendingUp,
  AlertTriangle,
  ArrowRight,
  ShieldCheck,
  CheckCircle2
} from 'lucide-react';

export default function CropsView({ farmer, onTriggerAgentPrompt }) {
  const { t } = useLanguage();
  const [selectedCrop, setSelectedCrop] = useState(farmer?.current_crop || 'Paddy');

  // Primary Crops (prominent)
  const primaryCrops = [
    {
      id: 'paddy',
      name: t('crops.paddy'),
      area: farmer?.current_crop === 'Paddy' ? farmer?.land_area || `2.0 ${t('acres')}` : `2.0 ${t('acres')}`,
      age: `40 ${t('daysUnit')}`,
      stage: t('stageTilleringPanicle'),
      status: t('cropStatusHealthy'),
      variety: 'BPT-5204 (Samba Mahsuri)',
      soil: 'Clay loam with assured irrigation',
      pests: t('pestsPaddy'),
      price: `₹2,340 / ${t('unit') || 'quintal'}`,
      isPrimary: true
    },
    {
      id: 'sugarcane',
      name: t('crops.sugarcane'),
      area: `1.5 ${t('acres')}`,
      age: `120 ${t('daysUnit')}`,
      stage: t('stageGrandGrowth'),
      status: t('cropStatusMonitoring'),
      variety: 'Co 86032 (Nayana)',
      soil: 'Deep well-drained loam',
      pests: t('pestsSugarcane'),
      price: '₹3,400 / ton (FRP)',
      isPrimary: true
    },
    {
      id: 'black_gram',
      name: t('crops.black_gram'),
      area: `1.0 ${t('acres')}`,
      age: `25 ${t('daysUnit')}`,
      stage: t('stageVegetativeBranching'),
      status: t('cropStatusHealthy'),
      variety: 'LBG-752',
      soil: 'Rice fallow clay soils',
      pests: t('pestsBlackGram'),
      price: `₹7,800 / ${t('unit') || 'quintal'}`,
      isPrimary: true
    }
  ];

  // Secondary Crops
  const secondaryCrops = [
    {
      id: 'tomato',
      name: t('crops.tomato'),
      area: `0.5 ${t('acres')}`,
      age: `35 ${t('daysUnit')}`,
      stage: t('stageVegetativeFlowering'),
      status: t('cropStatusMonitoring'),
      variety: 'Arka Rakshak',
      soil: 'Sandy loam with drip',
      pests: t('pestsTomato'),
      price: `₹1,800 / ${t('unit') || 'quintal'}`,
      isPrimary: false
    },
    {
      id: 'chilli',
      name: t('crops.chilli'),
      area: `0.5 ${t('acres')}`,
      age: `45 ${t('daysUnit')}`,
      stage: t('stageActiveFloweringFruit'),
      status: t('cropStatusAttention'),
      variety: 'Guntur Hope / Teja',
      soil: 'Black cotton with furrow',
      pests: t('pestsChilli'),
      price: `₹18,500 / ${t('unit') || 'quintal'}`,
      isPrimary: false
    },
    {
      id: 'groundnut',
      name: t('crops.groundnut'),
      area: `1.0 ${t('acres')}`,
      age: `40 ${t('daysUnit')}`,
      stage: t('stagePegging'),
      status: t('cropStatusHealthy'),
      variety: 'Kadiri-6',
      soil: 'Red sandy loam',
      pests: t('pestsGroundnut'),
      price: `₹6,400 / ${t('unit') || 'quintal'}`,
      isPrimary: false
    }
  ];

  const handleAskAdvisory = (crop) => {
    onTriggerAgentPrompt(`Provide weekly cultivation plan and pest advisory for ${crop.name} at ${crop.stage} (${crop.age})`);
  };

  return (
    <div className="view-content-wrapper">
      <div className="view-header-block">
        <h1 className="view-headline">
          🌾 {t('navCrops')}
        </h1>
        <p className="view-subheadline">
          {t('cropsViewSubheadline')}
        </p>
      </div>

      {/* Primary Crops Section */}
      <section>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
          <h2 style={{ fontSize: '18px', fontWeight: 800, color: 'var(--emerald-950)' }}>
            ★ {t('primaryCrops')}
          </h2>
          <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--emerald-800)', background: 'var(--emerald-100)', padding: '2px 8px', borderRadius: 'var(--radius-full)' }}>
            {t('coreAgronomicHierarchy')}
          </span>
        </div>

        <div className="crops-grid-container">
          {primaryCrops.map((crop) => (
            <div key={crop.id} className="crop-card-view primary-crop">
              <div className="crop-card-top">
                <span className="crop-name-title">{crop.name}</span>
                <span style={{
                  fontSize: '11.5px',
                  fontWeight: 700,
                  padding: '3px 9px',
                  borderRadius: 'var(--radius-full)',
                  background: crop.status === t('cropStatusHealthy') ? 'var(--emerald-100)' : 'var(--amber-100)',
                  color: crop.status === t('cropStatusHealthy') ? 'var(--emerald-800)' : 'var(--amber-500)'
                }}>
                  {crop.status}
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '13px' }}>
                <div>
                  <span style={{ color: 'var(--text-muted)', fontSize: '11.5px' }}>{t('cropAge')}:</span>
                  <div style={{ fontWeight: 700, color: 'var(--text-main)' }}>{crop.age}</div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)', fontSize: '11.5px' }}>{t('cropStage')}:</span>
                  <div style={{ fontWeight: 700, color: 'var(--text-main)' }}>{crop.stage}</div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)', fontSize: '11.5px' }}>{t('landArea')}:</span>
                  <div style={{ fontWeight: 700, color: 'var(--text-main)' }}>{crop.area}</div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)', fontSize: '11.5px' }}>{t('mandiPriceLabel')}:</span>
                  <div style={{ fontWeight: 700, color: 'var(--emerald-900)' }}>{crop.price}</div>
                </div>
              </div>

              <div style={{
                background: 'var(--bg-surface-alt)',
                padding: '10px',
                borderRadius: 'var(--radius-sm)',
                fontSize: '12px',
                color: 'var(--text-secondary)'
              }}>
                <div style={{ fontWeight: 700, color: 'var(--text-main)', marginBottom: '3px' }}>
                  🛡️ {t('activeSurveillance')}:
                </div>
                {crop.pests}
              </div>

              <button
                className="btn-confirm-action"
                style={{ width: '100%', marginTop: '6px' }}
                onClick={() => handleAskAdvisory(crop)}
              >
                <span>{t('viewAdvisory')}</span>
                <ArrowRight size={14} />
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* Secondary Crops Section */}
      <section style={{ marginTop: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
          <h2 style={{ fontSize: '18px', fontWeight: 800, color: 'var(--text-main)' }}>
            {t('secondaryCrops')}
          </h2>
          <span style={{ fontSize: '12px', fontWeight: 500, color: 'var(--text-muted)' }}>
            {t('commercialHorticulture')}
          </span>
        </div>

        <div className="crops-grid-container">
          {secondaryCrops.map((crop) => (
            <div key={crop.id} className="crop-card-view">
              <div className="crop-card-top">
                <span className="crop-name-title">{crop.name}</span>
                <span style={{
                  fontSize: '11.5px',
                  fontWeight: 700,
                  padding: '3px 9px',
                  borderRadius: 'var(--radius-full)',
                  background: crop.status === t('cropStatusHealthy') ? 'var(--emerald-100)' : crop.status === t('cropStatusMonitoring') ? 'var(--blue-100)' : 'var(--amber-100)',
                  color: crop.status === t('cropStatusHealthy') ? 'var(--emerald-800)' : crop.status === t('cropStatusMonitoring') ? 'var(--blue-600)' : 'var(--amber-500)'
                }}>
                  {crop.status}
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '13px' }}>
                <div>
                  <span style={{ color: 'var(--text-muted)', fontSize: '11.5px' }}>{t('cropAge')}:</span>
                  <div style={{ fontWeight: 700, color: 'var(--text-main)' }}>{crop.age}</div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)', fontSize: '11.5px' }}>{t('cropStage')}:</span>
                  <div style={{ fontWeight: 700, color: 'var(--text-main)' }}>{crop.stage}</div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)', fontSize: '11.5px' }}>{t('landArea')}:</span>
                  <div style={{ fontWeight: 700, color: 'var(--text-main)' }}>{crop.area}</div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)', fontSize: '11.5px' }}>{t('mandiPriceLabel')}:</span>
                  <div style={{ fontWeight: 700, color: 'var(--emerald-900)' }}>{crop.price}</div>
                </div>
              </div>

              <div style={{
                background: 'var(--bg-surface-alt)',
                padding: '10px',
                borderRadius: 'var(--radius-sm)',
                fontSize: '12px',
                color: 'var(--text-secondary)'
              }}>
                <div style={{ fontWeight: 700, color: 'var(--text-main)', marginBottom: '3px' }}>
                  🛡️ {t('activeSurveillance')}:
                </div>
                {crop.pests}
              </div>

              <button
                className="btn-confirm-action"
                style={{ width: '100%', marginTop: '6px' }}
                onClick={() => handleAskAdvisory(crop)}
              >
                <span>{t('viewAdvisory')}</span>
                <ArrowRight size={14} />
              </button>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
