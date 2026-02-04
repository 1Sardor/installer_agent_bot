import aiohttp
from data.data import base_url

async def get_statistics():

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.get(f'{base_url}statistics/') as resp:
                resp.raise_for_status()
                data = await resp.json()
    except Exception as e:
        print("Failed to fetch CEO role from API:", e)
        return False

    return data