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
