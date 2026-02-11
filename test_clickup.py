import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CLICKUP_API_KEY")
list_id = os.getenv("CLICKUP_LIST_ID")

headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
}

try:
    # Test getting user info (verifies key)
    user_url = "https://api.clickup.com/api/v2/user"
    user_resp = requests.get(user_url, headers=headers)
    if user_resp.status_code == 200:
        print("ClickUp API Key is working!")
        user_data = user_resp.json()
        print(f"Authenticated as: {user_data['user']['username']}")
    else:
        print(f"ClickUp API Key failed: {user_resp.status_code} - {user_resp.text}")

    # Test List ID
    if list_id:
        list_url = f"https://api.clickup.com/api/v2/list/{list_id}"
        list_resp = requests.get(list_url, headers=headers)
        if list_resp.status_code == 200:
            print(f"ClickUp List ID {list_id} is valid!")
        else:
            print(f"ClickUp List ID {list_id} failed: {list_resp.status_code} - {list_resp.text}")
except Exception as e:
    print(f"ClickUp test failed: {e}")
