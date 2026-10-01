import React from 'react';
import { Landmark, FileText, CheckCircle2, ExternalLink, AlertTriangle, ShieldCheck } from 'lucide-react';
import { useLanguage } from '../i18n';

export default function ServicesView({ servicesData, farmer }) {
  const { t } = useLanguage();

  if (!servicesData || servicesData.length === 0) {
    return (
      <div className="services-empty">
        <Landmark size={44} className="empty-icon" />
        <p>{t('noServicesFound')}</p>
      </div>
    );
  }

  return (
    <div className="services-container">
      {/* Disclaimer Banner */}
      <div className="services-disclaimer-banner">
        <AlertTriangle size={18} color="#fbbf24" className="disclaimer-icon" />
        <div className="disclaimer-text">
          <strong>{t('disclaimer')}:</strong> {t('disclaimerText')}
        </div>
      </div>

      {/* Scheme Cards Grid */}
      <div className="schemes-grid">
        {servicesData.map((scheme) => (
          <div key={scheme.id} className="scheme-card">
            <div className="scheme-card-header">
              <div>
                <div className="scheme-title-row">
                  <Landmark size={18} color="#10b981" />
                  <h4>{scheme.name}</h4>
                </div>
                <div className="scheme-level">
                  {scheme.level} • {scheme.scheme_code}
                </div>
              </div>
              <span className="scheme-subsidy-badge">
                {scheme.subsidy_percentage || t('verification')}
              </span>
            </div>

            <p className="scheme-purpose">{scheme.purpose}</p>

            {/* Key Benefits */}
            <div className="scheme-benefits-box">
              <div className="box-title">💰 {t('benefits')}:</div>
              <div className="box-desc">{scheme.benefits}</div>
            </div>

            <div className="scheme-details-grid">
              {/* Eligibility */}
              <div className="detail-col">
                <div className="detail-col-title">
                  {t('eligibility')} ({t('pendingApproval')}):
                </div>
                <ul className="detail-list">
                  {scheme.eligibility_criteria?.map((el, i) => (
                    <li key={i}>{el}</li>
                  ))}
                </ul>
              </div>

              {/* Required Documents */}
              <div className="detail-col">
                <div className="detail-col-title">
                  {t('requiredDocuments')}:
                </div>
                <ul className="detail-list">
                  {(scheme.required_documents || scheme.documents_required || []).map((doc, i) => (
                    <li key={i}>{doc}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Application Procedure & Official Portal */}
            <div className="scheme-footer-box">
              <div className="procedure-row">
                <strong>{t('applicationProcedure')}:</strong>
                {Array.isArray(scheme.application_process) ? (
                  <ol className="procedure-steps-list" style={{ margin: '6px 0 0 16px', padding: 0, fontSize: '0.82rem', lineHeight: '1.4' }}>
                    {scheme.application_process.map((step, sIdx) => (
                      <li key={sIdx} style={{ marginBottom: '3px' }}>{step}</li>
                    ))}
                  </ol>
                ) : (
                  <span> {scheme.application_process || scheme.how_to_apply || t('applyAtRBK')}</span>
                )}
              </div>
              <div className="portal-row" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '8px', marginTop: '10px' }}>
                {(scheme.official_portal_url || scheme.official_portal) && (
                  <a
                    href={scheme.official_portal_url || scheme.official_portal}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="portal-link"
                    style={{ display: 'inline-flex', alignItems: 'center', gap: '5px', background: '#059669', color: '#ffffff', padding: '6px 12px', borderRadius: '6px', fontSize: '0.8rem', fontWeight: '600', textDecoration: 'none' }}
                  >
                    <span>{t('officialPortal')}</span>
                    <ExternalLink size={13} />
                  </a>
                )}
                {scheme.helpline_number && (
                  <span style={{ fontSize: '0.78rem', color: '#374151', background: '#f3f4f6', padding: '4px 8px', borderRadius: '4px' }}>
                    📞 {scheme.helpline_number}
                  </span>
                )}
                {(scheme.last_verified_date || scheme.last_verified) && (
                  <span className="last-verified-tag">
                    <ShieldCheck size={12} color="#10b981" />
                    <span>{t('lastVerified')}: {scheme.last_verified_date || scheme.last_verified}</span>
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
