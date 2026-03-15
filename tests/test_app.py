import pytest
import os
import tempfile
from app import app
import database

@pytest.fixture
def client():
    # Tworzymy tymczasową bazę danych do testów
    db_fd, db_path = tempfile.mkstemp()
    app.config['DATABASE'] = db_path
    app.config['TESTING'] = True

    with app.test_client() as client:
        # Inicjalizacja bazy wewnątrz kontekstu aplikacji
        with app.app_context():
            database.init_db()
        yield client

    # Po teście zamykamy i usuwamy tymczasową bazę
    os.close(db_fd)
    os.unlink(db_path)

def test_index_status_code(client):
    """Sprawdza, czy strona główna zwraca 200 OK."""
    response = client.get('/')
    assert response.status_code == 200

def test_transfer_page_loads(client):
    """Sprawdza, czy strona przelewu ładuje się dla zalogowanego użytkownika."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Symulujemy zalogowanie
    
    response = client.get('/transfer')
    assert response.status_code == 200

def test_history_page_loads(client):
    """Sprawdza, czy historia ładuje się dla zalogowanego użytkownika."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        
    response = client.get('/history')
    assert response.status_code == 200