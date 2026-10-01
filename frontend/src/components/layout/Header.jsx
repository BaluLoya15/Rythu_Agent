import React from 'react';
import { useLanguage } from '../../i18n';
import { Sprout, Globe, User } from 'lucide-react';

export default function Header({
  farmer,
  onOpenFarmerModal
}) {
  const { language, setLanguage, t } = useLanguage();

  const farmerName = farmer?.name || t('defaultFarmerName');
  const cropName = (farmer?.current_crop && t(`crops.${farmer.current_crop.toLowerCase()}`)) || farmer?.current_crop || 'Paddy';
  const locationName = farmer?.district || farmer?.location?.split(',')[0] || t('defaultLocation');
  const landArea = farmer?.land_area || `2.0 ${t('acres')}`;

  return (
    <header className="command-header">
      {/* Brand Section */}
      <div className="header-left">
        <div className="brand-badge">
          <div className="brand-icon-box">
            <Sprout size={22} strokeWidth={2.4} />
          </div>
          <div className="brand-text-block">
            <span className="brand-title-text">RYTHU AGENT</span>
            <span className="brand-tagline-text">AI-powered agricultural action agent</span>
          </div>
        </div>
      </div>

      {/* Right Controls */}
      <div className="header-right">
        {/* Language Selector Dropdown */}
        <div className="lang-dropdown-wrapper">
          <div className="lang-select-btn">
            <Globe size={15} color="var(--emerald-700)" />
            <select
              id="language-select"
              aria-label="Select language"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              style={{
                background: 'transparent',
                border: 'none',
                outline: 'none',
                fontWeight: 600,
                fontSize: '13.5px',
                color: 'var(--text-main)',
                cursor: 'pointer'
              }}
            >
              <option value="en">English</option>
              <option value="te">తెలుగు</option>
              <option value="hi">हिन्दी</option>
            </select>
          </div>
        </div>

        {/* Farmer Profile Pill */}
        <div
          className="farmer-profile-pill"
          onClick={onOpenFarmerModal}
          title={t('editProfile')}
          role="button"
          tabIndex={0}
        >
          <div className="farmer-avatar-circle">
            {farmerName.charAt(0)}
          </div>
          <div className="farmer-pill-info">
            <span className="farmer-pill-name">{farmerName}</span>
            <span className="farmer-pill-meta">
              {landArea} • {cropName} • {locationName}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
