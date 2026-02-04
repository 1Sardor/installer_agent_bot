from pathlib import Path
from config import bot

async def download_image(file_id):
    file = await bot.get_file(file_id)

    folder = Path("media/razxod")
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / f"{file.file_unique_id}.jpg"
    await bot.download_file(file.file_path, destination=file_path)

    return str(file_path)
