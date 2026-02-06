import aiohttp
from data.data import base_url


async def get_active_work_for_agent():

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.get(f'{base_url}active-works-for-agent/') as resp:
                resp.raise_for_status()
                data = await resp.json()
    except Exception as e:
        print("Failed to fetch AGENT role from API:", e)
        return False

    return data


async def get_installed_works_list(chat_id, status):

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.get(f'{base_url}agent-works/?chat_id={chat_id}&status={status}') as resp:
                resp.raise_for_status()
                data = await resp.json()
    except Exception as e:
        print("Failed to fetch AGENT role from API:", e)
        return False

    return data


async def accept_work(chat_id, work_id):
    payload = {
        "chat_id": chat_id,
        "work_id": work_id,
    }
    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.post(
                f"{base_url}accept-work/",
                json=payload
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


async def complete_work(chat_id, work_id, document_id, image_id):
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field("work_id", str(work_id))
        form.add_field("chat_id", str(chat_id))

        if image_id:
            form.add_field(
                "image",
                open(image_id, "rb"),
                filename=f"complated_work_image.jpg",
                content_type="image/jpeg"
            )


        if document_id:
            form.add_field(
                "document",
                open(document_id, "rb"),
                filename=f"complated_work_document.pdf",
                content_type="application/pdf"
            )

        async with session.post(f'{base_url}complete-work/', data=form) as resp:
            return await resp.json()
