from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, PasswordField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, Optional, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(2, 50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(2, 50)])
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=3, max=25),
                                                   Regexp('^[A-Za-z0-9_.]+$',
                                                          message="Username can only contain letters,"
                                                                  " numbers, dots and underscores.")])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    dob = DateField('Date of Birth', validators=[Optional()])
    gender = SelectField('Gender', validators=[Optional()],
                         choices=[('', 'Prefer not to say'), ('male', 'Male'), ('female', 'Female'),
                                  ('other', 'Other')])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    terms = BooleanField('I agree to the Terms & Conditions', validators=[DataRequired()])
    privacy = BooleanField('I agree to the Privacy Policy', validators=[DataRequired()])
    submit = SubmitField('Create Account')

class ApplicationForm(FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired(), Length(2, 50)])
    role = StringField("Role", validators=[DataRequired(), Length(2, 100)])
    job_type = SelectField("Job Type", validators=[DataRequired()], choices=[("full_time", "Full Time"), ("part_time", "Part Time"), ("remote", "Remote")])
    status = SelectField("Status", validators=[DataRequired()], choices=[("submitted", "Submitted"), ("pending", "Pending"), ("interview", "Interview"), ("rejected", "Rejected")])
    applied_date = DateField("Date of Application", validators=[Optional()])
    salary = StringField("Salary", validators=[Optional()])
    location = StringField("Location", validators=[Optional()])
    source = StringField("Source", validators=[Optional()])
    contact_person = StringField("Contact Person", validators=[Optional()])
    notes = StringField("Notes", validators=[Optional()])
    submit = SubmitField('Create Application')