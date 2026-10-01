import React from 'react';
import { BookOpen, ShieldCheck, Bookmark, ExternalLink } from 'lucide-react';
import { useLanguage } from '../i18n';

export default function SourcesView({ sources = [] }) {
  const { t } = useLanguage();

  if (!sources || sources.length === 0) {
    return (
      <div className="sources-empty">
        <BookOpen size={44} className="empty-icon" />
        <h4>{t('sourcesTitle')}</h4>
        <p>{t('noSourcesFound')}</p>
      </div>
    );
  }

  return (
    <div className="sources-container">
      {/* Header Banner */}
      <div className="sources-header-banner">
        <div className="banner-left">
          <ShieldCheck size={22} color="#10b981" />
          <div>
            <h4>{t('sourcesTitle')}</h4>
            <p>{t('sourcesSubtitle')}</p>
          </div>
        </div>
        <span className="sources-count-badge">
          {sources.length} {t('verifiedResearch')}
        </span>
      </div>

      {/* Sources List */}
      <div className="sources-cards-list">
        {sources.map((src, idx) => (
          <div key={idx} className="source-card">
            <div className="source-card-top">
              <div className="source-main-info">
                <div className="source-title-row">
                  <Bookmark size={15} color="#10b981" />
                  <h5>{src.document_title}</h5>
                </div>
                <div className="source-meta-row">
                  <span><strong>{t('organization')}:</strong> {src.source_organization}</span>
                  {src.section_or_chapter && (
                    <>
                      <span className="dot">•</span>
                      <span><strong>{t('section')}:</strong> {src.section_or_chapter}</span>
                    </>
                  )}
                  {src.page_number && (
                    <>
                      <span className="dot">•</span>
                      <span><strong>{t('page')}:</strong> {src.page_number}</span>
                    </>
                  )}
                </div>
              </div>
            </div>

            {/* Snippet */}
            <blockquote className="source-snippet">
              "{src.content_snippet}"
            </blockquote>

            {/* Provenance / Reference */}
            <div className="source-card-footer">
              <span><strong>{t('provenance')}:</strong> {src.official_reference}</span>
              <span className="verified-status">
                <ShieldCheck size={12} color="#10b981" />
                <span>{t('lastVerified')}</span>
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
