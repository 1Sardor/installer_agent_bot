import aiohttp
from data.data import base_url

def check_phone(phone):
    if phone.startswith("+998"):
        phone = phone.replace("+998", "")
    elif phone.startswith("998"):
        phone = phone.replace("998", "")
    return phone

async def connect_api(phone, chat_id):
    payload = {
        "phone": check_phone(phone),
        "chat_id": chat_id,
    }

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.post(
                f"{base_url}connect-chat-id/",
                json=payload, ssl=False
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()

    except aiohttp.ClientResponseError as e:
        print("API error:", e.status, e.message)
        return None
    except Exception as e:
        print("Failed to create user:", e)
        return None

    return data

