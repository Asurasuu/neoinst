from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")
app.mount("/images", StaticFiles(directory="./images"), name="images")

templates = Jinja2Templates(directory="./pages")


# Дальше роуты

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    template = "index.html"
    context = {"request": request}

    return templates.TemplateResponse(template, context)

# Страница сообщений
@app.get("/messanger", response_class=HTMLResponse)
async def read_item(request: Request):
    template = "messanger.html"
    context = {"request": request}

    return templates.TemplateResponse(template, context)

# Страница о проекте
@app.get("/about", response_class=HTMLResponse)
async def read_item(request: Request):
    template = "about.html"
    context = {"request": request}

    return templates.TemplateResponse(template, context)

# Страница профиль
@app.get("/profile", response_class=HTMLResponse)
async def read_item(request: Request):
    template = "profile.html"
    context = {"request": request}

    return templates.TemplateResponse(template, context)

# Страница настройки
@app.get("/settings", response_class=HTMLResponse)
async def read_item(request: Request):
    template = "settings.html"
    context = {"request": request}

    return templates.TemplateResponse(template, context)