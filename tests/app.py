import pytest
from app import app  # Import Twojej aplikacji Flask z pliku app.py

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Sprawdza, czy strona główna aplikacji zwraca status 200 (OK)."""
    response = client.get('/')
    assert response.status_code == 200

def test_app_exists():
    """Sprawdza, czy instancja aplikacji została poprawnie utworzona."""
    assert app is not None