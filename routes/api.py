import aiosqlite
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from rich.console import Console

# --- Constants --- #

app = APIRouter(tags=["API"], prefix="/api")
limiter = Limiter(key_func=get_remote_address)
console = Console()

# --- Classes --- #

class Ping(BaseModel):
    status: bool = True

# --- Routes --- #

@limiter.limit("1/5minutes")
@app.get("/ping", response_model=list[Ping])
async def ping() -> dict:
    return {"status":True}

# -------------- #
