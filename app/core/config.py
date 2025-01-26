import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    WB_PARSE_URL = os.environ.get("WB_PARSE_URL")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    PARSER_URL = os.environ.get("PARSER_URL")


settings = Settings()
