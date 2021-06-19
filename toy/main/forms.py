from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange


class CenterAddition(FlaskForm):
    centername = StringField('Center name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pincode = IntegerField('PIN code', validators=[
        DataRequired(), NumberRange(min=100000, max=999999)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Add Center')


class VaccineAddition(FlaskForm):
    vaccinename = StringField('Vaccine name', validators=[DataRequired()])
    manufacturing_company = StringField(
        'Manufacturing Company Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Vaccine')


class UpdateCenterDetails(FlaskForm):
    centername = StringField('Center name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pincode = IntegerField('PIN code', validators=[
                           DataRequired(),
                           NumberRange(min=100000, max=999999)])
    submit = SubmitField('Update Details')


class UpdateVaccineUnits(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Update Quantity')


class Request(FlaskForm):
    vaccinename = StringField('Vaccine Name', validators=[DataRequired()])
    quantity = IntegerField('No. of Units', validators=[DataRequired()])
    submit = SubmitField('Request')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
