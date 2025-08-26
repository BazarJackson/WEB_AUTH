# WEB_AUTH — FastAPI с регистрацией и логином пользователей через Docker

Проект демонстрирует простой веб-приложение на FastAPI с регистрацией, авторизацией, хешированием паролей через bcrypt и логированием пользователей. Проект работает через Docker Compose с контейнерами:

- **web** — FastAPI (порт 8000)  
- **db** — PostgreSQL (порт 5433)  

---

## **Функционал**

- Регистрация пользователей с проверкой на уже существующего пользователя  
- Логин пользователей  
- Страница приветствия после успешного входа (`success.html`)  
- Логирование пользователей: дата, время, IP, имя пользователя  
- Пароли хранятся в хешированном виде через bcrypt  

---

## **Установка и запуск на Ubuntu**

### 1. Установка Docker и Docker Compose

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

docker --version
docker compose version

# Чтобы не писать sudo каждый раз
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Установка Git

```bash
sudo apt install git -y
git --version

git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"
```

### 3. Клонирование проекта

```bash
git clone git@github.com:BazarJackson/WEB_AUTH.git
cd WEB_AUTH
```

### 4. Создание таблиц в базе данных

```bash
docker-compose exec web python create_tables.py
```

### 5. Сборка и запуск контейнеров

```bash
docker-compose up -d --build
```

FastAPI доступен на порту 8000
PostgreSQL на порту 5433

### 6. Проверка логов пользователей

```bash
docker-compose exec web tail -f /app/user_activity.log
```

### 7. Открытие веб-страниц

Главная: http://localhost:8000

Регистрация: http://localhost:8000/register

Логин: http://localhost:8000/login

После успешного входа открывается success.html
