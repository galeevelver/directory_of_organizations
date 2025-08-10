import asyncio
import random
from faker import Faker
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.session import SessionLocal
from src.domain.models import Building, Activity, Organization
from src.domain.models.phone import Phone

faker = Faker("ru_RU")


BASE_LAT = 11.36
BASE_LON = 151.66


async def create_buildings(session: AsyncSession) -> list[Building]:
    buildings = [
        Building(
            address=faker.address(),
            latitude=BASE_LAT + random.uniform(-0.01, 0.01),
            longitude=BASE_LON + random.uniform(-0.01, 0.01),
        )
        for _ in range(5)
    ]
    session.add_all(buildings)
    await session.flush()
    return buildings


async def create_activities(session: AsyncSession) -> list[Activity]:
    food = Activity(name="Еда")
    cars = Activity(name="Автомобили")
    session.add_all([food, cars])
    await session.flush()

    meat = Activity(name="Мясная продукция", parent_id=food.id)
    milk = Activity(name="Молочная продукция", parent_id=food.id)
    trucks = Activity(name="Грузовые", parent_id=cars.id)
    cars_light = Activity(name="Легковые", parent_id=cars.id)
    session.add_all([meat, milk, trucks, cars_light])
    await session.flush()

    accessories = Activity(name="Аксессуары", parent_id=cars_light.id)
    parts = Activity(name="Запчасти", parent_id=cars_light.id)
    session.add_all([accessories, parts])
    await session.flush()

    return [food, cars, meat, milk, trucks, cars_light, accessories, parts]


async def create_organizations(session: AsyncSession, buildings: list[Building], activities: list[Activity]):
    for i in range(10):
        name = "ОМК" if i == 0 else faker.company()
        building = random.choice(buildings)

        org = Organization(name=name, building_id=building.id)
        org.activities.extend(random.sample(activities, k=2))
        session.add(org)
        await session.flush()

        phones = [
            Phone(phone=faker.phone_number(), organization_id=org.id)
            for _ in range(2)
        ]
        session.add_all(phones)


async def clear_all(session: AsyncSession):
    await session.execute(text(
        "TRUNCATE organizations, buildings, activities, phones, organization_activity RESTART IDENTITY CASCADE"
    ))


async def main():
    async with SessionLocal() as session:
        async with session.begin():
            await clear_all(session)
            buildings = await create_buildings(session)
            activities = await create_activities(session)
            await create_organizations(session, buildings, activities)
        print("База успешно очищена и наполнена.")


if __name__ == "__main__":
    asyncio.run(main())