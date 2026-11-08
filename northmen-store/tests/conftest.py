import pytest
from fastapi.testclient import TestClient
from faker import Faker

from app import main


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setattr(main, "DB_PATH", db_file)
    main.init_db()
    monkeypatch.setattr(main, "melhor_envio_quote", lambda cep, products: [{"id": "test-service", "name": "Correios PAC (teste)", "price": 18.50, "delivery_days": 5}])
    with TestClient(main.app, headers={"Authorization": "Basic YWRtaW46bm9ydGhtZW4tYWRtaW4tY2hhbmdlLW1l"}) as test_client:
        yield test_client


@pytest.fixture()
def fake():
    return Faker("pt_BR")
