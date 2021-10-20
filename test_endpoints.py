import shutil
from fastapi.testclient import TestClient
from app.main import app
from app.settings import BASE_DIR, UPLOAD_DIR

from PIL import Image

client = TestClient(app)

def test_get_home():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']


def test_post_home():
    response = client.post("/")

    assert response.status_code == 200
    assert "application/json" in response.headers['content-type']
    assert response.json() == {"hello":"world"}


def test_image_echo():
    image_dir = BASE_DIR / "images"

    for path in image_dir.glob('*'):
        try:
            img = Image.open(path)
        except:
            img = None


        response = client.post("/image-echo/", files={"file":open(path, 'rb')})
        fext = str(path.suffix).replace('.','')
        if img is not None:
            assert response.status_code == 200
        else:
            assert response.status_code == 400

    shutil.rmtree(UPLOAD_DIR)
