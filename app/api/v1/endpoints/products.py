import asyncio

import httpx
from fastapi import APIRouter, HTTPException

from app.db.schemas import Product
from app.core import WB_PARSE_URL

router = APIRouter()


@router.post("/products", status_code=201)
async def parse_product(product: Product):
    print(product.artikul)

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(WB_PARSE_URL.format(artikul=product.artikul))

        if response.status_code != 200:
            raise HTTPException(status_code=503, detail="WB API error")

        product_json = response.json()

    print(product_json)


@router.get("/subscribe/{artikul}")
async def subscribe(artikul: int):
    pass
