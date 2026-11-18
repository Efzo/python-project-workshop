import asyncio
from dataclasses import dataclass
from hmac import compare_digest
from os import environ
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class Settings:
    token: str


def load_settings():
    return Settings(token=environ.get("METRICS_TOKEN", ""))


def verify_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    settings: Annotated[Settings, Depends(load_settings)],
):
    if not settings.token:
        raise HTTPException(status_code=503, detail="Metrics token is not configured")
    if credentials is None or not compare_digest(
        credentials.credentials.encode(), settings.token.encode()
    ):
        raise HTTPException(
            status_code=401, detail="Invalid bearer token", headers={"WWW-Authenticate": "Bearer"}
        )


async def read_metric(name: str, value: int):
    await asyncio.sleep(0.05)
    return name, value


app = FastAPI(title="Protected Metrics API")


@app.get("/metrics", dependencies=[Depends(verify_token)])
async def metrics():
    try:
        async with asyncio.timeout(1):
            results = await asyncio.gather(read_metric("queued", 3), read_metric("ready", 7))
    except TimeoutError as error:
        raise HTTPException(status_code=504, detail="Metrics deadline exceeded") from error
    return dict(results)
