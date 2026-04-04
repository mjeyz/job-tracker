from flask import Flask, render_template, redirect, url_for, flash
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
DATABASE_URL = "postgresql://postgres:9992@localhost:5432/job tracker"


class User(UserMixin):
    def __init__(self, id, first_name, last_name, username, dob, gender, email, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.dob = dob
        self.gender = gender
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))

        user = cur.fetchone()
        if user:
            return User(id=user[0], first_name=user[1], last_name=user[2], username=user[3], dob=user[4],
                        gender=user[5], email=user[6], password=user[7])
        return None


@app.route('/')
def home():
    return render_template("index.html", current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        print(email, password)

        with psycopg2.connect(DATABASE_URL) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users Where email = %s", (email,))

            user = cur.fetchone()

            if not user:
                flash("This email is not registered. Please register first.", "danger")
                return redirect(url_for("login"))

            print(user[7], check_password_hash(user[7], password))

            if not check_password_hash(user[7], password):
                flash("Incorrect password. Please try again.", "danger")
                return redirect(url_for("login"))

            user_obj = User(id=user[0], first_name=[1], last_name=[2], username=user[3], dob=[4], gender=user[5],
                            email=user[6], password=[7])
            login_user(user_obj)
            return redirect(url_for("dashboard"))

    return render_template("auth/login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


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
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (first_name, last_name, username, dob, gender, email, hashed_password))
            conn.commit()

            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            user_id = cur.fetchone()[0]

            if cur.fetchone():
                flash("This Email is already registered. Please register first.", "danger")
                return redirect(url_for("register"))

            user = User(id=user_id, first_name=first_name, last_name=last_name, username=username, dob=dob,
                        gender=gender, email=email, password=password)
            login_user(user)
            flash("Registration successful.", "success")
            return redirect(url_for("dashboard"))

    return render_template("auth/register.html", form=form, current_user=current_user)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    with psycopg2.connect(DATABASE_URL) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM job_application WHERE user_id = %s", (current_user.id,))
        application = cur.fetchall()

    return render_template("dashboard.html", current_user=current_user, applications=application)


@app.route("/add_application", methods=['GET', 'POST'])
def add_application():
    form = ApplicationForm()

    if form.validate_on_submit():
        company_name = form.company_name.data
        role = form.role.data
        job_type = form.job_type.data
        status = form.status.data
        applied_date = form.applied_date.data
        salary = form.salary.data
        location = form.location.data
        source = form.source.data
        contact_person = form.contact_person.data
        notes = form.notes.data

        with psycopg2.connect(DATABASE_URL) as conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO job_application (user_id, company_name, role, job_type,
                                                        status, applied_date, salary, location, source, contact_person, notes)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (current_user.id, company_name, role, job_type, status, applied_date,
                         salary, location, source, contact_person, notes))
            conn.commit()

    return render_template("add_application.html", form=form, current_user=current_user)


@app.route("/application/<int:application_id>", methods=['GET', 'POST'])
def view_application(application_id):
    pass


@app.route("/edit_application", methods=["GET", "POST"])
def edit_application(application_id):
    return render_template("edit_application")


@app.route("/delete_application", methods=["GET", "POST"])
def delete_application(application_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM job_application WHERE id = %s", (application_id,))
        conn.commit()

    flash("Application deleted successfully.", "success")
    return redirect(url_for("dashboard"))

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")
if __name__ == '__main__':
    app.run(debug=True, port=5003)
