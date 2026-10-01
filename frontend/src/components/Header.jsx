import React from 'react';
import { Sprout, User, Globe } from 'lucide-react';
import { useLanguage } from '../i18n';

export default function Header({
  farmer,
  onOpenFarmerModal,
  onToggleSidebar,
  sidebarOpen
}) {
  const { language, setLanguage, t, supportedLanguages, normalizeCropKey } = useLanguage();

  // Extract clean farmer display strings
  const farmerName = farmer?.name || t('defaultFarmerName');
  const landArea = farmer?.land_area || `2.0 ${t('acres')}`;
  const rawCrop = farmer?.current_crop || 'Paddy';
  const cropKey = normalizeCropKey(rawCrop);
  const localizedCrop = t(`crops.${cropKey}`) || rawCrop;
  const location = farmer?.location?.split(',')[0] || t('defaultLocation');

  return (
    <header className="app-header">
      {/* LEFT: Product Identity */}
      <div className="brand-section">
        {onToggleSidebar && (
          <button
            className="mobile-sidebar-toggle"
            onClick={onToggleSidebar}
            title={sidebarOpen ? 'Collapse Sidebar' : 'Open Sidebar'}
            aria-label="Toggle Sidebar"
          >
            ☰
          </button>
        )}
        <div className="logo-badge">
          <Sprout size={26} color="#10b981" />
        </div>
        <div className="brand-info">
          <h1 className="brand-title">RYTHU AGENT</h1>
          <p className="brand-subtitle">{t('appSubtitle')}</p>
        </div>
      </div>

      {/* RIGHT: Language Selector & Farmer Profile */}
      <div className="header-actions">
        {/* Multilingual Selector: 🌐 English | తెలుగు | हिन्दी */}
        <div className="lang-selector-pill" role="group" aria-label="Language selector">
          <Globe size={14} color="#10b981" className="globe-icon" />
          {supportedLanguages.map((l) => (
            <button
              key={l.code}
              id={`lang-btn-${l.code}`}
              className={`lang-btn ${language === l.code ? 'active' : ''}`}
              onClick={() => setLanguage(l.code)}
              title={`Switch language to ${l.label}`}
            >
              {l.nativeLabel}
            </button>
          ))}
        </div>

        {/* Farmer Profile Pill */}
        <button
          className="farmer-profile-card"
          onClick={onOpenFarmerModal}
          title={t('editProfile')}
          aria-label={t('farmerProfile')}
        >
          <div className="farmer-avatar">
            <User size={16} />
          </div>
          <div className="farmer-summary">
            <div className="farmer-name-row">
              <span className="farmer-name">{farmerName}</span>
              <span className="farmer-edit-badge">{t('editProfile')}</span>
            </div>
            <div className="farmer-meta-row">
              <span>{landArea}</span>
              <span className="dot">•</span>
              <span>{localizedCrop}</span>
              <span className="dot">•</span>
              <span>{location}</span>
            </div>
          </div>
        </button>
      </div>
    </header>
  );
}
