import os
from flask import Flask, request, session, redirect, \
	url_for, render_template, flash, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from user import User, udb
from upload import Upload, fdb

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
VALID_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

def init_db():
	"""Create the initial database tables."""
	udb.create_all()
	fdb.create_all()

def get_user(username):
	"""Query the database for an instance of a given username."""
	return User.query.filter_by(name=username).first()

def valid_file(filename):
	"""Determines if a file contains an allowed extension."""
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in VALID_EXTENSIONS

def valid_user(name):
	"""Redirects a user to the login page if they attempt to
	access a page belonging to another user."""
	if 'logged_in' in session and session['logged_in'] == name:
		error = None
	elif get_user(name) is None:
		error = "User %s does not exist." % name
	else:
		error = "Must be logged in as %s to access this page." % name

	return error

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/create/', methods=['GET', 'POST'])
def create():
	error = None
	if request.method == 'POST':
		# Get submitted values from fields.
		username = request.form['username']
		password = request.form['password-a']

		# Check if there is a user by the same username in the database.
		user_instance = get_user(username)
		if user_instance is not None:
			error = 'Username is already taken.'
		elif password != request.form['password-b']:
			error = 'Passwords do not match.'
		else:
			user_instance = User(username, password)
			flash('Account created!')
			session['logged_in'] = username
			return redirect(url_for('index'))

	return render_template('create.html', error=error)

@app.route('/login/', methods=['GET', 'POST'])
@app.route('/user/', alias=True)
def login():
	error = None
	if request.method == 'POST':
		username = request.form['username']
		user_instance = get_user(username)
		if user_instance is None:
			error = 'Invalid username.'
		elif not user_instance.check_pw(request.form['password']):
			error = 'Invalid password.'
		else:
			session['logged_in'] = username
			flash('Successfully logged in.')
			return redirect(url_for('index'))

	return render_template('login.html', error=error)

@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	flash('Successfully logged out.')

	return redirect(url_for('login'))

@app.route('/user/<name>/')
def view_files(name):
	error = valid_user(name)
	if error is None:
		return render_template('view_files.html', username=name)
	else:
		return render_template('login.html', error=error)

@app.route('/user/<name>/upload/', methods=['GET', 'POST'])
def upload(name):
	error = valid_user(name)
	if error is None:
		if request.method == 'POST':
			file = request.files['file']
			if file and valid_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				file_instance = Upload(name, filename)
				flash('File was uploaded successfully.')
				return redirect(url_for('view_files', name=name))

		return render_template('upload.html', error=error)
	else:
		return render_template('login.html', error=error)

@app.route('/user/<name>/<filename>/')
def uploaded_file(name, filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
	init_db()
	app.run()