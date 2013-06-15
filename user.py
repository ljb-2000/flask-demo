import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
	'sqlite://///Users/jamesgray/Desktop/Source/Python/flask-demo/data/users.db'
# Create SQLAlchemy object for user database
udb = SQLAlchemy(app)

class User(udb.Model):
	"""Creates a user object and stores in an SQLAlchemy database."""

	# Initialize columns
	id = udb.Column(udb.Integer, primary_key=True)
	name = udb.Column(udb.String(80), unique=True)
	pw_hash = udb.Column(udb.String(160), unique=False)

	def __init__(self, username, password):
		self.name = username

		# Get an instance of the user object from the 
		# database if it exists.
		db_instance = User.query.filter_by(name=username).first()

		if db_instance is None:
			# Insert the user object into the database 
			# if no instance exists.
			self.set_pw(password)
			udb.session.add(self)
			udb.session.commit()
		else:
			# Retrieve relevant data from database
			self.id = db_instance.id
			self.pw_hash = db_instance.pw_hash
			print 'Error: User is already in the database'

	def __repr__(self):
		return '<User %r>' % self.name

	def set_pw(self, password):
		"""Generates a hash for the given password, to be
		stored in the database."""
		self.pw_hash = generate_password_hash(password)

	def check_pw(self, password):
		"""Checks a password against the stored hash."""
		return check_password_hash(self.pw_hash, password)

	def remove(self):
		"""Completely remove the user from the database.
		Note that you must query the database for the user object
		to be deleted before calling this function."""
		udb.session.delete(self)
		udb.session.commit()