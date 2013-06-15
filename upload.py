import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
	'sqlite://///Users/jamesgray/Desktop/Source/Python/flask-demo/data/uploads.db'
# Create SQLAlchemy object for file database
fdb = SQLAlchemy(app)

class Upload(fdb.Model):
	"""Creates an upload object and stores in an SQLAlchemy database."""

	# Initialize columns
	id = fdb.Column(fdb.Integer, primary_key=True)
	userid = fdb.Column(fdb.String(80), unique=True)
	filename = fdb.Column(fdb.String(160), unique=False)

	def __init__(self, username, filename):
		self.userid = username
		self.filename = filename
		fdb.session.add(self)
		fdb.session.commit()

	def __repr__(self):
		return '<File %r>' % self.filename