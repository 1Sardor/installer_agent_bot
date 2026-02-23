import aiohttp
from data.data import base_url

async def get_unrated_work(chat_id):

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.get(f'{base_url}unrated-work/?chat_id={chat_id}', ssl=False) as resp:
                resp.raise_for_status()
                data = await resp.json()
    except Exception as e:
        return False

    return data
