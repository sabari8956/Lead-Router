import requests
import json
import os

class ClickUpClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def create_task(self, list_id, lead_data):
        """
        Creates a task in ClickUp from lead data.
        """
        url = f"{self.base_url}/list/{list_id}/task"

        payload = {
            "name": f"Lead: {lead_data['name']} - {lead_data['intent']}",
            "description": f"**Phone**: {lead_data['phone'] or 'N/A'}\n**Intent**: {lead_data['intent']}\n\n**Original Message**:\n{lead_data['original_text']}",
            "priority": 3,  # Normal
            "status": "TO DO"
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating ClickUp task: {e}")
            if response is not None:
                print(f"Response: {response.text}")
            return None
