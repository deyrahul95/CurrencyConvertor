from fastapi import FastAPI
import logging

from routes import router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(router=router)
