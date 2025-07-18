from fastapi import APIRouter

from dishka.integrations.fastapi import DishkaRoute, FromDishka as Depends

projects_router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"],
    route_class=DishkaRoute
)
