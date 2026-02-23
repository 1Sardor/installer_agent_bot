import aiohttp
from data.data import base_url

async def save_rating(client_id, rating, work_id):
    payload = {
        "client_id": client_id,
        "rating": rating,
        "work_id": work_id,
    }

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.post(
                f"{base_url}save-rating/",
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

