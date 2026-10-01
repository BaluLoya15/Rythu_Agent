import React, { useState, useEffect } from 'react';
import { useLanguage } from '../../i18n';
import { getServices } from '../../api/client';
import {
  Landmark,
  ShieldCheck,
  PhoneCall,
  ExternalLink,
  Search,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  ArrowRight,
  Sparkles
} from 'lucide-react';

export default function ServicesDashboard({ farmer, onTriggerAgentPrompt }) {
  const { t, language } = useLanguage();
  const [services, setServices] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('all');
  const [openEligibilityMap, setOpenEligibilityMap] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchServices() {
      setIsLoading(true);
      try {
        const data = await getServices('all schemes', language);
        setServices(data || []);
      } catch (err) {
        console.error('Error fetching schemes:', err);
      } finally {
        setIsLoading(false);
      }
    }
    fetchServices();
  }, [language]);

  const toggleEligibility = (id) => {
    setOpenEligibilityMap((prev) => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const categories = [
    { id: 'all', label: t('filterAll') },
    { id: 'central', label: t('filterCentral') },
    { id: 'state', label: t('filterState') },
    { id: 'insurance', label: t('filterInsurance') },
    { id: 'credit', label: t('filterCredit') }
  ];

  const filtered = services.filter((s) => {
    // Category match
    if (activeCategory === 'central' && !s.level?.toLowerCase().includes('central') && !s.level?.toLowerCase().includes('కేంద్ర') && !s.level?.toLowerCase().includes('केंद्र')) {
      return false;
    }
    if (activeCategory === 'state' && !s.level?.toLowerCase().includes('state') && !s.level?.toLowerCase().includes('andhra') && !s.level?.toLowerCase().includes('ఆంధ్ర') && !s.level?.toLowerCase().includes('రాష్ట్ర') && !s.level?.toLowerCase().includes('आंध्र')) {
      return false;
    }
    if (activeCategory === 'insurance' && !s.name?.toLowerCase().includes('bima') && !s.name?.toLowerCase().includes('బీమా') && !s.name?.toLowerCase().includes('insurance') && !s.name?.toLowerCase().includes('बीमा')) {
      return false;
    }
    if (activeCategory === 'credit' && !s.name?.toLowerCase().includes('credit') && !s.name?.toLowerCase().includes('kcc') && !s.name?.toLowerCase().includes('రుణ') && !s.name?.toLowerCase().includes('loan') && !s.name?.toLowerCase().includes('ऋण')) {
      return false;
    }

    // Search query match
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      s.name?.toLowerCase().includes(q) ||
      s.purpose?.toLowerCase().includes(q) ||
      s.benefits?.toLowerCase().includes(q)
    );
  });

  return (
    <div className="view-content-wrapper">
      {/* Top Banner Matching Reference Image */}
      <div style={{
        background: '#ffffff',
        border: '1.5px solid var(--border-emerald)',
        borderLeft: '5px solid #1b4d3e',
        borderRadius: 'var(--radius-lg)',
        padding: '24px 28px',
        boxShadow: 'var(--shadow-sm)',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }}>
        <div>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontSize: '12px',
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: '0.04em',
            color: '#1b4d3e',
            marginBottom: '6px'
          }}>
            <Landmark size={15} />
            <span>{t('servicesBadge')}</span>
          </div>
          <h1 style={{
            fontSize: '26px',
            fontWeight: 800,
            color: 'var(--text-main)',
            margin: '0 0 6px 0',
            lineHeight: 1.2
          }}>
            {t('servicesHeadline')}
          </h1>
          <p style={{
            fontSize: '14px',
            color: 'var(--text-secondary)',
            margin: 0,
            lineHeight: 1.45
          }}>
            {t('servicesSubheadline')}
          </p>
        </div>

        {/* Filter Pills Matching Reference Image */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          flexWrap: 'wrap',
          paddingTop: '6px',
          borderTop: '1px solid var(--border-subtle)'
        }}>
          {categories.map((cat) => {
            const isActive = activeCategory === cat.id;
            return (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                style={{
                  padding: '7px 16px',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '13px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  border: isActive ? '1px solid #1b4d3e' : '1px solid var(--border-subtle)',
                  background: isActive ? '#1b4d3e' : '#ffffff',
                  color: isActive ? '#ffffff' : 'var(--text-secondary)',
                  transition: 'all 0.15s ease'
                }}
              >
                {cat.label}
              </button>
            );
          })}
        </div>

        {/* Search Input */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          padding: '8px 14px',
          background: 'var(--bg-surface-alt)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-md)',
          maxWidth: '520px'
        }}>
          <Search size={16} color="var(--text-muted)" />
          <input
            type="text"
            placeholder={t('searchSchemesPlaceholder')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              border: 'none',
              background: 'transparent',
              outline: 'none',
              fontSize: '13.5px',
              width: '100%',
              color: 'var(--text-main)'
            }}
          />
        </div>
      </div>

      {/* Schemes Grid Matching Reference Image 3-Column Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(330px, 1fr))',
        gap: '20px',
        marginTop: '8px'
      }}>
        {filtered.map((sc, i) => {
          const isEligibleOpen = Boolean(openEligibilityMap[sc.id]);
          return (
            <div
              key={sc.id || i}
              style={{
                background: '#ffffff',
                border: '1.5px solid var(--border-subtle)',
                borderRadius: '14px',
                overflow: 'hidden',
                boxShadow: '0 2px 6px rgba(0, 0, 0, 0.04)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                transition: 'transform 0.15s ease, box-shadow 0.15s ease'
              }}
            >
              <div>
                {/* Top Category Tag Pill */}
                <div style={{ padding: '12px 16px 8px 16px' }}>
                  <span style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px',
                    fontSize: '11px',
                    fontWeight: 700,
                    color: 'var(--text-secondary)',
                    background: 'var(--bg-surface-alt)',
                    padding: '3px 10px',
                    borderRadius: 'var(--radius-full)',
                    border: '1px solid var(--border-subtle)'
                  }}>
                    🏛️ {sc.level}
                  </span>
                </div>

                {/* Card Title Banner with Emerald Gradient */}
                <div style={{
                  background: 'linear-gradient(180deg, #1b4d3e 0%, #235d4b 100%)',
                  padding: '16px 18px',
                  color: '#ffffff'
                }}>
                  <h3 style={{
                    fontSize: '16.5px',
                    fontWeight: 800,
                    margin: 0,
                    lineHeight: 1.35,
                    color: '#ffffff'
                  }}>
                    {sc.name}
                  </h3>
                </div>

                {/* Card Body: Benefits & Accordion */}
                <div style={{ padding: '16px 18px' }}>
                  {/* Benefits Section */}
                  <div style={{ marginBottom: '14px' }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '5px',
                      fontSize: '12px',
                      fontWeight: 700,
                      color: '#1b4d3e',
                      textTransform: 'uppercase',
                      marginBottom: '6px'
                    }}>
                      <span>💸</span>
                      <span>{t('keyBenefits')}</span>
                    </div>
                    <p style={{
                      fontSize: '13px',
                      color: 'var(--text-secondary)',
                      lineHeight: 1.5,
                      margin: 0
                    }}>
                      {sc.benefits}
                    </p>
                  </div>

                  {/* Collapsible Eligibility Accordion */}
                  <div style={{
                    border: '1px solid var(--border-subtle)',
                    borderRadius: 'var(--radius-md)',
                    overflow: 'hidden'
                  }}>
                    <button
                      onClick={() => toggleEligibility(sc.id)}
                      style={{
                        width: '100%',
                        padding: '10px 12px',
                        background: 'var(--bg-surface-alt)',
                        border: 'none',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        cursor: 'pointer',
                        fontSize: '12.5px',
                        fontWeight: 600,
                        color: 'var(--text-main)'
                      }}
                    >
                      <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <CheckCircle2 size={14} color="#1b4d3e" />
                        <span>{t('eligibilityCriteria')}</span>
                      </span>
                      {isEligibleOpen ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                    </button>

                    {isEligibleOpen && (
                      <div style={{
                        padding: '12px',
                        background: '#ffffff',
                        borderTop: '1px solid var(--border-subtle)',
                        fontSize: '12px',
                        color: 'var(--text-secondary)'
                      }}>
                        <ul style={{ margin: '0 0 0 16px', padding: 0, lineHeight: 1.5 }}>
                          {(sc.eligibility_criteria || []).map((el, idx) => (
                            <li key={idx} style={{ marginBottom: '4px' }}>{el}</li>
                          ))}
                        </ul>
                        {sc.helpline_number && (
                          <div style={{ marginTop: '8px', paddingTop: '6px', borderTop: '1px dashed var(--border-subtle)', fontSize: '11.5px', color: 'var(--text-muted)' }}>
                            <PhoneCall size={12} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '4px' }} />
                            {sc.helpline_number}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Card Footer: Action Buttons */}
              <div style={{
                padding: '0 18px 18px 18px',
                display: 'flex',
                flexDirection: 'column',
                gap: '8px'
              }}>
                {sc.official_portal_url && (
                  <a
                    href={sc.official_portal_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '8px',
                      padding: '11px 16px',
                      background: '#1b4d3e',
                      color: '#ffffff',
                      borderRadius: 'var(--radius-md)',
                      fontSize: '13.5px',
                      fontWeight: 700,
                      textDecoration: 'none',
                      boxShadow: '0 2px 4px rgba(27, 77, 62, 0.25)',
                      transition: 'background 0.15s ease'
                    }}
                  >
                    <span>{t('viewOfficialWebsite')}</span>
                    <ExternalLink size={14} />
                  </a>
                )}

                <button
                  onClick={() => onTriggerAgentPrompt?.(`Check detailed eligibility and required document checklist for ${sc.name}`)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '6px',
                    padding: '8px 14px',
                    background: 'transparent',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: 'var(--radius-md)',
                    fontSize: '12px',
                    fontWeight: 600,
                    color: 'var(--text-muted)',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease'
                  }}
                >
                  <Sparkles size={12} color="#1b4d3e" />
                  <span>{t('askAgentScheme')}</span>
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
