import httpx
from fastapi import APIRouter

router = APIRouter(prefix="/external")


@router.get("/catfact")
async def get_external_data():
    """Fetch a random cat fact from an external API."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://catfact.ninja/fact")
        response.raise_for_status()
        data = response.json()
    return data
