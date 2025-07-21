from fastapi import APIRouter, status, UploadFile, File

from dishka.integrations.fastapi import DishkaRoute, FromDishka as Depends

from ...core.schemas import Project

projects_router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"],
    route_class=DishkaRoute
)


@projects_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=Project,
    summary="Создаёт проект."
)
async def create_project(project: Project) -> ...: ...


@projects_router.post(
    path="/{project_id}/documentations",
    status_code=status.HTTP_201_CREATED,
    response_model=...,
    summary="Добавляет документацию с существующему проекту."
)
async def add_documentation(file: UploadFile = File(...)) -> ...: ...


@projects_router.post(
    path="/{project_id}/modules",
    status_code=status.HTTP_201_CREATED,
    response_model=...,
    summary="Добавляет модуль в проект"
)
async def add_module() -> ...: ...


@projects_router.post(
    path="/{project_id}/metadata",
    status_code=status.HTTP_201_CREATED,
    response_model=...,
    summary=""
)
async def add_metadata(file: UploadFile = File(...)) -> ...: ...
