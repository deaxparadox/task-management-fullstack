from fastapi import FastAPI

from .routes import index

app = FastAPI()

app.include_router(index.router, prefix="/api")

