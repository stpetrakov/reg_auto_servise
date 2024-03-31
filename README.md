# Пример приложения с регистрацией и авторизацией через JWT

Это веб-приложение на Flask, которое предоставляет эндпоинты для регистрации пользователей, авторизации и доступа к защищенному ресурсу с использованием JSON Web Tokens (JWT).

## Установка зависимостей
Чтобы запустить это приложение, вам понадобится установить несколько библиотек Python. Выполните следующую команду для установки зависимостей:

`pip install flask flask_jwt_extended`


## Использование

1. **Регистрация пользователя**: 
   - Метод: POST
   - Путь: `/register`
   - Формат данных: JSON
   - Требуемые поля: `email`, `password`
   - Ответ: `user_id` нового пользователя и статус проверки пароля

2. **Авторизация пользователя**:
   - Метод: POST
   - Путь: `/authorize`
   - Формат данных: JSON
   - Требуемые поля: `email`, `password`
   - Ответ: JWT токен доступа
   
3. **Доступ к Feed**:
   - Метод: GET
   - Путь: `/feed`
   - Заголовок: `Authorization: Bearer <access_token>`
   - Ответ: 200 в случае успешной аутентификации

## Пример использования:

```bash
# Запуск приложения
python app.py

#Регистрация нового пользователя
curl -X POST \
  http://127.0.0.1:5000/register \
  -H 'Content-Type: application/json' \
  -d '{
	"email": "user@vk.com",
	"password": "Password123!"
}'

#Авторизация пользователя
curl -X POST \
  http://127.0.0.1:5000/authorize \
  -H 'Content-Type: application/json' \
  -d '{
	"email": "user@vk.com",
	"password": "Password123!"
}'

#Получение доступа к feed
curl -X GET \
  http://127.0.0.1:5000/feed \
  -H 'Authorization: Bearer <access_token>'
```


