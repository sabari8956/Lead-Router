from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File for local lead storage backup
LEADS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leads_storage.json')

def get_local_leads():
    if not os.path.exists(LEADS_FILE):
        return []
    try:
        with open(LEADS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading local leads: {e}")
        return []

def save_local_lead(lead_data):
    leads = get_local_leads()
    # Add timestamp and ID if missing
    lead_data['created_at'] = datetime.now().isoformat()
    lead_data['id'] = f"local-{int(datetime.now().timestamp())}"
    leads.append(lead_data)
    # Keep only last 100 leads locally
    leads = leads[-100:]
    with open(LEADS_FILE, 'w') as f:
        json.dump(leads, f, indent=4)
    return lead_data

# ClickUp Configuration
CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")
CLICKUP_BASE_URL = "https://api.clickup.com/api/v2"

headers = {
    "Authorization": CLICKUP_API_KEY,
    "Content-Type": "application/json"
}

@app.route('/api/webhook/lead', methods=['POST'])
def receive_lead():
    """Endpoint for the bot to report a new lead discovered"""
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    saved_lead = save_local_lead(data)
    return jsonify({"success": True, "lead": saved_lead})

@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Fetch all leads from local storage and ClickUp"""
    all_leads = []
    
    # 1. Get Local Leads (100% reliable)
    local_leads = get_local_leads()
    for l in local_leads:
        l['source'] = 'Telegram (Local)'
        all_leads.append(l)

    # 2. Get ClickUp Leads (Online)
    try:
        if CLICKUP_API_KEY and CLICKUP_LIST_ID and "pk_" in CLICKUP_API_KEY:
            url = f"{CLICKUP_BASE_URL}/list/{CLICKUP_LIST_ID}/task"
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                tasks = response.json().get('tasks', [])
                for task in tasks:
                    all_leads.append({
                        "id": task.get('id'),
                        "name": task.get('name'),
                        "description": task.get('description', ''),
                        "status": task.get('status', {}).get('status', 'Unknown').upper(),
                        "priority": get_priority_name(task.get('priority')),
                        "created_at": format_timestamp(task.get('date_created')),
                        "source": "ClickUp"
                    })
            else:
                logger.warning(f"ClickUp API returned {response.status_code}")
    except Exception as e:
        logger.error(f"ClickUp fetch error: {e}")

    # Sort by date (newest first)
    all_leads.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return jsonify({
        "success": True,
        "count": len(all_leads),
        "leads": all_leads,
        "config_status": {
            "clickup_connected": bool(CLICKUP_API_KEY and "pk_" in CLICKUP_API_KEY),
            "list_id_set": bool(CLICKUP_LIST_ID and len(CLICKUP_LIST_ID) < 15)
        }
    })

@app.route('/api/leads/<lead_id>', methods=['GET'])
def get_lead_details(lead_id):
    """Fetch details for a specific lead"""
    # 1. Check Local Leads
    local_leads = get_local_leads()
    for lead in local_leads:
        if lead.get('id') == lead_id:
            return jsonify({
                "success": True,
                "lead": {
                    "id": lead.get('id'),
                    "name": lead.get('name'),
                    "description": lead.get('original_text', ''),
                    "status": "TO DO",
                    "priority": "Normal",
                    "created_at": lead.get('created_at'),
                    "updated_at": lead.get('created_at'),
                    "source": "Telegram (Local)"
                }
            })

    # 2. Check ClickUp
    if CLICKUP_API_KEY and CLICKUP_LIST_ID and "pk_" in CLICKUP_API_KEY:
        try:
            url = f"{CLICKUP_BASE_URL}/task/{lead_id}"
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                task = response.json()
                return jsonify({
                    "success": True,
                    "lead": {
                        "id": task.get('id'),
                        "name": task.get('name'),
                        "description": task.get('description', ''),
                        "status": task.get('status', {}).get('status', 'Unknown').upper(),
                        "priority": get_priority_name(task.get('priority')),
                        "created_at": format_timestamp(task.get('date_created')),
                        "updated_at": format_timestamp(task.get('date_updated')),
                        "url": task.get('url'),
                        "source": "ClickUp"
                    }
                })
        except Exception as e:
            logger.error(f"ClickUp fetch error: {e}")

    return jsonify({"success": False, "error": "Lead not found"}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    leads = get_leads().get_json().get('leads', [])
    
    status_counts = {}
    priority_counts = {}
    for lead in leads:
        status = lead.get('status', 'TO DO')
        priority = lead.get('priority', 'Normal')
        status_counts[status] = status_counts.get(status, 0) + 1
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
    return jsonify({
        "success": True,
        "stats": {
            "total_leads": len(leads),
            "by_status": status_counts,
            "by_priority": priority_counts,
            "last_updated": datetime.now().isoformat()
        }
    })

def get_priority_name(priority_value):
    priority_map = {1: "Urgent", 2: "High", 3: "Normal", 4: "Low", None: "Normal"}
    return priority_map.get(priority_value, "Normal")

def format_timestamp(timestamp_ms):
    if not timestamp_ms: return None
    try:
        return datetime.fromtimestamp(int(timestamp_ms) / 1000).isoformat()
    except: return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
