from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.init_db import init_database
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.item import router as item_router
from app.routers.category import router as category_router
from app.routers.holder import router as holder_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(item_router)
app.include_router(category_router)
app.include_router(holder_router)