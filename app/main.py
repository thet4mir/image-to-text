from .settings import * # noqa
import pathlib
import io
import uuid
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Depends,
    File,
    UploadFile,
)
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from PIL import Image


app = FastAPI()
tempaltes = Jinja2Templates(directory=str(BASE_DIR/ "templates"))


@app.get("/", response_class=HTMLResponse)
def home_get_view(request: Request, settings:Settings = Depends(get_settings)):
    return tempaltes.TemplateResponse("home.html", {"request": request})


@app.post("/")
def home_post_view():
    return {"hello":"world"}


@app.post("/image-echo/", response_class=FileResponse)
async def image_echo_view(file:UploadFile = File(...)):

    # BytesIo allow us to open file in memory
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid Image!", status_code=400)

    # check the uploads dir exists
    UPLOAD_DIR.mkdir(exist_ok=True)

    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    img.save(dest)

    return dest
