from fastapi.exceptions import HTTPException

from app.core.config import settings
from app import schemas

import aiohttp


class LibraryService():
    async def create_purchased_episode(self, episode_id: int, token: str) -> schemas.Episode:
        headers={"Authorization": f"Bearer {token}"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(f"{settings.LIBRARY_SERVICE_BASE_URL}/v1/library/purchased/{episode_id}") as resp:
                if resp.status != 200:
                    raise HTTPException(status_code=resp.status, detail=await resp.text())
                episode_data = await resp.json()
                return schemas.Episode(**episode_data)
