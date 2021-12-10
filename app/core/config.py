from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator
from typing import List, Optional, Dict, Any

import base64
import os

from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = os.getenv("API_V1_STR","/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    IDENTITY_SERVICE_BASE_URL = os.getenv("IDENTITY_SERVICE_BASE_URL")
    TOKEN_URL = os.getenv("TOKEN_URL")

    TOSS_BASE_URL = os.getenv("TOSS_BASE_URL")    
    TOSS_SECRET_KEY: str = os.getenv("TOSS_SECRET_KEY")
    TOSS_AUTHORIZATION = base64.b64encode(
        f'{TOSS_SECRET_KEY}:'.encode("utf-8")).decode('utf-8')

    MAIN_SERVICE_BASE_URL = os.getenv("MAIN_SERVICE_BASE_URL")
    LIBRARY_SERVICE_BASE_URL = os.getenv("LIBRARY_SERVICE_BASE_URL")

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

settings = Settings()
