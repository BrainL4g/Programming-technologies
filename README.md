# Programming-technologies

Переименовать .env.example в .env 

Запуск через докер:  
из папки backend команда  
- docker compose up --build

Без докера  
Изменить в backend/.env :
- DATABASE_PASSWORD на свой пароль
- DATABASE_USER на свой логин
- REDIS_HOST на localhost
- DATABASE_HOST на localhost
- Запустить backend/src/main.py

По умолчанию создается аккаунт админа admin@example.com с паролем 12345

url api swagger 127.0.0.1:8000/docs#/

url frontend 127.0.0.1:3000/
