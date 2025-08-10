from fastapi import FastAPI

from src.api.v1 import activity, building, organization
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(
    title="Directory API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    description="""
    API для справочника организаций, зданий и видов деятельности.

    ## Возможности

    * Поиск организаций по названию
    * Поиск организаций по виду деятельности
    * Поиск организаций в заданном радиусе или прямоугольной области
    * Получение информации об организации по ID
    * Получение списка организаций в здании
    """,
)
app.include_router(organization.router)
app.include_router(building.router)
app.include_router(activity.router)
