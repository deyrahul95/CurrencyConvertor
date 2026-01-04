from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from routes import router
from db.database import init_db_and_seed

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db_and_seed()
    yield
    # shutdown


app = FastAPI()

app.include_router(router=router)
