from flask import Flask, request, jsonify, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret' 
app.config['JWT_TOKEN_LOCATION'] = ['headers']  
app.config['JWT_ALGORITHM'] = 'HS256' 
jwt = JWTManager(app)

users_db = {}

email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

# Проверка надежности пароля
password_length_regex = r'.{8,}'
password_digit_regex = r'.*\d'
password_uppercase_regex = r'.*[A-Z]'
password_lowercase_regex = r'.*[a-z]'
password_special_char_regex = r'.*[!@#$%^&*()_+={}\[\]:;<>,.?/~`|\\-]'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Проверяем валидность email
    if not re.match(email_regex, email):
        return jsonify({'error': 'Invalid email'}), 400

    # Проверяем, существует ли пользователь с таким email
    if email in users_db:
        return jsonify({'error': 'User with this email already exists'}), 400

    # Проверяем надежность пароля
    if (not re.match(password_length_regex, password) or
            not re.match(password_digit_regex, password) or
            not re.match(password_uppercase_regex, password) or
            not re.match(password_lowercase_regex, password) or
            not re.match(password_special_char_regex, password)):
        return jsonify({'error': 'Weak password. Password must contain at least 8 characters, '
                                  'including at least one uppercase letter, one lowercase letter, '
                                  'one digit, and one special character.'}), abort(400, description="weak_password")

    # Хэшируем пароль
    hashed_password = generate_password_hash(password)

    # Генерируем уникальный user_id
    user_id = len(users_db) + 1

    # Добавляем пользователя в базу данных
    users_db[email] = {'user_id': user_id, 'password': hashed_password}

    # Возвращаем user_id и статус проверки пароля
    return jsonify({'user_id': user_id, 'password_check_status': 'good'}), 200

@app.route('/authorize', methods=['POST'])
def authorize():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Проверяем, существует ли пользователь с таким email
    if email not in users_db:
        return jsonify({'error': 'User not found'}), 404

    # Получаем хэшированный пароль из базы данных
    hashed_password = users_db[email]['password']

    # Проверяем пароль
    if not check_password_hash(hashed_password, password):
        return jsonify({'error': 'Invalid password'}), 401

    # Генерируем JWT access token
    access_token = create_access_token(identity=users_db[email]['user_id'])
    print(access_token) #так как токен может не влезать в вывод терминала

    # Возвращаем access token
    return jsonify({'access_token': access_token}), 200

@app.route('/feed', methods=['GET'])
@jwt_required()
def feed():
    # Если токен валиден, возвращаем 200. Иначе программа сама вернёт ошибку 401
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)

