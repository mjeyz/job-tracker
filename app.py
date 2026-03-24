from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap5
from flask_login import login_required, login_user, logout_user, current_user, LoginManager, UserMixin
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from form import *

app = Flask(__name__)
Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "13114asap"
DATABASE_URL =  "postgresql://postgres:9992@localhost:5432/job tracker"


class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        print(email, password)

    return render_template("auth/login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        dob = form.dob.data
        gender = form.gender.data
        password = form.password.data
        terms = form.terms.data
        privacy = form.privacy.data

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        with psycopg2.connect(DATABASE_URL) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (first_name, last_name, username, dob, gender, email, password)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)", (first_name, last_name, username, dob, gender, email, hashed_password))
            conn.commit()

        print(first_name, last_name, username, email, dob, gender, terms, privacy, hashed_password)


    return render_template("auth/register.html", form=form)



if __name__ == '__main__':
    app.run(debug=True, port=5003)