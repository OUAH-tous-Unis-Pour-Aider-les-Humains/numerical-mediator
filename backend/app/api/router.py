from fastapi import APIRouter

from app.api.classification import router as classification_router
from app.api.experimentation import router as experimentation_router
from app.api.health import router as health_router
from app.api.maths import router as maths_router
from app.api.science import router as science_router
from app.api.system import router as system_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(system_router)
api_router.include_router(classification_router)
api_router.include_router(experimentation_router)
api_router.include_router(maths_router)
api_router.include_router(science_router)
