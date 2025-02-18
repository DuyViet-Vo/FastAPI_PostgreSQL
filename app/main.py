from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_router

app = FastAPI(
    title="Buidling RESTful APIs with FastAPI",
    description="Demo project for building RESTful APIs with FastAPI. Designed by Vo Duy Viet",
    version="1.0.0",
    openapi_tags=[],
)

# Cấu hình CORS nếu cần
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")
