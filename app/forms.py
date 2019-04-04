from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, Email
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    region = SelectField(u'Region', choices=[("sf","San Francisco"),("sel","Seoul"),
    ("hyd","Hyderabad"),("ber","Berlin"),("ba","Buenos Aires"),("ldn","London"),
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
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


# book forms
class AddBookForm(FlaskForm):
    bookname = StringField('Book Name', validators=[DataRequired()])
    author = StringField("Author of the Book", validators=[DataRequired()])
    numpages = IntegerField("Number of Pages", validators=[DataRequired()])
    condition = SelectField(u'Condition of the book', choices=[("new", "New"),("used","Used"),
    ("torn","Torn")], validators=[DataRequired()])
    submit = SubmitField('Add')
