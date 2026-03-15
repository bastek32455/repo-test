import pytest
from app import app  # Importujemy Twoją aplikację Flask

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Sprawdza, czy strona główna się ładuje."""
    response = client.get('/')
    assert response.status_code == 200

