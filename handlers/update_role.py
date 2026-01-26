from data.data import base_url
import json
import requests

ROLES_FILE = "data/db.json"
DJANGO_API_CEO = f"http://{base_url}/users/"

def load_roles():
    try:
        with open(ROLES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_roles(roles):
    with open(ROLES_FILE, "w") as f:
        json.dump(roles, f, indent=4)

async def update_ceo_role():
    try:
        r = requests.get(DJANGO_API_CEO, timeout=5)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print("Failed to fetch CEO role from API:", e)
        return False

    user = str(data.get("user"))
    if not user:
        print("No chat_id returned from API")
        return False
    roles = load_roles()
    for i in user:
        roles[i['chat_id']] = i['role']
    save_roles(roles)
    return True