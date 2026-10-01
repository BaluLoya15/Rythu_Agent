import React, { useState, useMemo } from 'react';
import {
  MessageSquare, Plus, Search, Edit2, Trash2, Archive,
  ArchiveRestore, MoreVertical, X, Check
} from 'lucide-react';
import { useLanguage } from '../i18n';

export default function Sidebar({
  conversations = [],
  activeConversationId,
  onSelectConversation,
  onNewChat,
  onRenameConversation,
  onArchiveConversation,
  onDeleteConversation,
  isOpen,
  onClose
}) {
  const { t, normalizeCropKey } = useLanguage();
  const [searchQuery, setSearchQuery] = useState('');
  const [showArchived, setShowArchived] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState('');
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);
  const [menuOpenId, setMenuOpenId] = useState(null);

  // Filter conversations by active/archived state and search query
  const filteredConversations = useMemo(() => {
    return conversations.filter(c => {
      // Archive filter
      const matchesArchive = showArchived ? Boolean(c.archived) : !c.archived;
      if (!matchesArchive) return false;

      // Search query filter (matches title, crop, or language)
      if (!searchQuery.trim()) return true;
      const q = searchQuery.toLowerCase();
      const titleMatch = (c.title || '').toLowerCase().includes(q);
      const cropMatch = (c.crop || '').toLowerCase().includes(q);
      return titleMatch || cropMatch;
    });
  }, [conversations, showArchived, searchQuery]);

  // Group conversations by date relative to user's local timezone
  const groupedConversations = useMemo(() => {
    const today = [];
    const yesterday = [];
    const previous7Days = [];
    const older = [];

    const now = new Date();
    const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
    const startOfYesterday = startOfToday - 24 * 60 * 60 * 1000;
    const startOf7Days = startOfToday - 7 * 24 * 60 * 1000;

    filteredConversations.forEach(conv => {
      const convTime = new Date(conv.updated_at || conv.created_at).getTime();
      if (convTime >= startOfToday) {
        today.push(conv);
      } else if (convTime >= startOfYesterday) {
        yesterday.push(conv);
      } else if (convTime >= startOf7Days) {
        previous7Days.push(conv);
      } else {
        older.push(conv);
      }
    });

    return [
      { key: 'today', title: t('today'), items: today },
      { key: 'yesterday', title: t('yesterday'), items: yesterday },
      { key: 'previous7Days', title: t('previous7Days'), items: previous7Days },
      { key: 'older', title: t('older'), items: older }
    ].filter(g => g.items.length > 0);
  }, [filteredConversations, t]);

  const handleStartRename = (conv, e) => {
    e.stopPropagation();
    setEditingId(conv.id);
    setEditTitle(conv.title || '');
    setMenuOpenId(null);
  };

  const handleSaveRename = (convId, e) => {
    e.stopPropagation();
    if (editTitle.trim()) {
      onRenameConversation(convId, editTitle.trim());
    }
    setEditingId(null);
  };

  const handleCancelRename = (e) => {
    e.stopPropagation();
    setEditingId(null);
  };

  const handleDeletePrompt = (convId, e) => {
    e.stopPropagation();
    setConfirmDeleteId(convId);
    setMenuOpenId(null);
  };

  const handleConfirmDelete = (convId, e) => {
    e.stopPropagation();
    onDeleteConversation(convId);
    setConfirmDeleteId(null);
  };

  const handleToggleArchive = (conv, e) => {
    e.stopPropagation();
    onArchiveConversation(conv.id, !conv.archived);
    setMenuOpenId(null);
  };

  return (
    <aside className={`chat-sidebar ${isOpen ? 'open' : ''}`}>
      {/* Top Header */}
      <div className="sidebar-header">
        <div className="sidebar-title-row">
          <div className="sidebar-brand-title">
            <MessageSquare size={18} color="#10b981" />
            <span>{t('chats')}</span>
          </div>
          {onClose && (
            <button className="sidebar-close-btn" onClick={onClose} aria-label="Close sidebar">
              <X size={16} />
            </button>
          )}
        </div>

        {/* + New Chat Button */}
        <button
          id="new-chat-btn"
          className="btn-new-chat"
          onClick={() => {
            onNewChat();
            if (window.innerWidth < 768 && onClose) onClose();
          }}
        >
          <Plus size={16} />
          <span>{t('newChat')}</span>
        </button>

        {/* Search Conversations Bar */}
        <div className="sidebar-search-box">
          <Search size={14} className="search-icon" />
          <input
            id="search-conversations-input"
            type="text"
            className="search-input"
            placeholder={t('searchConversations')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          {searchQuery && (
            <button
              className="clear-search-btn"
              onClick={() => setSearchQuery('')}
              aria-label="Clear search"
            >
              <X size={12} />
            </button>
          )}
        </div>
      </div>

      {/* Conversations List by Date Groupings */}
      <div className="sidebar-conversations-list">
        {groupedConversations.length === 0 ? (
          <div className="sidebar-empty">
            <p>{searchQuery ? t('noConversationsFound') : showArchived ? t('noArchivedConversations') : t('noConversationsFound')}</p>
          </div>
        ) : (
          groupedConversations.map(group => (
            <div key={group.key} className="conversation-date-group">
              <div className="group-heading">{group.title}</div>
              <ul className="group-items">
                {group.items.map(conv => {
                  const isActive = conv.id === activeConversationId;
                  const isEditing = editingId === conv.id;
                  const cropKey = normalizeCropKey(conv.crop);
                  const cropIcon = cropKey === 'paddy' ? '🌾' :
                                   cropKey === 'sugarcane' ? '🎋' :
                                   cropKey === 'black_gram' ? '🌱' :
                                   cropKey === 'tomato' ? '🍅' :
                                   cropKey === 'chilli' ? '🌶️' :
                                   cropKey === 'groundnut' ? '🥜' : '🌾';

                  return (
                    <li
                      key={conv.id}
                      className={`conversation-item ${isActive ? 'active' : ''}`}
                      onClick={() => {
                        if (!isEditing) {
                          onSelectConversation(conv.id);
                          if (window.innerWidth < 768 && onClose) onClose();
                        }
                      }}
                    >
                      {isEditing ? (
                        <div className="edit-title-form" onClick={(e) => e.stopPropagation()}>
                          <input
                            type="text"
                            className="edit-title-input"
                            value={editTitle}
                            onChange={(e) => setEditTitle(e.target.value)}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') handleSaveRename(conv.id, e);
                              if (e.key === 'Escape') handleCancelRename(e);
                            }}
                            autoFocus
                          />
                          <button
                            className="btn-edit-action save"
                            onClick={(e) => handleSaveRename(conv.id, e)}
                            title={t('save')}
                          >
                            <Check size={14} />
                          </button>
                          <button
                            className="btn-edit-action cancel"
                            onClick={handleCancelRename}
                            title={t('cancel')}
                          >
                            <X size={14} />
                          </button>
                        </div>
                      ) : (
                        <>
                          <div className="conv-main-info">
                            <span className="conv-crop-icon">{cropIcon}</span>
                            <span className="conv-title" title={conv.title}>
                              {conv.title || t('newChat')}
                            </span>
                          </div>

                          {/* Quick Action Menu Trigger */}
                          <div className="conv-actions">
                            <button
                              className="btn-conv-menu"
                              onClick={(e) => {
                                e.stopPropagation();
                                setMenuOpenId(menuOpenId === conv.id ? null : conv.id);
                              }}
                              title="Options"
                            >
                              <MoreVertical size={14} />
                            </button>

                            {/* Dropdown Options */}
                            {menuOpenId === conv.id && (
                              <div className="conv-dropdown-menu" onClick={(e) => e.stopPropagation()}>
                                <button
                                  className="dropdown-item"
                                  onClick={(e) => handleStartRename(conv, e)}
                                >
                                  <Edit2 size={13} />
                                  <span>{t('rename')}</span>
                                </button>
                                <button
                                  className="dropdown-item"
                                  onClick={(e) => handleToggleArchive(conv, e)}
                                >
                                  {conv.archived ? <ArchiveRestore size={13} /> : <Archive size={13} />}
                                  <span>{conv.archived ? t('unarchive') : t('archive')}</span>
                                </button>
                                <button
                                  className="dropdown-item danger"
                                  onClick={(e) => handleDeletePrompt(conv.id, e)}
                                >
                                  <Trash2 size={13} />
                                  <span>{t('delete')}</span>
                                </button>
                              </div>
                            )}
                          </div>
                        </>
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          ))
        )}
      </div>

      {/* Bottom Sidebar Footer: Toggle Archive view */}
      <div className="sidebar-footer">
        <button
          className="btn-toggle-archived"
          onClick={() => setShowArchived(!showArchived)}
        >
          {showArchived ? <ArchiveRestore size={14} /> : <Archive size={14} />}
          <span>{showArchived ? t('chats') : t('archivedChats')}</span>
        </button>
      </div>

      {/* Delete Confirmation Modal */}
      {confirmDeleteId && (
        <div className="modal-backdrop" onClick={() => setConfirmDeleteId(null)}>
          <div className="modal-content confirm-delete-modal" onClick={(e) => e.stopPropagation()}>
            <h3 className="modal-title">{t('deleteConfirmTitle')}</h3>
            <p className="modal-desc">{t('deleteConfirmMessage')}</p>
            <div className="modal-btn-row">
              <button
                className="btn-secondary"
                onClick={() => setConfirmDeleteId(null)}
              >
                {t('cancel')}
              </button>
              <button
                className="btn-danger"
                onClick={(e) => handleConfirmDelete(confirmDeleteId, e)}
              >
                {t('confirmDelete')}
              </button>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}
