from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Модели базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    searches = db.relationship('SearchHistory', backref='user', lazy=True)

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Создание базы данных
with app.app_context():
    db.create_all()

# Маршруты
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            # flash('Пароли не совпадают!', 'error')
            return redirect(url_for('register'))

        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            # flash('Пользователь с таким email или username уже существует.', 'error')
            return redirect(url_for('register'))

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        # flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('user_login'))  # Изменено с 'login' на 'user_login'
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.id
            # flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('home'))
        else:
            # flash('Неверный email или пароль.', 'error')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/profile')
def user_profile():
    if 'user_id' not in session:
        # flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('user_login'))

    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/history')
def user_history():
    if 'user_id' not in session:
        # flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('user_login'))

    user = User.query.get(session['user_id'])
    searches = SearchHistory.query.filter_by(user_id=user.id).all()
    return render_template('history.html', user=user, searches=searches)

@app.route('/add_search', methods=['POST'])
def add_search():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    course_name = request.form['course_name']
    user_id = session['user_id']

    search = SearchHistory(course_name=course_name, user_id=user_id)
    db.session.add(search)
    db.session.commit()

    # flash('Поиск добавлен в историю.', 'success')
    return redirect(url_for('user_history'))

@app.route('/how-to-use')
def how_to_use():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('how_to_use.html', user=user)
    return render_template('how_to_use.html')

@app.route('/logout')
def perform_logout():
    session.pop('user_id', None)
    # flash('Вы вышли из системы.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='172.16.22.244', port=8000)