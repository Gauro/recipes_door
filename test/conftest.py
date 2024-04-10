# from app.routes import app, db
import pytest

from app.models import db
from app.routes import app

db.init_app(app)


@pytest.fixture(scope='session')
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
