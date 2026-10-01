import React, { useState } from 'react';
import { useLanguage } from '../../i18n';
import {
  X,
  Search,
  MessageSquare,
  Trash2,
  Calendar
} from 'lucide-react';

export default function AllChatsModal({
  isOpen,
  onClose,
  conversations,
  activeConversationId,
  onSelectConversation,
  onDeleteConversation
}) {
  const { t } = useLanguage();
  const [searchQuery, setSearchQuery] = useState('');

  if (!isOpen) return null;

  const filtered = (conversations || []).filter(c => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      (c.title && c.title.toLowerCase().includes(q)) ||
      (c.crop && c.crop.toLowerCase().includes(q))
    );
  });

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-dialog-box" style={{ maxWidth: '640px' }} onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '18px 24px',
          borderBottom: '1px solid var(--border-subtle)'
        }}>
          <h3 style={{ fontSize: '18px', fontWeight: 800, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <MessageSquare size={18} color="var(--emerald-800)" />
            {t('chats')}
          </h3>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', padding: '4px' }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Search */}
        <div style={{ padding: '14px 24px', borderBottom: '1px solid var(--border-subtle)' }}>
          <div className="chat-search-input-box" style={{ margin: 0 }}>
            <Search size={14} color="var(--text-muted)" />
            <input
              type="text"
              placeholder={t('searchConversations')}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              autoFocus
            />
          </div>
        </div>

        {/* List */}
        <div style={{ maxHeight: '420px', overflowY: 'auto', padding: '12px 18px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
          {filtered.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '30px', color: 'var(--text-muted)', fontSize: '14px' }}>
              {t('noConversationsFound')}
            </div>
          ) : (
            filtered.map((conv) => {
              const isActive = activeConversationId === conv.id;
              return (
                <div
                  key={conv.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 14px',
                    borderRadius: 'var(--radius-md)',
                    background: isActive ? 'var(--emerald-50)' : 'var(--bg-surface-alt)',
                    border: `1px solid ${isActive ? 'var(--border-emerald)' : 'var(--border-subtle)'}`,
                    cursor: 'pointer'
                  }}
                  onClick={() => {
                    onSelectConversation(conv.id);
                    onClose();
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <MessageSquare size={16} color={isActive ? 'var(--emerald-800)' : 'var(--text-muted)'} />
                    <div>
                      <div style={{ fontSize: '13.5px', fontWeight: isActive ? 700 : 500, color: 'var(--text-main)' }}>
                        {conv.title || t('newChat')}
                      </div>
                      <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                        {conv.crop ? `${conv.crop} • ` : ''}{conv.updated_at ? new Date(conv.updated_at).toLocaleDateString() : ''}
                      </div>
                    </div>
                  </div>

                  <button
                    className="mini-action-btn"
                    title={t('delete')}
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteConversation(conv.id);
                    }}
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
