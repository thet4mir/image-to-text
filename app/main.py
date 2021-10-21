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
import pytesseract
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
tempaltes = Jinja2Templates(directory=str(BASE_DIR/ "templates"))


@app.get("/", response_class=HTMLResponse)
def home_get_view(request: Request, settings:Settings = Depends(get_settings)):
    return tempaltes.TemplateResponse("home.html", {"request": request})


@app.post("/prediction/")
async def prediction_view(file:UploadFile = File(...)):

    # check the uploads dir exists
    UPLOAD_DIR.mkdir(exist_ok=True)
    # BytesIo allow us to open file in memory
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid Image!", status_code=400)

    preds = pytesseract.image_to_string(img)
    predictions = [x for x in preds.split("\n")]
    return {"result":predictions, "original":preds}


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
