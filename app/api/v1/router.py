from fastapi import APIRouter
from .books import router as books_router
from .health import router as health_router


"""
Main API router module.

This module aggregates and includes all sub-routers
(e.g., Books, Health) into a single API router for the application.
"""

router = APIRouter()
router.include_router(books_router)
router.include_router(health_router)
