import aiohttp
from data.data import base_url

async def get_active_works():

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.get(f'{base_url}active-works/', ssl=False) as resp:
                resp.raise_for_status()
                data = await resp.json()
    except Exception as e:
        print("Failed to fetch CEO role from API:", e)
        return False

    return data


async def get_works_list():

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.get(f'{base_url}works/', ssl=False) as resp:
                resp.raise_for_status()
                data = await resp.json()
    except Exception as e:
        print("Failed to fetch CEO role from API:", e)
        return False

    return data


async def create_work(chat_id, work_type, address, client_name, client_phone, izoh, finish_date):
    payload = {
        "chat_id": chat_id,
        "work_type": work_type,
        "address": address,
        "client_name": client_name,
        "client_phone": client_phone,
        "izoh": izoh,
        "finish_date": str(finish_date),
    }
    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.post(
                f"{base_url}works/",
                json=payload, ssl=False
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
    except aiohttp.ClientResponseError as e:
        print("API error:", e.status, e.message)
        return None
    except Exception as e:
        print("Failed to create work:", e)
        return None

    return data

