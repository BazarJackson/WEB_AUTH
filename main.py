from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import bcrypt
import logging


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Зависимость для сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Главная страница
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Страница регистрации (GET)
@app.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Обработка регистрации (POST)
@app.post("/register")
def register_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == username).first()
    client_ip = request.client.host

    if existing_user:
        logging.info(f"Попытка регистрации существующего пользователя: {username}, IP: {client_ip}")
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Пользователь уже зарегистрирован", "login_url": "/login"}
        )
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hashed_password.decode('utf-8'))
    db.add(user)
    db.commit()
    
    logging.info(f"Новая регистрация: {username}, IP: {client_ip}")
    
    return RedirectResponse(url="/login", status_code=303)

# Страница логина (GET)
@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Обработка логина (POST)
@app.post("/login")
def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    client_ip = request.client.host
    user = db.query(User).filter(User.username == username).first()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        logging.info(f"Успешный вход: {username}, IP: {client_ip}")
        return templates.TemplateResponse("success.html", {"request": request, "username": username})
    
    logging.info(f"Неудачная попытка входа: {username}, IP: {client_ip}")
    return templates.TemplateResponse("login.html", {"request": request, "error": "Неверный логин или пароль"})

# Настройка логирования в файл
logging.basicConfig(
    filename="user_activity.log",   # имя файла логов
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)