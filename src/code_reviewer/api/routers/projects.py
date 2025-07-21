from fastapi import APIRouter, status, UploadFile, File

from dishka.integrations.fastapi import DishkaRoute, FromDishka as Depends

from ...core.schemas import Project

projects_router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"],
    route_class=DishkaRoute
)


@projects_router.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=...,
    summary=""
)
async def upload_file(file: UploadFile = File(...)) -> ...:
    content = await file.read()
