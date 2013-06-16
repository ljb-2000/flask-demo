# flask-demo - upload.py
# Author: James Gray
# June 2013
#
# This file contains the Upload class, which
# flask-demo uses to add and fetch file uploads
# and owner information to and from a file database.

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
	'sqlite://///home/jamesgray/flask-demo/data/uploads.db'

# Create SQLAlchemy object for file database
fdb = SQLAlchemy(app)

class Upload(fdb.Model):
	"""
	Creates an upload object and stores in an SQLAlchemy database.
	"""

	# Initialize columns
	id = fdb.Column(fdb.Integer, primary_key=True)
	userid = fdb.Column(fdb.String(80))
	filename = fdb.Column(fdb.String(160))

	def __init__(self, username, filename):
		self.userid = username
		self.filename = filename

		# Insert the object into the database.
		fdb.session.add(self)
		fdb.session.commit()

	def __repr__(self):
		return '<File %r>' % self.filename