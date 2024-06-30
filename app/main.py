from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, schemas, auth, database
import requests  # Импортируем requests для выполнения HTTP запросов
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

# Нужно для сохранения токеты
TOKEN = None
USER = None

# Создание таблиц в базе данных

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")
app.mount("/images", StaticFiles(directory="./images"), name="images")

templates = Jinja2Templates(directory="./pages")

# Дальше роуты

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    global USER

    if USER is not None:
        template = "index.html"
        context = {"request": request, 'user': USER}

        return templates.TemplateResponse(template, context)

    return RedirectResponse("/auth")  # Перенаправление на страницу входа

# Страница сообщений
@app.get("/messanger", response_class=HTMLResponse)
async def read_item(request: Request):
    global USER

    if USER is not None:
        template = "messanger.html"
        context = {"request": request, 'user': USER}

        return templates.TemplateResponse(template, context)

    return RedirectResponse("/auth")  # Перенаправление на страницу входа

# Страница о проекте
@app.get("/about", response_class=HTMLResponse)
async def read_item(request: Request):
    template = "about.html"
    context = {"request": request}

    return templates.TemplateResponse(template, context)

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    global USER

    if USER is not None:
        template = "profile.html"
        context = {"request": request, 'user': USER}

        return templates.TemplateResponse(template, context)

    return RedirectResponse("/auth")  # Перенаправление на страницу входа

# Страница настройки
@app.get("/settings", response_class=HTMLResponse)
async def read_item(request: Request):
    global USER

    if USER is not None:
        template = "settings.html"
        context = {"request": request, 'user': USER}

        return templates.TemplateResponse(template, context)

    return RedirectResponse("/auth")  # Перенаправление на страницу входа

# Страница авторизации
@app.get("/auth", response_class=HTMLResponse)
async def read_item(request: Request):
    global USER

    if USER is None:
        template = "auth.html"
        context = {"request": request}

        return templates.TemplateResponse(template, context)

    return RedirectResponse("/profile")

# Страница регистрации
@app.get("/registration", response_class=HTMLResponse)
async def read_item(request: Request):
    global USER

    if USER is None:
        template = "registration.html"
        context = {"request": request}

        return templates.TemplateResponse(template, context)
    
    return RedirectResponse("/profile")

# Регистрация пользователя
@app.post("/register") # response_model=schemas.User
def read_item(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    global USER
    
    if USER is None:
        db_user = db.query(models.User).filter(models.User.username == username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = auth.get_password_hash(password)
        db_user = models.User(username=username, email=email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Получаем модель нашего пользователя
        user = db.query(models.User).filter(models.User.username == username).first()

        if user:
            USER = user

            return RedirectResponse("/profile", status_code=302)
    
    else:
        return RedirectResponse("/")
        # return db_user

# Новый маршрут для аутентификации и сохранения токена
@app.post("/login")
def read_item(username: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    global TOKEN
    global USER

    if USER is None:
        user = db.query(models.User).filter(models.User.username == username).first()

        if auth.verify_password(password, user.hashed_password):
            if user:
                USER = user

                return RedirectResponse("/profile", status_code=302)
    
    else:
        return RedirectResponse("/")

# Функа выхода
@app.get("/logout")
def logout(request: Request):
    global USER

    if USER is not None:
        USER = None
    
    return RedirectResponse("/")