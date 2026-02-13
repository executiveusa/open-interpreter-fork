"""
Open Interpreter Vercel Serverless API
Main entry point for serverless deployment
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Import integrations conditionally
try:
    from interpreter.integrations.agent_mail import get_agent_mail, get_beads
    from interpreter.integrations.openclaw import get_openclaw
    INTEGRATIONS_AVAILABLE = True
except ImportError:
    INTEGRATIONS_AVAILABLE = False


@app.route('/')
def index():
    """Root endpoint - API info."""
    return jsonify({
        "name": "Open Interpreter API",
        "version": "0.4.3",
        "status": "running",
        "integrations": INTEGRATIONS_AVAILABLE,
        "endpoints": {
            "/api/state": "Get dashboard state",
            "/api/agents": "Manage agents",
            "/api/messages": "Manage messages",
            "/api/issues": "Manage issues (Beads)",
            "/api/workflows/status": "Get workflow status"
        }
    })


@app.route('/api/state')
def get_state():
    """Get current dashboard state."""
    if not INTEGRATIONS_AVAILABLE:
        return jsonify({"error": "Integrations not available"}), 500
    
    openclaw = get_openclaw()
    
    return jsonify({
        "agents": {},
        "messages": [],
        "issues": [],
        "reservations": [],
        "workflows": openclaw.get_status()
    })


@app.route('/api/agents', methods=['GET', 'POST'])
def agents():
    """Manage agents."""
    if request.method == 'POST':
        data = request.json
        if not INTEGRATIONS_AVAILABLE:
            return jsonify({"error": "Integrations not available"}), 500
        
        mail = get_agent_mail()
        agent = mail.register_agent(
            name=data['name'],
            project_key=data.get('project_key', 'default'),
            program=data.get('program', 'claude'),
            model=data.get('model', 'opus')
        )
        return jsonify({"success": True, "agent": {"name": agent.name}})
    
    return jsonify({})


@app.route('/api/messages', methods=['GET', 'POST'])
def messages():
    """Manage messages."""
    if request.method == 'POST':
        data = request.json
        if not INTEGRATIONS_AVAILABLE:
            return jsonify({"error": "Integrations not available"}), 500
        
        mail = get_agent_mail()
        msg = mail.send_message(
            project_key=data.get('project_key', 'default'),
            sender=data.get('sender', 'api'),
            recipient=data['recipient'],
            subject=data['subject'],
            body=data['body']
        )
        return jsonify({"success": True, "message_id": msg.id})
    
    return jsonify([])


@app.route('/api/issues', methods=['GET', 'POST'])
def issues():
    """Manage issues (Beads)."""
    if request.method == 'POST':
        data = request.json
        if not INTEGRATIONS_AVAILABLE:
            return jsonify({"error": "Integrations not available"}), 500
        
        beads = get_beads()
        issue = beads.create_issue(
            title=data['title'],
            description=data.get('description', '')
        )
        return jsonify({
            "success": True, 
            "issue": {
                "id": issue.id,
                "title": issue.title,
                "status": issue.status.value
            }
        })
    
    return jsonify([])


@app.route('/api/workflows/status')
def workflow_status():
    """Get workflow status."""
    if not INTEGRATIONS_AVAILABLE:
        return jsonify({"error": "Integrations not available"}), 500
    
    openclaw = get_openclaw()
    return jsonify(openclaw.get_status())


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


# Vercel requires this handler
def handler(event, context):
    """AWS Lambda style handler for Vercel."""
    return app(event, context)


# For local development
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
