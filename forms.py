from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Length
from wtforms import ValidationError
from flask import request, flash
from model.db import User


class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired("Please Enter Valid Email"
                                                                 ), Email()], render_kw={"placeholder": "Enter Email Address"})
    password = PasswordField("Password", validators=[DataRequired("Please Enter Password")], render_kw={
                             "placeholder": "Enter Password"})
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[
                             DataRequired("Please First Name")], render_kw={"placeholder": "Enter First Name"})
    last_name = StringField('Last Name', validators=[
                            DataRequired("Please Enter Last Name")], render_kw={"placeholder": "Enter Last Name"})
    email = EmailField('Email Address', validators=[DataRequired("Please Enter Valid Email"
                                                                 ), Email()], render_kw={"placeholder": "Enter Email Address"})
    password = PasswordField("Password", validators=[DataRequired("Please Enter Password"), Length(min=5, max=15)], render_kw={
                             "placeholder": "Please Enter Password"})
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired("Please Enter Password"), EqualTo("password"), Length(min=5, max=15)], render_kw={
                             "placeholder": "Please Confirm Password"})
    submit = SubmitField("Register")
