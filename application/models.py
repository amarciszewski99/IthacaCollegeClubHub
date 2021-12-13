from datetime import datetime
from application import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Member(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64))
	email = db.Column(db.String(128), unique = True)
	password = db.Column(db.String(64))
	major = db.Column(db.String(64))
	year = db.Column(db.Integer)
	m2e_list = db.relationship("MemberToEvent", backref="member", lazy="dynamic")
	m2c_list = db.relationship("MemberToClub", backref="member", lazy="dynamic")

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

@login.user_loader
def load_user(id):
    return Member.query.get(int(id))


class Club(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), index = True, unique = True)
	description = db.Column(db.String(1024))
	m2c_list = db.relationship("MemberToClub", backref="club", lazy="dynamic")


class Event(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(128), index = True)
	date = db.Column(db.String(64), index = True)
	address = db.Column(db.String(128), index = True)
	description = db.Column(db.String(1024))
	clubID = db.Column(db.Integer, db.ForeignKey('club.id'))
	m2e_list = db.relationship("MemberToEvent", backref="event", lazy="dynamic")


class MemberToClub(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	memberID = db.Column(db.Integer, db.ForeignKey('member.id'))
	clubID = db.Column(db.Integer, db.ForeignKey('club.id'))
	is_admin = db.Column(db.Boolean)


class MemberToEvent(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	memberID = db.Column(db.Integer, db.ForeignKey('member.id'))
	eventID = db.Column(db.Integer, db.ForeignKey('event.id'))
