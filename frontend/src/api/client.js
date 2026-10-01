// API Client for Rythu Agent Backend
const API_BASE = '/api';

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function sendChatMessage(message, { farmerId = 'farmer-001', sessionId = null, conversationId = null, language = 'en', forceDemo = false } = {}) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      farmer_id: farmerId,
      session_id: sessionId,
      conversation_id: conversationId,
      language: language,
      force_demo_mode: forceDemo
    })
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.statusText}`);
  }
  return res.json();
}

export async function confirmAction(actionId, farmerId = 'farmer-001', sessionId = '', approved = true) {
  const res = await fetch(`${API_BASE}/action/confirm`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action_id: actionId,
      farmer_id: farmerId,
      session_id: sessionId,
      approved
    })
  });
  if (!res.ok) {
    throw new Error(`Action confirmation failed: ${res.statusText}`);
  }
  return res.json();
}

export async function getFarmerProfile(farmerId = 'farmer-001') {
  const res = await fetch(`${API_BASE}/farmer/${farmerId}`);
  if (!res.ok) throw new Error('Farmer not found');
  return res.json();
}

export async function updateFarmerProfile(farmerId, updates) {
  const res = await fetch(`${API_BASE}/farmer/${farmerId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
  });
  if (!res.ok) throw new Error('Update failed');
  return res.json();
}

export async function getMarketPrices(crop = 'tomato', location = 'Vijayawada', demo = true) {
  const res = await fetch(`${API_BASE}/market?crop=${encodeURIComponent(crop)}&location=${encodeURIComponent(location)}&demo=${demo}`);
  return res.json();
}

export async function getWeather(location = 'Vijayawada', demo = true) {
  const res = await fetch(`${API_BASE}/weather?location=${encodeURIComponent(location)}&demo=${demo}`);
  return res.json();
}

export async function getServices(query = 'all schemes', language = 'en') {
  const res = await fetch(`${API_BASE}/services?query=${encodeURIComponent(query)}&language=${encodeURIComponent(language)}`);
  return res.json();
}

// Conversation Management APIs
export async function listConversations(farmerId = 'farmer-001', includeArchived = false) {
  const res = await fetch(`${API_BASE}/conversations?farmer_id=${encodeURIComponent(farmerId)}&include_archived=${includeArchived}`);
  if (!res.ok) throw new Error('Failed to load conversations');
  return res.json();
}

export async function createConversation(farmerId = 'farmer-001', title = 'New Chat', language = 'en') {
  const res = await fetch(`${API_BASE}/conversations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ farmer_id: farmerId, title, language })
  });
  if (!res.ok) throw new Error('Failed to create conversation');
  return res.json();
}

export async function getConversation(conversationId) {
  const res = await fetch(`${API_BASE}/conversations/${encodeURIComponent(conversationId)}`);
  if (!res.ok) throw new Error('Failed to fetch conversation');
  return res.json();
}

export async function updateConversation(conversationId, updates) {
  const res = await fetch(`${API_BASE}/conversations/${encodeURIComponent(conversationId)}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
  });
  if (!res.ok) throw new Error('Failed to update conversation');
  return res.json();
}

export async function deleteConversation(conversationId) {
  const res = await fetch(`${API_BASE}/conversations/${encodeURIComponent(conversationId)}`, {
    method: 'DELETE'
  });
  if (!res.ok) throw new Error('Failed to delete conversation');
  return res.json();
}

export async function archiveConversation(conversationId, archived = true) {
  const res = await fetch(`${API_BASE}/conversations/${encodeURIComponent(conversationId)}/archive?archived=${archived}`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to archive conversation');
  return res.json();
}

export async function searchConversations(query, farmerId = 'farmer-001') {
  const res = await fetch(`${API_BASE}/conversations/search?q=${encodeURIComponent(query)}&farmer_id=${encodeURIComponent(farmerId)}`);
  if (!res.ok) throw new Error('Failed to search conversations');
  return res.json();
}

export async function getConversationActions(conversationId) {
  const res = await fetch(`${API_BASE}/conversations/${encodeURIComponent(conversationId)}/actions`);
  if (!res.ok) return [];
  return res.json();
}
