from wtforms import Form, StringField, PasswordField, BooleanField ,IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class AdvancedSearch(Form):
    artist = StringField('Artist')
    city = StringField('City')
    country = StringField('Country')
    date = StringField('Date')
    genre = StringField('Genre')
    min_age = StringField('Minimum Age')
    max_age = StringField('Maximum Age')
    min_price = StringField('Minimum Price')
    max_price = StringField('Maximum Price')
    page = StringField('Page')


class AddDelConcert(Form):
    artist = StringField('Artist', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    age_limit = IntegerField('Age Limit', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])


class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=10)])
    age = StringField('Age', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=10)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=10)])


class UpdateProfileForm(Form):
    age = StringField('Age', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    picture = StringField('Picture', validators=[DataRequired(),Length(min=2, max=10000)])
