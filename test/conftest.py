import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from asgi_lifespan import LifespanManager
from src.app.main import app
from src.app.core.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db: Session = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    app.dependency_overrides[get_db] = override_get_db
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://localhost:8000") as test_client:
            yield test_client
