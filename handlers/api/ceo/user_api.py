import aiohttp
from data.data import base_url

async def get_user_list():

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.get(f'{base_url}users/') as resp:
                resp.raise_for_status()
                data = await resp.json()
    except Exception as e:
        print("Failed to fetch CEO role from API:", e)
        return False

    return data

async def create_user(full_name, chat_id, status):
    payload = {
        "full_name": full_name,
        "chat_id": chat_id,
        "status": status
    }

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.post(
                f"{base_url}users/",
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


async def update_user(
    user_id: int,
    full_name: str | None = None,
    chat_id: int | None = None,
    status: int | None = None,
):
    payload = {}

    if full_name is not None:
        payload["full_name"] = full_name
    if chat_id is not None:
        payload["chat_id"] = chat_id
    if status is not None:
        payload["status"] = status

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.patch(
                f"{base_url}users/{user_id}/",
                json=payload
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()

    except aiohttp.ClientResponseError as e:
        print("API error:", e.status, e.message)
        return None
    except Exception as e:
        print("Failed to update user:", e)
        return None

    return data


async def user_delete(obj_id: int):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
            async with session.delete(f"{base_url}users/{obj_id}/") as resp:
                if resp.status in (200, 204):
                    return True
                resp.raise_for_status()
                return True
    except Exception as e:
        print("Generic delete error:", e)
        return False
