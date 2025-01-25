from fastapi import APIRouter

router = APIRouter()


@router.post("/products")
async def parse_product(product):
    pass


@router.get("/subscribe/{artikul}")
async def subscribe(artikul: int):
    pass
