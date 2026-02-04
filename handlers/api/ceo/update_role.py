from data.data import base_url
import json
import aiohttp

ROLES_FILE = "data/db.json"
DJANGO_API_CEO = f"{base_url}users/"


def load_roles():
    try:
        with open(ROLES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_roles(roles):
    with open(ROLES_FILE, "w") as f:
        json.dump(roles, f, indent=4)


def get_status(status):
    if status == 1:
        return "ceo"
    if status == 2:
        return "agent"
    if status == 3:
        return "seller"
    return None


async def update_ceo_role():
    roles = load_roles()

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.get(DJANGO_API_CEO) as resp:
                resp.raise_for_status()
                data = await resp.json()
    except Exception as e:
        print("Failed to fetch CEO role from API:", e)
        return False

    if not isinstance(data, list):
        print("Invalid API response:", data)
        return False
    print(data)
    for item in data:
        chat_id = item.get("chat_id")
        status = item.get("status_code")

        if chat_id is None or status is None:
            continue

        role = get_status(int(status))
        if role:
            roles[str(chat_id)] = role

    save_roles(roles)

    print("ROLES SAVED:", roles)
    return True
