from toy import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    centername = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)


class Vaccines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vaccinename = db.Column(db.String, nullable=False)
    manufacturing_company = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    centerid = db.Column(db.Integer, nullable=False)
    vaccineid = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
