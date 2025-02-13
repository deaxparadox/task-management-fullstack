from fastapi import FastAPI

from .log import logging
from .routes import index, auth

app = FastAPI()

app.include_router(index.router, prefix="/api")
app.include_router(auth.router, prefix="/api/auth")