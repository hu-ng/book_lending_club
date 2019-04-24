from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, Email
from .models import User
from datetime import date


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    region = SelectField(u'Region',
                         choices=[("sf", "San Francisco"), ("sel", "Seoul"),
                                  ("hyd", "Hyderabad"), ("ber", "Berlin"),
                                  ("ba", "Buenos Aires"), ("ldn", "London"),
                                  ("tpe", "Taipei")], validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), Email()], render_kw={"placeholder": "email"})
    password = PasswordField('', validators=[DataRequired()], render_kw={"placeholder": "password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


# book forms
class AddBookForm(FlaskForm):
    bookname = StringField('Book Name', validators=[DataRequired()])
    author = StringField("Author of the Book", validators=[DataRequired()])
    numpages = IntegerField("Number of Pages", validators=[DataRequired()])
    condition = SelectField(u'Condition of the book',
                            choices=[("new", "New"),
                                     ("used", "Used"),
                                     ("torn", "Torn")], validators=[DataRequired()])
    img = StringField('Image URL', validators=[Length(min=0, max=240, message="url is too long")])
    submit = SubmitField('Add')


# borrowing request form
class RequestForm(FlaskForm):
    start_date = DateField("Checkout date", format='%Y-%m-%d',
                           validators=[DataRequired()])
    end_date = DateField("Return date", format='%Y-%m-%d',
                         validators=[DataRequired()])
    submit = SubmitField("Request")
