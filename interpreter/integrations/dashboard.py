"""
Real-time Dashboard for Open Interpreter Multi-Agent System

Provides:
- Web UI for monitoring agents
- Real-time updates via WebSocket
- Agent status tracking
- Message inbox viewing
- Issue/Beads management
- File reservation monitoring
"""

import os
import json
import asyncio
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional

from flask import Flask, render_template_string, jsonify, request
from flask_socketio import SocketIO, emit, join_room


# Initialize Flask and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global state
class DashboardState:
    """Global dashboard state."""
    
    def __init__(self):
        self.agents: Dict[str, Dict] = {}
        self.messages: List[Dict] = []
        self.issues: List[Dict] = []
        self.reservations: List[Dict] = []
        self.logs: List[Dict] = []
        self.workflows: Dict[str, Any] = {}
        
    def add_log(self, level: str, message: str, source: str = "system"):
        """Add a log entry."""
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "source": source
        }
        self.logs.append(log)
        # Keep only last 1000 logs
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
        
        # Emit to WebSocket
        socketio.emit('log_update', log, broadcast=True)
        
    def update_agent(self, agent_id: str, data: Dict):
        """Update agent status."""
        self.agents[agent_id] = {
            **self.agents.get(agent_id, {}),
            **data,
            "updated_at": datetime.utcnow().isoformat()
        }
        socketio.emit('agent_update', self.agents[agent_id], broadcast=True)
        
    def add_message(self, message: Dict):
        """Add a message."""
        self.messages.append(message)
        socketio.emit('new_message', message, broadcast=True)
        
    def add_issue(self, issue: Dict):
        """Add an issue."""
        self.issues.append(issue)
        socketio.emit('new_issue', issue, broadcast=True)
        
    def update_issue(self, issue_id: str, data: Dict):
        """Update an issue."""
        for i, issue in enumerate(self.issues):
            if issue.get('id') == issue_id:
                self.issues[i] = {**issue, **data}
                socketio.emit('issue_update', self.issues[i], broadcast=True)
                break


state = DashboardState()


# HTML Template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open Interpreter - Agent Dashboard</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .log-entry { font-family: 'Monaco', 'Menlo', monospace; font-size: 12px; }
        .status-dot { height: 10px; width: 10px; border-radius: 50%; display: inline-block; }
        .status-idle { background-color: #9CA3AF; }
        .status-working { background-color: #10B981; animation: pulse 2s infinite; }
        .status-error { background-color: #EF4444; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .scroll-auto { scrollbar-width: thin; scrollbar-color: #4B5563 #1F2937; }
    </style>
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen">
    <!-- Header -->
    <header class="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                    </svg>
                </div>
                <div>
                    <h1 class="text-xl font-bold">Open Interpreter</h1>
                    <p class="text-sm text-gray-400">Multi-Agent Dashboard</p>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <span class="text-sm text-gray-400" id="connection-status">
                    <span class="status-dot status-idle"></span> Connecting...
                </span>
                <button onclick="refreshAll()" class="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg text-sm">
                    Refresh
                </button>
            </div>
        </div>
    </header>

    <div class="flex h-[calc(100vh-80px)]">
        <!-- Sidebar -->
        <aside class="w-64 bg-gray-800 border-r border-gray-700 p-4">
            <nav class="space-y-2">
                <a href="#" onclick="showTab('overview')" class="tab-btn flex items-center space-x-3 px-4 py-3 rounded-lg bg-gray-700 text-white" data-tab="overview">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
                    </svg>
                    <span>Overview</span>
                </a>
                <a href="#" onclick="showTab('agents')" class="tab-btn flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300" data-tab="agents">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                    <span>Agents</span>
                </a>
                <a href="#" onclick="showTab('messages')" class="tab-btn flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300" data-tab="messages">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                    </svg>
                    <span>Messages</span>
                </a>
                <a href="#" onclick="showTab('issues')" class="tab-btn flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300" data-tab="issues">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
                    </svg>
                    <span>Issues</span>
                </a>
                <a href="#" onclick="showTab('reservations')" class="tab-btn flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300" data-tab="reservations">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                    </svg>
                    <span>Reservations</span>
                </a>
                <a href="#" onclick="showTab('logs')" class="tab-btn flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300" data-tab="logs">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    <span>Logs</span>
                </a>
                <a href="#" onclick="showTab('workflows')" class="tab-btn flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300" data-tab="workflows">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                    </svg>
                    <span>Workflows</span>
                </a>
            </nav>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 overflow-auto p-6">
            <!-- Overview Tab -->
            <div id="tab-overview" class="tab-content">
                <h2 class="text-2xl font-bold mb-6">Dashboard Overview</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <div class="text-3xl font-bold text-blue-400" id="agent-count">0</div>
                        <div class="text-gray-400 text-sm">Active Agents</div>
                    </div>
                    <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <div class="text-3xl font-bold text-green-400" id="message-count">0</div>
                        <div class="text-gray-400 text-sm">Messages</div>
                    </div>
                    <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <div class="text-3xl font-bold text-purple-400" id="issue-count">0</div>
                        <div class="text-gray-400 text-sm">Issues</div>
                    </div>
                    <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <div class="text-3xl font-bold text-yellow-400" id="reservation-count">0</div>
                        <div class="text-gray-400 text-sm">Active Reservations</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <h3 class="text-lg font-semibold mb-4">Recent Activity</h3>
                        <div id="recent-activity" class="space-y-3 max-h-64 overflow-auto scroll-auto">
                            <p class="text-gray-500">No recent activity</p>
                        </div>
                    </div>
                    <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <h3 class="text-lg font-semibold mb-4">Quick Actions</h3>
                        <div class="space-y-3">
                            <button onclick="createIssue()" class="w-full bg-blue-600 hover:bg-blue-700 px-4 py-3 rounded-lg text-left">
                                + Create New Issue
                            </button>
                            <button onclick="registerAgent()" class="w-full bg-green-600 hover:bg-green-700 px-4 py-3 rounded-lg text-left">
                                + Register New Agent
                            </button>
                            <button onclick="sendMessage()" class="w-full bg-purple-600 hover:bg-purple-700 px-4 py-3 rounded-lg text-left">
                                + Send Message
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Agents Tab -->
            <div id="tab-agents" class="tab-content hidden">
                <h2 class="text-2xl font-bold mb-6">Agent Management</h2>
                <div id="agents-list" class="space-y-4"></div>
            </div>

            <!-- Messages Tab -->
            <div id="tab-messages" class="tab-content hidden">
                <h2 class="text-2xl font-bold mb-6">Message Inbox</h2>
                <div id="messages-list" class="space-y-4"></div>
            </div>

            <!-- Issues Tab -->
            <div id="tab-issues" class="tab-content hidden">
                <h2 class="text-2xl font-bold mb-6">Issue Tracker (Beads)</h2>
                <div class="flex space-x-2 mb-4">
                    <button onclick="filterIssues('all')" class="px-4 py-2 bg-gray-700 rounded-lg text-sm">All</button>
                    <button onclick="filterIssues('backlog')" class="px-4 py-2 bg-gray-700 rounded-lg text-sm">Backlog</button>
                    <button onclick="filterIssues('ready')" class="px-4 py-2 bg-gray-700 rounded-lg text-sm">Ready</button>
                    <button onclick="filterIssues('in_progress')" class="px-4 py-2 bg-gray-700 rounded-lg text-sm">In Progress</button>
                    <button onclick="filterIssues('done')" class="px-4 py-2 bg-gray-700 rounded-lg text-sm">Done</button>
                </div>
                <div id="issues-list" class="space-y-4"></div>
            </div>

            <!-- Reservations Tab -->
            <div id="tab-reservations" class="tab-content hidden">
                <h2 class="text-2xl font-bold mb-6">File Reservations</h2>
                <div id="reservations-list" class="space-y-4"></div>
            </div>

            <!-- Logs Tab -->
            <div id="tab-logs" class="tab-content hidden">
                <h2 class="text-2xl font-bold mb-6">System Logs</h2>
                <div id="logs-list" class="bg-gray-800 rounded-xl p-4 max-h-[70vh] overflow-auto scroll-auto font-mono text-sm"></div>
            </div>

            <!-- Workflows Tab -->
            <div id="tab-workflows" class="tab-content hidden">
                <h2 class="text-2xl font-bold mb-6">Workflow Status</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <h3 class="text-lg font-semibold mb-4">🧠 Second Brain</h3>
                        <div class="text-gray-400">
                            <p>Memories: <span id="brain-memories">0</span></p>
                        </div>
                    </div>
                    <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <h3 class="text-lg font-semibold mb-4">☀️ Morning Brief</h3>
                        <div class="text-gray-400">
                            <p>Schedule: <span id="brief-time">8:00 AM</span></p>
                            <p>Channel: <span id="brief-channel">Telegram</span></p>
                        </div>
                    </div>
                    <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <h3 class="text-lg font-semibold mb-4">📺 Content Factory</h3>
                        <div id="factory-agents" class="space-y-2"></div>
                    </div>
                    <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <h3 class="text-lg font-semibold mb-4">🎯 Goal Tracking</h3>
                        <div class="text-gray-400">
                            <p>Goals: <span id="goals-count">0</span></p>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        // Socket.IO connection
        const socket = io();
        
        socket.on('connect', () => {
            document.getElementById('connection-status').innerHTML = 
                '<span class="status-dot status-working"></span> Connected';
            state.add_log('info', 'Dashboard connected');
        });
        
        socket.on('disconnect', () => {
            document.getElementById('connection-status').innerHTML = 
                '<span class="status-dot status-error"></span> Disconnected';
        });

        // Listen for events
        socket.on('agent_update', (data) => {
            updateAgentCard(data);
        });
        
        socket.on('new_message', (data) => {
            addMessageCard(data);
            updateCounts();
        });
        
        socket.on('new_issue', (data) => {
            addIssueCard(data);
            updateCounts();
        });
        
        socket.on('issue_update', (data) => {
            updateIssueCard(data);
        });
        
        socket.on('log_update', (data) => {
            addLogEntry(data);
        });

        // State
        let currentTab = 'overview';

        // Tab management
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(el => {
                el.classList.remove('bg-gray-700', 'text-white');
                el.classList.add('text-gray-300');
            });
            
            document.getElementById('tab-' + tabName).classList.remove('hidden');
            const btn = document.querySelector(`[data-tab="${tabName}"]`);
            btn.classList.add('bg-gray-700', 'text-white');
            btn.classList.remove('text-gray-300');
            
            currentTab = tabName;
            refreshAll();
        }

        // Refresh data
        function refreshAll() {
            fetch('/api/state').then(r => r.json()).then(data => {
                state = data;
                updateCounts();
                updateAgentsList();
                updateMessagesList();
                updateIssuesList();
                updateReservationsList();
                updateWorkflows();
            });
        }

        function updateCounts() {
            document.getElementById('agent-count').textContent = Object.keys(state.agents || {}).length;
            document.getElementById('message-count').textContent = (state.messages || []).length;
            document.getElementById('issue-count').textContent = (state.issues || []).length;
            document.getElementById('reservation-count').textContent = (state.reservations || []).length;
        }

        function updateAgentsList() {
            const container = document.getElementById('agents-list');
            if (!state.agents || Object.keys(state.agents).length === 0) {
                container.innerHTML = '<p class="text-gray-500">No agents registered</p>';
                return;
            }
            container.innerHTML = Object.values(state.agents).map(agent => `
                <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
                    <div class="flex items-center justify-between">
                        <div>
                            <h4 class="font-semibold">${agent.name || 'Unknown'}</h4>
                            <p class="text-sm text-gray-400">${agent.program} / ${agent.model}</p>
                        </div>
                        <span class="status-dot ${agent.status === 'working' ? 'status-working' : 'status-idle'}"></span>
                    </div>
                </div>
            `).join('');
        }

        function updateMessagesList() {
            const container = document.getElementById('messages-list');
            if (!state.messages || state.messages.length === 0) {
                container.innerHTML = '<p class="text-gray-500">No messages</p>';
                return;
            }
            container.innerHTML = state.messages.slice(-10).reverse().map(msg => `
                <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
                    <div class="flex justify-between items-start">
                        <div>
                            <h4 class="font-semibold">${msg.subject}</h4>
                            <p class="text-sm text-gray-400">From: ${msg.sender} → To: ${msg.recipient}</p>
                        </div>
                        <span class="text-xs text-gray-500">${new Date(msg.created_at).toLocaleString()}</span>
                    </div>
                    <p class="mt-2 text-gray-300">${msg.body.substring(0, 100)}...</p>
                </div>
            `).join('');
        }

        function updateIssuesList() {
            const container = document.getElementById('issues-list');
            if (!state.issues || state.issues.length === 0) {
                container.innerHTML = '<p class="text-gray-500">No issues</p>';
                return;
            }
            container.innerHTML = state.issues.map(issue => `
                <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
                    <div class="flex justify-between items-start">
                        <div>
                            <span class="text-xs bg-${getStatusColor(issue.status)}-900 text-${getStatusColor(issue.status)}-300 px-2 py-1 rounded">${issue.status}</span>
                            <h4 class="font-semibold mt-2">${issue.title}</h4>
                            <p class="text-sm text-gray-400">${issue.id}</p>
                        </div>
                        <button onclick="updateIssueStatus('${issue.id}')" class="text-blue-400 hover:text-blue-300">Update</button>
                    </div>
                </div>
            `).join('');
        }

        function getStatusColor(status) {
            const colors = {
                'backlog': 'gray',
                'ready': 'blue',
                'in_progress': 'yellow',
                'done': 'green',
                'blocked': 'red'
            };
            return colors[status] || 'gray';
        }

        function updateReservationsList() {
            const container = document.getElementById('reservations-list');
            if (!state.reservations || state.reservations.length === 0) {
                container.innerHTML = '<p class="text-gray-500">No active reservations</p>';
                return;
            }
            container.innerHTML = state.reservations.map(res => `
                <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
                    <div class="flex justify-between items-start">
                        <div>
                            <h4 class="font-semibold">${res.agent_name}</h4>
                            <p class="text-sm text-gray-400">${res.paths.join(', ')}</p>
                        </div>
                        <span class="text-xs text-yellow-500">${res.status}</span>
                    </div>
                </div>
            `).join('');
        }

        function addLogEntry(log) {
            const container = document.getElementById('logs-list');
            const entry = document.createElement('div');
            entry.className = 'log-entry py-1 border-b border-gray-700';
            entry.innerHTML = `<span class="text-gray-500">[${new Date(log.timestamp).toLocaleTimeString()}]</span> <span class="text-${getLogLevelColor(log.level)}">${log.level.toUpperCase()}</span> <span class="text-gray-300">${log.message}</span>`;
            container.insertBefore(entry, container.firstChild);
        }

        function getLogLevelColor(level) {
            const colors = { 'info': 'blue', 'warning': 'yellow', 'error': 'red', 'success': 'green' };
            return colors[level] || 'gray';
        }

        function updateWorkflows() {
            // Update workflow status
            if (state.workflows) {
                document.getElementById('brain-memories').textContent = state.workflows.second_brain?.memories_count || 0;
                document.getElementById('goals-count').textContent = state.workflows.goals_count || 0;
            }
        }

        // Actions
        function createIssue() {
            const title = prompt('Issue title:');
            if (title) {
                fetch('/api/issues', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({title, description: ''})
                });
            }
        }

        function registerAgent() {
            const name = prompt('Agent name:');
            if (name) {
                fetch('/api/agents', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, program: 'claude', model: 'opus'})
                });
            }
        }

        function sendMessage() {
            const to = prompt('Recipient:');
            const subject = prompt('Subject:');
            const body = prompt('Message:');
            if (to && subject && body) {
                fetch('/api/messages', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({recipient: to, subject, body, sender: 'dashboard'})
                });
            }
        }

        // Initial load
        refreshAll();
    </script>
</body>
</html>
"""


# API Routes
@app.route('/')
def index():
    """Serve the dashboard."""
    return render_template_string(DASHBOARD_HTML)


@app.route('/api/state')
def get_state():
    """Get current dashboard state."""
    return jsonify({
        'agents': state.agents,
        'messages': state.messages,
        'issues': state.issues,
        'reservations': state.reservations,
        'logs': state.logs[-50:],  # Last 50 logs
        'workflows': state.workflows
    })


@app.route('/api/agents', methods=['GET', 'POST'])
def agents():
    """Manage agents."""
    if request.method == 'POST':
        data = request.json
        from interpreter.integrations.agent_mail import get_agent_mail
        mail = get_agent_mail()
        agent = mail.register_agent(
            name=data['name'],
            project_key=data.get('project_key', 'default'),
            program=data.get('program', 'claude'),
            model=data.get('model', 'opus')
        )
        state.update_agent(agent.name, {
            'name': agent.name,
            'program': agent.program,
            'model': agent.model,
            'status': 'idle'
        })
        state.add_log('info', f'Agent registered: {agent.name}', 'agent_mail')
        return jsonify({'success': True, 'agent': agent.__dict__})
    
    return jsonify(state.agents)


@app.route('/api/messages', methods=['GET', 'POST'])
def messages():
    """Manage messages."""
    if request.method == 'POST':
        data = request.json
        from interpreter.integrations.agent_mail import get_agent_mail
        mail = get_agent_mail()
        msg = mail.send_message(
            project_key=data.get('project_key', 'default'),
            sender=data.get('sender', 'dashboard'),
            recipient=data['recipient'],
            subject=data['subject'],
            body=data['body']
        )
        state.add_message({
            'id': msg.id,
            'sender': msg.sender,
            'recipient': msg.recipient,
            'subject': msg.subject,
            'body': msg.body,
            'created_at': msg.created_at.isoformat()
        })
        state.add_log('info', f'Message sent: {msg.subject}', 'agent_mail')
        return jsonify({'success': True})
    
    return jsonify(state.messages)


@app.route('/api/issues', methods=['GET', 'POST'])
def issues():
    """Manage issues (Beads)."""
    if request.method == 'POST':
        data = request.json
        from interpreter.integrations.agent_mail import get_beads
        beads = get_beads()
        issue = beads.create_issue(
            title=data['title'],
            description=data.get('description', '')
        )
        state.add_issue({
            'id': issue.id,
            'title': issue.title,
            'description': issue.description,
            'status': issue.status.value,
            'priority': issue.priority,
            'created_at': issue.created_at.isoformat()
        })
        state.add_log('info', f'Issue created: {issue.title}', 'beads')
        return jsonify({'success': True, 'issue': issue.__dict__})
    
    return jsonify(state.issues)


@app.route('/api/reservations', methods=['GET'])
def reservations():
    """Get active reservations."""
    from interpreter.integrations.agent_mail import get_agent_mail
    mail = get_agent_mail()
    active = mail.get_active_reservations('default')
    return jsonify([{
        'id': r.id,
        'agent_name': r.agent_name,
        'paths': r.paths,
        'status': r.status.value,
        'expires_at': r.expires_at.isoformat()
    } for r in active])


@app.route('/api/workflows/status')
def workflow_status():
    """Get workflow status."""
    from interpreter.integrations.openclaw import get_openclaw
    openclaw = get_openclaw()
    return jsonify(openclaw.get_status())


# Background task to update workflow status
def update_workflow_status():
    """Periodically update workflow status."""
    while True:
        try:
            from interpreter.integrations.openclaw import get_openclaw
            openclaw = get_openclaw()
            state.workflows = openclaw.get_status()
        except Exception as e:
            state.add_log('error', f'Workflow update error: {str(e)}')
        
        socketio.sleep(5)


# SocketIO events
@socketio.on('join')
def on_join(data):
    """Join a room."""
    room = data.get('room', 'dashboard')
    join_room(room)


def start_dashboard(host='0.0.0.0', port=5000):
    """Start the dashboard server."""
    # Start background thread for workflow updates
    threading.Thread(target=update_workflow_status, daemon=True).start()
    
    # Add initial log
    state.add_log('info', 'Dashboard starting...', 'system')
    
    # Run the server
    socketio.run(app, host=host, port=port, debug=False)


if __name__ == '__main__':
    start_dashboard()
