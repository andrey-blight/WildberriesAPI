class Settings:
    WB_PARSE_URL = "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"
    DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/wildberries_db"


settings = Settings()
