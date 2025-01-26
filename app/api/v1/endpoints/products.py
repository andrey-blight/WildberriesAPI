import httpx
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas import Product, ProductInDB, ProductResponse
from app.db.models import create_product
from app.db.session import get_db
from app.core import settings, scheduler
from app.core.scheduler import send_http_request

router = APIRouter()


def _extract_product_fields(product_json: dict) -> dict:
    product = product_json["data"]["products"][0]

    resp_json = {
        "artikul": product["id"],
        "name": product["name"],
        "price": product["salePriceU"] / 100,
        "rating": product["reviewRating"],
        "count": product["totalQuantity"]
    }
    return resp_json


@router.post("/products", status_code=201, response_model=ProductResponse)
async def parse_product(product: Product, db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(settings.WB_PARSE_URL.format(artikul=product.artikul))

        if response.status_code != 200:
            raise HTTPException(status_code=503, detail="WB API error")

        product_json = response.json()

    product = ProductInDB(**_extract_product_fields(product_json))

    print(product)

    return await create_product(db, product)


@router.get("/subscribe/{artikul}", status_code=200)
async def subscribe(artikul: int):
    task_id = str(artikul)

    if not scheduler.get_job(task_id):
        scheduler.add_job(
            send_http_request,
            'interval',
            minutes=10,
            id=task_id,
            args=[artikul],
            replace_existing=True
        )

    return f"Created task {task_id}"
