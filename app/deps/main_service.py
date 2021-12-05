from fastapi.exceptions import HTTPException

from app.core.config import settings
from app import schemas

import aiohttp


class MainService():
    async def get_episode(self, episode_id: int) -> schemas.Episode:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.MAIN_SERVICE_BASE_URL}/v1/episodes/{episode_id}") as resp:
                if resp.status != 200:
                    raise HTTPException(status_code=resp.status, detail=await resp.text())
                episode_data = await resp.json()
                return schemas.Episode(**episode_data)

    
    async def get_series(self, series_id: int) -> schemas.Series:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.MAIN_SERVICE_BASE_URL}/v1/serieses/{series_id}") as resp:
                if resp.status != 200:
                    raise HTTPException(status_code=resp.status, detail=await resp.text())
                episode_data = await resp.json()
                return schemas.Series(**episode_data)
