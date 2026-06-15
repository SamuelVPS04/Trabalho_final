import os
import sys
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Force a local SQLite database for tests and avoid external DATABASE_URL
os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')

from app import app as flask_app, db
from models import User

@pytest.fixture(scope='function')
def client(tmp_path):
    db_file = tmp_path / 'test.db'
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_file}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret-key'
    })

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(nome='Administrador', email='admin@exemplo.com', tipo='admin')
        admin.set_senha('admin123')
        db.session.add(admin)
        db.session.commit()

    with flask_app.test_client() as client:
        yield client
