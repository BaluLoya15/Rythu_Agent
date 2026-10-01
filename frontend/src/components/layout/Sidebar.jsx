import React, { useState } from 'react';
import { useLanguage } from '../../i18n';
import {
  LayoutDashboard,
  Bot,
  Sprout,
  TrendingUp,
  CloudSun,
  Landmark,
  Plus,
  Search,
  MessageSquare,
  Trash2,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

export default function Sidebar({
  activeView,
  onSelectView,
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  onOpenAllChats,
  isCollapsed,
  onToggleCollapse
}) {
  const { t } = useLanguage();
  const [searchQuery, setSearchQuery] = useState('');

  // Primary navigation items
  const navItems = [
    { id: 'overview', label: t('navOverview'), icon: LayoutDashboard },
    { id: 'agent', label: t('navAgent'), icon: Bot, badge: 'AI' },
    { id: 'crops', label: t('navCrops'), icon: Sprout },
    { id: 'market', label: t('navMarket'), icon: TrendingUp },
    { id: 'weather', label: t('navWeather'), icon: CloudSun },
    { id: 'services', label: t('navServices'), icon: Landmark }
  ];

  // Filter recent conversations
  const filteredConversations = (conversations || [])
    .filter(c => !c.archived)
    .filter(c => {
      if (!searchQuery.trim()) return true;
      const q = searchQuery.toLowerCase();
      return (
        (c.title && c.title.toLowerCase().includes(q)) ||
        (c.crop && c.crop.toLowerCase().includes(q))
      );
    })
    .slice(0, 5); // Show 3-5 recent conversations

  return (
    <aside className={`sidebar-panel ${isCollapsed ? 'collapsed' : ''}`}>
      {/* Sidebar Header & Collapse Toggle */}
      <div className="sidebar-header-bar">
        {!isCollapsed && <span className="sidebar-heading">{t('navOverview')}</span>}
        <button
          className="collapse-toggle-btn"
          onClick={onToggleCollapse}
          title={isCollapsed ? t('expandSidebar') : t('collapseSidebar')}
        >
          {isCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      {/* Main Farm Navigation */}
      <nav className="sidebar-nav-list">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeView === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item-btn ${isActive ? 'active' : ''}`}
              onClick={() => onSelectView(item.id)}
              title={isCollapsed ? item.label : undefined}
            >
              <Icon size={18} className="nav-icon" />
              {!isCollapsed && <span>{item.label}</span>}
              {!isCollapsed && item.badge && (
                <span className="nav-item-badge">{item.badge}</span>
              )}
            </button>
          );
        })}
      </nav>

      <div className="sidebar-divider" />

      {/* Recent Chats Section (Shown when expanded) */}
      {!isCollapsed && (
        <div className="sidebar-chats-section">
          {/* New Chat Button */}
          <button className="new-chat-btn" onClick={onNewChat}>
            <Plus size={16} />
            <span>{t('newChat')}</span>
          </button>

          {/* Search Conversations Input */}
          <div className="chat-search-input-box">
            <Search size={14} color="var(--text-muted)" />
            <input
              type="text"
              placeholder={t('searchConversations')}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="chats-section-top">
            <span className="sidebar-heading">{t('recentConversations')}</span>
          </div>

          {/* Recent Chats List */}
          <div className="recent-chats-scroll">
            {filteredConversations.length === 0 ? (
              <div style={{ padding: '12px 6px', fontSize: '12px', color: 'var(--text-muted)' }}>
                {t('noConversationsFound')}
              </div>
            ) : (
              filteredConversations.map((conv) => {
                const isActive = activeConversationId === conv.id && activeView === 'agent';
                return (
                  <div
                    key={conv.id}
                    className={`recent-chat-row ${isActive ? 'active' : ''}`}
                    onClick={() => {
                      onSelectConversation(conv.id);
                      onSelectView('agent');
                    }}
                  >
                    <div className="recent-chat-title-box">
                      <MessageSquare size={13} color={isActive ? 'var(--emerald-800)' : 'var(--text-muted)'} />
                      <span>{conv.title || t('newChat')}</span>
                    </div>

                    <div className="recent-chat-actions" onClick={(e) => e.stopPropagation()}>
                      <button
                        className="mini-action-btn"
                        title={t('delete')}
                        onClick={() => onDeleteConversation(conv.id)}
                      >
                        <Trash2 size={12} />
                      </button>
                    </div>
                  </div>
                );
              })
            )}
          </div>

          {/* View All Chats Link */}
          <button className="view-all-chats-link" onClick={onOpenAllChats}>
            {t('viewAllChats')} →
          </button>
        </div>
      )}
    </aside>
  );
}
