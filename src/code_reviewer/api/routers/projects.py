from fastapi import APIRouter, status

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
    response_model=...,
    summary=""
)
async def create_project(project: Project, repository: Depends[...]) -> ...:
    ...
