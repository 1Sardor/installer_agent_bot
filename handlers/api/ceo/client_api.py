import aiohttp
from data.data import base_url

async def get_client_list():

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.get(f'{base_url}clients/') as resp:
                resp.raise_for_status()
                data = await resp.json()
    except Exception as e:
        print("Failed to fetch CEO role from API:", e)
        return False

    return data


async def create_client(full_name, phone, address):
    payload = {
        "full_name": full_name,
        "phone": phone,
        "address": address
    }

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.post(
                f"{base_url}clients/",
                json=payload
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

