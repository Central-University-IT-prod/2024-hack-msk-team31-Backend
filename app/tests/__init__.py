from starlette.testclient import TestClient

from app.misc import app

client = TestClient(app)
