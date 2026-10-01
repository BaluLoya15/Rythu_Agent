import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/layout/Header';
import Sidebar from './components/layout/Sidebar';
import FarmIntelligencePanel from './components/layout/FarmIntelligencePanel';

import FarmOverview from './components/dashboard/FarmOverview';
import AgentWorkspace from './components/agent/AgentWorkspace';
import CropsView from './components/crops/CropsView';
import MarketDashboard from './components/market/MarketDashboard';
import WeatherDashboard from './components/weather/WeatherDashboard';
import ServicesDashboard from './components/services/ServicesDashboard';

import FarmerProfileDrawer from './components/profile/FarmerProfileDrawer';
import DevTestingModal from './components/DevTestingModal';
import AllChatsModal from './components/modals/AllChatsModal';

import {
  checkHealth,
  getFarmerProfile,
  updateFarmerProfile,
  getWeather,
  getMarketPrices,
  sendChatMessage,
  confirmAction,
  listConversations,
  createConversation,
  getConversation,
  deleteConversation,
  getConversationActions
} from './api/client';
import { useLanguage } from './i18n';

export default function App() {
  const { language, t } = useLanguage();

  // Active View: 'overview' (default) | 'agent' | 'crops' | 'market' | 'weather' | 'services' | 'sources'
  const [activeView, setActiveView] = useState('overview');

  // Application Data States
  const [farmer, setFarmer] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [marketData, setMarketData] = useState(null);

  // Conversations & Agent State
  const [conversations, setConversations] = useState([]);
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [latestResponse, setLatestResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [actionStatusMap, setActionStatusMap] = useState({});

  // Layout & Modal States
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isFarmerModalOpen, setIsFarmerModalOpen] = useState(false);
  const [isDevModalOpen, setIsDevModalOpen] = useState(false);
  const [isAllChatsModalOpen, setIsAllChatsModalOpen] = useState(false);
  const [forceDemo, setForceDemo] = useState(false); // LIVE FIRST DEFAULT

  // Load conversations list
  const refreshConversations = useCallback(async (farmerId = 'farmer-001') => {
    try {
      const list = await listConversations(farmerId, true);
      setConversations(list || []);
      return list;
    } catch (err) {
      console.error('Failed to load conversations:', err);
      return [];
    }
  }, []);

  // Load a single conversation and restore its messages
  const loadConversation = useCallback(async (convId) => {
    if (!convId) return;
    try {
      const detail = await getConversation(convId);
      setActiveConversationId(convId);

      const msgs = (detail.messages || []).map((m) => ({
        id: m.id,
        role: m.role,
        content: m.content,
        tool_trace: m.tool_trace_json
          ? typeof m.tool_trace_json === 'string'
            ? JSON.parse(m.tool_trace_json)
            : m.tool_trace_json
          : [],
        action_plan: m.action_plan_json
          ? typeof m.action_plan_json === 'string'
            ? JSON.parse(m.action_plan_json)
            : m.action_plan_json
          : null,
        sources: m.sources_json
          ? typeof m.sources_json === 'string'
            ? JSON.parse(m.sources_json)
            : m.sources_json
          : [],
        proposed_actions: m.proposed_actions_json
          ? typeof m.proposed_actions_json === 'string'
            ? JSON.parse(m.proposed_actions_json)
            : m.proposed_actions_json
          : []
      }));

      setMessages(msgs);

      // Restore latest response from assistant turn
      const latestAssistant = [...msgs].reverse().find((m) => m.role === 'assistant');
      if (latestAssistant) {
        setLatestResponse({
          action_plan: latestAssistant.action_plan,
          tool_trace: latestAssistant.tool_trace,
          task_plan: [],
          rag_sources: latestAssistant.sources,
          intent: detail.context?.last_intent || 'AGRICULTURAL_PLANNING'
        });
      } else {
        setLatestResponse(null);
      }

      // Load action statuses
      try {
        const acts = await getConversationActions(convId);
        const map = {};
        acts.forEach((a) => {
          map[a.action_id] = a.status;
        });
        setActionStatusMap(map);
      } catch (e) {
        // ignore
      }
    } catch (err) {
      console.error('Failed to load conversation details:', err);
    }
  }, []);

  // Create + New Chat and switch to Agent Workspace
  const handleNewChat = useCallback(async () => {
    try {
      const farmerId = farmer?.id || 'farmer-001';
      const created = await createConversation(farmerId, t('newChat'), language);
      setConversations((prev) => [created, ...prev]);
      setActiveConversationId(created.id);
      setMessages([]);
      setLatestResponse(null);
      setActiveView('agent');
    } catch (err) {
      console.error('Failed to create new chat:', err);
    }
  }, [farmer, language, t]);

  // Initial Load: health, farmer profile, live weather, live market, conversations
  useEffect(() => {
    async function init() {
      // 1. Farmer Profile
      let currentFarmer = null;
      try {
        currentFarmer = await getFarmerProfile('farmer-001');
        setFarmer(currentFarmer);
      } catch (err) {
        currentFarmer = {
          id: 'farmer-001',
          name: 'Venkat Rao',
          location: 'Vijayawada, Andhra Pradesh',
          district: 'Krishna',
          land_area: '2.0 Acres',
          current_crop: 'Paddy',
          crops: ['Paddy'],
          crop_variety: 'BPT-5204 (Samba Mahsuri)',
          crop_stage: 'Tillering & Panicle Initiation (40-45 days)',
          irrigation_type: 'Canal & Furrow Irrigation',
          farming_type: 'Small & Marginal Farmer'
        };
        setFarmer(currentFarmer);
      }

      // 2. Live Weather (Open-Meteo)
      try {
        const wData = await getWeather(currentFarmer?.district || 'Vijayawada', false);
        setWeatherData(wData);
      } catch (e) {
        console.warn('Weather fetch failed, will retry');
      }

      // 3. Live Market
      try {
        const mData = await getMarketPrices((currentFarmer?.current_crop || 'paddy').toLowerCase(), currentFarmer?.district || 'Vijayawada', false);
        setMarketData(mData);
      } catch (e) {
        console.warn('Market fetch failed, will retry');
      }

      // 4. Conversations List
      const list = await refreshConversations(currentFarmer?.id || 'farmer-001');
      if (list && list.length > 0) {
        const firstOne = list.find((c) => !c.archived) || list[0];
        loadConversation(firstOne.id);
      } else {
        try {
          const created = await createConversation(currentFarmer?.id || 'farmer-001', 'New Chat', 'en');
          setConversations([created]);
          setActiveConversationId(created.id);
        } catch (e) {
          // ignore
        }
      }
    }
    init();
  }, [refreshConversations, loadConversation]);

  // Handle keyboard shortcut for dev modal (Ctrl+Shift+D)
  useEffect(() => {
    if (window.location.search.includes('dev=true')) {
      setIsDevModalOpen(true);
    }
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.altKey) && e.shiftKey && (e.key === 'D' || e.key === 'd')) {
        setIsDevModalOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Send message to real AI agent
  const handleSendMessage = async (text) => {
    if (!text.trim() || isLoading) return;

    let targetConvId = activeConversationId;
    if (!targetConvId) {
      try {
        const created = await createConversation(farmer?.id || 'farmer-001', t('newChat'), language);
        targetConvId = created.id;
        setActiveConversationId(targetConvId);
        setConversations((prev) => [created, ...prev]);
      } catch (e) {
        console.error('Failed to auto-create conversation', e);
      }
    }

    // Append user message immediately
    const tempUserMsg = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: text
    };
    setMessages((prev) => [...prev, tempUserMsg]);
    setIsLoading(true);

    try {
      const res = await sendChatMessage(text, {
        farmerId: farmer?.id || 'farmer-001',
        conversationId: targetConvId,
        language: language,
        forceDemo: forceDemo
      });

      setLatestResponse(res);

      // Append assistant message
      const assistantMsg = {
        id: `asst-${Date.now()}`,
        role: 'assistant',
        content: res.markdown_reply,
        tool_trace: res.tool_trace || [],
        action_plan: res.action_plan,
        sources: res.rag_sources || [],
        proposed_actions: res.proposed_actions || []
      };
      setMessages((prev) => [...prev, assistantMsg]);

      // Refresh conversations list to update title
      await refreshConversations(farmer?.id || 'farmer-001');
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          role: 'assistant',
          content: `⚠️ **${t('unavailable')}**: ${t('networkError')}`
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Trigger prompt from copilot card or crop card -> switches to agent and submits query
  const handleTriggerAgentPrompt = (queryText) => {
    setActiveView('agent');
    handleSendMessage(queryText);
  };

  // Handle human-in-the-loop action confirmation
  const handleConfirmAction = async (actionId, approved) => {
    try {
      const res = await confirmAction(
        actionId,
        farmer?.id || 'farmer-001',
        activeConversationId || '',
        approved
      );
      setActionStatusMap((prev) => ({ ...prev, [actionId]: res.status }));

      const confirmMsg = {
        id: `act-${Date.now()}`,
        role: 'assistant',
        content: approved
          ? `✅ **${t('actionCompleted')}:** ${res.message}`
          : `❌ **${t('decline')}:** ${res.message}`,
        proposed_actions: []
      };
      setMessages((prev) => [...prev, confirmMsg]);
    } catch (err) {
      alert(`${t('confirmationFailed')}: ${err.message}`);
    }
  };

  // Handle deleting conversation
  const handleDeleteConversation = async (convId) => {
    try {
      await deleteConversation(convId);
      const remaining = conversations.filter((c) => c.id !== convId);
      setConversations(remaining);

      if (activeConversationId === convId) {
        if (remaining.length > 0) {
          loadConversation(remaining[0].id);
        } else {
          handleNewChat();
        }
      }
    } catch (err) {
      console.error('Failed to delete conversation:', err);
    }
  };

  // Handle saving farmer profile
  const handleSaveFarmerProfile = async (updates) => {
    try {
      const updated = await updateFarmerProfile(farmer?.id || 'farmer-001', updates);
      const newFarmer = updated || { ...farmer, ...updates };
      setFarmer(newFarmer);

      // Refresh live weather and market for newly saved crop & location
      try {
        const wData = await getWeather(newFarmer.district || newFarmer.location || 'Vijayawada', false);
        setWeatherData(wData);
      } catch (e) {
        // keep current
      }
      try {
        const mData = await getMarketPrices(
          (newFarmer.current_crop || 'paddy').toLowerCase(),
          newFarmer.district || newFarmer.location || 'Vijayawada',
          false
        );
        setMarketData(mData);
      } catch (e) {
        // keep current
      }
      return newFarmer;
    } catch (err) {
      console.error('Profile update failed:', err);
      const fallback = { ...farmer, ...updates };
      setFarmer(fallback);
      return fallback;
    }
  };

  return (
    <div className="app-shell">
      {/* 1. Global Command Header (Farmer Mode by default, no visible dev button) */}
      <Header
        farmer={farmer}
        onOpenFarmerModal={() => setIsFarmerModalOpen(true)}
      />

      {/* 2. Main Workspace: Sidebar + Central Content + Right Intelligence Panel */}
      <div className="workspace-container">
        {/* Left Navigation Sidebar */}
        <Sidebar
          activeView={activeView}
          onSelectView={setActiveView}
          conversations={conversations}
          activeConversationId={activeConversationId}
          onSelectConversation={loadConversation}
          onNewChat={handleNewChat}
          onDeleteConversation={handleDeleteConversation}
          onOpenAllChats={() => setIsAllChatsModalOpen(true)}
          isCollapsed={isSidebarCollapsed}
          onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        />

        {/* Center Main Viewport */}
        <main className="main-content-viewport">
          {activeView === 'overview' && (
            <FarmOverview
              farmer={farmer}
              weatherData={weatherData}
              marketData={marketData}
              onTriggerAgentPrompt={handleTriggerAgentPrompt}
              onNavigateView={setActiveView}
              onConfirmAction={handleConfirmAction}
            />
          )}

          {activeView === 'agent' && (
            <AgentWorkspace
              farmer={farmer}
              messages={messages}
              isLoading={isLoading}
              latestResponse={latestResponse}
              onSendMessage={handleSendMessage}
              onConfirmAction={handleConfirmAction}
              actionStatusMap={actionStatusMap}
            />
          )}

          {activeView === 'crops' && (
            <CropsView
              farmer={farmer}
              onTriggerAgentPrompt={handleTriggerAgentPrompt}
            />
          )}

          {activeView === 'market' && (
            <MarketDashboard
              farmer={farmer}
              onTriggerAgentPrompt={handleTriggerAgentPrompt}
            />
          )}

          {activeView === 'weather' && (
            <WeatherDashboard
              farmer={farmer}
              onTriggerAgentPrompt={handleTriggerAgentPrompt}
            />
          )}

          {activeView === 'services' && (
            <ServicesDashboard
              farmer={farmer}
              onTriggerAgentPrompt={handleTriggerAgentPrompt}
            />
          )}
        </main>

        {/* Right-Side Live Farm Intelligence Panel */}
        <FarmIntelligencePanel
          farmer={farmer}
          weatherData={weatherData}
          marketData={marketData}
          activeActionsCount={3}
          onNavigateView={setActiveView}
        />
      </div>

      {/* Premium Right-Side Farm Profile Drawer */}
      <FarmerProfileDrawer
        farmer={farmer}
        isOpen={isFarmerModalOpen}
        onClose={() => setIsFarmerModalOpen(false)}
        onSave={handleSaveFarmerProfile}
      />

      <DevTestingModal
        isOpen={isDevModalOpen}
        onClose={() => setIsDevModalOpen(false)}
        onRunScenario={handleSendMessage}
        forceDemo={forceDemo}
        setForceDemo={setForceDemo}
      />

      <AllChatsModal
        isOpen={isAllChatsModalOpen}
        onClose={() => setIsAllChatsModalOpen(false)}
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={(convId) => {
          loadConversation(convId);
          setActiveView('agent');
        }}
        onDeleteConversation={handleDeleteConversation}
      />
    </div>
  );
}
