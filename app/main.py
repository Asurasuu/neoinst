from fastapi import FastAPI, Request, Depends, HTTPException, status, Form, Cookie, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import models, schemas, auth, database
import requests  # Импортируем requests для выполнения HTTP запросов
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Union
from sqlalchemy.orm.exc import UnmappedInstanceError
import aiofiles

# Создание таблиц в базе данных

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")
app.mount("/images", StaticFiles(directory="./images"), name="images")

templates = Jinja2Templates(directory="./pages")

# Дальше роуты

# Главная страница
@app.get("/", response_class=HTMLResponse)
def read_item(request: Request, db: Session = Depends(database.get_db), usr_id: Union[str, None] = Cookie(default=None)):

    if usr_id is not None: 
        user = db.query(models.User).filter(models.User.id == usr_id).first()
        photos = db.query(models.Photo).all()
        
        template = "index.html"
        context = {"request": request, 'user': user, 'photos': photos}

        return templates.TemplateResponse(template, context)

    return RedirectResponse("/auth")  # Перенаправление на страницу входа

# Страница сообщений
@app.get("/messanger/", response_class=HTMLResponse)
def read_item(request: Request, db: Session = Depends(database.get_db), usr_id: Union[str, None] = Cookie(default=None)):
    if usr_id is not None: 
        user = db.query(models.User).filter(models.User.id == usr_id).first()
        users = db.query(models.User).filter(models.User.id != usr_id).all()


        template = "messanger.html"
        context = {"request": request, 'users': users,'user': user, 'iid': None}
        return templates.TemplateResponse(template, context)

    return RedirectResponse("/auth")  # Перенаправление на страницу входа

@app.get("/messanger/{id}", response_class=HTMLResponse)
def read_item(request: Request, id: int, db: Session = Depends(database.get_db), usr_id: Union[str, None] = Cookie(default=None)):
    if usr_id is not None: 
        user = db.query(models.User).filter(models.User.id == usr_id).first()
        users = db.query(models.User).filter(models.User.id != usr_id).all()

        # Модель собеседника
        iid = db.query(models.User).filter(models.User.id == id).first()

        # Все сообщения
        messages = db.query(models.Message).filter(
            or_(
                and_(models.Message.sender_id == usr_id, models.Message.recipient_id == iid.id),
                and_(models.Message.sender_id == iid.id, models.Message.recipient_id == usr_id)
            )
        ).all()


        template = "messanger.html"
        context = {"request": request, 'users': users,'user': user, 'iid': iid, 'messages': messages}
        return templates.TemplateResponse(template, context)

    return RedirectResponse("/auth")  # Перенаправление на страницу входа

# Страница о проекте
@app.get("/about", response_class=RedirectResponse)
def read_item(request: Request):
    return RedirectResponse('https://neo-inst.vercel.app/abouts/index.html#')
    
@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request, db: Session = Depends(database.get_db), usr_id: Union[str, None] = Cookie(default=None)):
    if usr_id: 
        user = db.query(models.User).filter(models.User.id == usr_id).first()
        template = "profile.html"
        context = {"request": request, 'user': user}

        return templates.TemplateResponse(template, context)

    return RedirectResponse("/auth")  # Перенаправление на страницу входа

# Страница настройки
@app.get("/settings", response_class=HTMLResponse)
def read_item(request: Request, db: Session = Depends(database.get_db), usr_id: Union[str, None] = Cookie(default=None)):
    user = db.query(models.User).filter(models.User.id == usr_id).first()

    if usr_id is not None: 
        template = "settings.html"
        context = {"request": request, 'user': user}

        return templates.TemplateResponse(template, context)

    return RedirectResponse("/auth")  # Перенаправление на страницу входа

# Страница авторизации
@app.get("/auth", response_class=HTMLResponse)
def read_item(request: Request, usr_id: Union[str, None] = Cookie(default=None)):
    global USER

    if usr_id is None: 
        template = "auth.html"
        context = {"request": request}

        return templates.TemplateResponse(template, context)

    return RedirectResponse("/profile")

# Страница регистрации
@app.get("/registration", response_class=HTMLResponse)
def read_item(request: Request, usr_id: Union[str, None] = Cookie(default=None)):
    if usr_id is None: 
        template = "registration.html"
        context = {"request": request}

        return templates.TemplateResponse(template, context)
    
    return RedirectResponse("/profile")

# Регистрация пользователя
@app.post("/register") # response_model=schemas.User
def read_item(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db), usr_id: Union[str, None] = Cookie(default=None)):
    if usr_id is None: 
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
            usr_id = user.id

            resp = RedirectResponse("/profile", status_code=302)
            resp.set_cookie(key="usr_id", value=usr_id)
            return resp
    
    else:
        return RedirectResponse("/")
        # return db_user

# Новый маршрут для аутентификации и сохранения токена
@app.post("/login")
def read_item(username: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db), usr_id: Union[str, None] = Cookie(default=None)):
    if usr_id is None: 
        user = db.query(models.User).filter(models.User.username == username).first()

        if auth.verify_password(password, user.hashed_password):
            if user:
                usr_id = user.id

                resp = RedirectResponse("/profile", status_code=302)
                resp.set_cookie(key="usr_id", value=usr_id)

                return resp
    
    else:
        return RedirectResponse("/")

# Функа выхода
@app.get("/logout")
def logout(request: Request, usr_id: Union[str, None] = Cookie(default=None)):
    if usr_id is not None:
    
        resp = RedirectResponse("/")
        resp.delete_cookie(key="usr_id")
        return resp

    return RedirectResponse("/auth")

# Отправляем сообщение
@app.post("/sendmessage")
def send_message(from_user_id: str = Form(...), text_message: str = Form(...), db: Session = Depends(database.get_db), usr_id: Union[str, None] = Cookie(default=None)):
    if usr_id is not None:
        new_message = models.Message(sender_id=usr_id, recipient_id=from_user_id, content=text_message)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        return RedirectResponse("/messanger/" + from_user_id, status_code=302)

    return RedirectResponse("/auth")  # Перенаправление на страницу входа

# TODO выдает ошибку после сохранения данных
@app.post("/savesettings")
def save_settings(request: Request, surname: str = Form(...), name: str = Form(...), email: str = Form(...), 
                    phone: str = Form(...), about: str = Form(...),
                    db: Session = Depends(database.get_db), 
                    usr_id: Union[str, None] = Cookie(default=None)):
    
    if usr_id is not None:
        user = db.query(models.User).filter(models.User.id == usr_id).update({
            "name": name, "surname": surname,
            "phone": phone, "email": email,
            "about": about
        })

        db.commit()
        try:
            db.refresh(user)
        except UnmappedInstanceError as e:
            pass

        resp = RedirectResponse("/settings", status_code = 302)
        return resp 
    
    return RedirectResponse("/auth")  # Перенаправление на страницу входа

# Загрузка файлов

@app.post("/uploadfiles")
async def upload_photos(request: Request, text: str = Form(...), file: UploadFile = File(...),
                        db: Session = Depends(database.get_db), 
                        usr_id: Union[str, None] = Cookie(default=None)):
    
    async with aiofiles.open(f"./images/posts/{file.filename}", 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

        
    new_photo = models.Photo(filename=file.filename, content=content, text = text, user_id=usr_id)
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    return true