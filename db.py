from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

engine = create_async_engine(url=os.getenv("DATABASE_URL"), echo=True)
