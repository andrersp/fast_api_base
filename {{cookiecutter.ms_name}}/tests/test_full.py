
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from {{cookiecutter.ms_name}}.app import create_app
from {{cookiecutter.ms_name}}.ext.database import get_session
from {{cookiecutter.ms_name}}.crud.default_data import create_default_rules, create_first_user


app = create_app()


database = 'database.db'
if os.path.exists(database):
    os.remove(database)


@pytest.fixture(name='session')
async def session_fixture():

    engine = create_async_engine(
        f"sqlite+aiosqlite:///{database}", connect_args={"check_same_thread": False}, future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        await create_default_rules(conn)
        await create_first_user(conn)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


@pytest.fixture(name='client')
async def app_client(session):

    def get_session_override():  #
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client  #
    app.dependency_overrides.clear()  #


data_login_success = {
    "username": "admin",
    "password": "admin",

}

data_login_error = {
    "username": "admin_user",
    "password": "admin",
}

data_login_disable = {
    "username": "user",
    "password": "fake_123",
}

data_create_user = {
    "name": "Fake Name user",
    "password": "fake_123",
    "email": "novo_email@mail.com",
    "rule_id": 1,
    "username": "user"
}

data_update_user_duplicate_email = {
    "name": "Fake Name user",
    "email": "email@mail.com",
    "rule_id": 1,
    "username": "user"
}

data_update_user = {
    "name": "Fake Name user",
    "email": "email_atualizado@mail.com",
    "rule_id": 1,
    "username": "user",
    "enable": False
}

header = {}


def test_login(client):  #
    response = client.post(
        "/v1/login",
        data=data_login_success)
    data = response.json()
    header['Authorization'] = f'Bearer {data.get("access_token")}'

    assert response.status_code == 200
    assert data['success'] == True
    response = client.post(
        "/v1/login",
        data=data_login_error)
    data = response.json()

    assert response.status_code == 422
    assert data['success'] == False


def test_create_user(client):

    r = client.post("/v1/user", json=data_create_user, headers=header)

    result = r.json()

    assert r.status_code == 201
    assert "id" in result
    assert result['success'] == True

    data_create_user['email'] = 'email@mail.com'

    # Duplicate Email and user
    r = client.post("/v1/user", json=data_create_user, headers=header)
    result = r.json()
    assert r.status_code == 422
    assert not "id" in result


def test_get_all_users(client):
    r = client.get("/v1/user", headers=header)

    result = r.json()
    assert r.status_code == 200
    assert "data" in result
    assert result.get("success") == True


@pytest.mark.asyncio
async def test_select_user(client):
    r = client.get("/v1/user/1", headers=header)

    result = r.json()
    assert r.status_code == 200
    assert "id" in result
    assert result.get("success") == True

    r = client.get("/v1/user/10", headers=header)

    assert r.status_code == 404


def test_update_user(client):
    r = client.put(
        "/v1/user/2", json=data_update_user_duplicate_email, headers=header)

    result = r.json()
    assert r.status_code == 422
    assert result['success'] == False

    r = client.put(
        "/v1/user/2", json=data_update_user, headers=header)
    result = r.json()
    assert "id" in result
    assert r.status_code == 200
    assert result['success'] == True
    assert result['email'] == "email_atualizado@mail.com"


def test_about_me(client):
    r = client.get("/v1/user/me", headers=header)

    result = r.json()

    assert "id" in result
    assert r.status_code == 200


def test_login_disable(client):  #
    r = response = client.post(
        "/v1/login",
        data=data_login_disable)
    data = response.json()
    assert r.status_code == 403
    assert data['success'] == False
