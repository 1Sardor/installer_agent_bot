import aiohttp
from data.data import base_url

async def get_razxod_list():

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.get(f'{base_url}razxod/') as resp:
                resp.raise_for_status()
                data = await resp.json()
    except Exception as e:
        print("Failed to fetch CEO role from API:", e)
        return False

    return data


async def create_razxod(miqdor, izoh, image):
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field("miqdor", str(miqdor))
        form.add_field("izoh", izoh)

        if image:
            form.add_field(
                "image",
                open(image, "rb"),
                filename=f"razxod.jpg",
                content_type="image/jpeg"
            )

        async with session.post(f'{base_url}razxod/', data=form) as resp:
            return await resp.json()
