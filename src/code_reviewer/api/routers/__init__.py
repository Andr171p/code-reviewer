__all__ = ("router",)

from fastapi import APIRouter

from .projects import projects_router

router = APIRouter()

router.include_router(projects_router)
