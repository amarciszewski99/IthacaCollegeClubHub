from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, \
    SelectMultipleField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.fields import DateField, TimeField, DateTimeField
from app.models import Member


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    year = IntegerField('Graduation Year', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Member.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email Already Used')

class AddEventForm(FlaskForm):
    name = StringField('Event Field', validators=[DataRequired()])
    club = SelectField('Hosting Club', validators=[DataRequired()])
    date_time = DateTimeField('Event Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    location = TextAreaField('Event Location', validators=[DataRequired()])
    submit = SubmitField('Schedule Event')

class AddClubForm(FlaskForm):
    name = StringField('Club Name', validators=[DataRequired()])
    description = StringField('Club Description', validators=[DataRequired()])
    submit = SubmitField('Add Club')

class JoinClubForm(FlaskForm):
    submit = SubmitField('Join Club')

class JoinEventForm(FlaskForm):
    submit = SubmitField('RSVP')