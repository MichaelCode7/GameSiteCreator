from flask import Flask, render_template, redirect, request, abort
import sqlalchemy
from forms.user import RegisterForm
from forms.user import LoginForm
from data import db_session
from data.users import User
import datetime
from data.news import News
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from general_funcs import GeneralFuncs as gf
from general_vars import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

def main():
    db_session.global_init("db/gshopdata.db")
    app.run()

@app.route("/about")
def about():
    params = gf.get_form_json(json_info_f, key="about_info")
    return render_template('about.html', **params)

@app.route("/")
def index():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        return render_template("index.html", title="Главная")
    else:
        return redirect('/about')

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.last_login_date = datetime.datetime.now()
            db_sess.commit()
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/news',  methods=['GET', 'POST'])
@login_required
def news():
    return render_template('news.html', title='Новости')

if __name__ == '__main__':
    main()

