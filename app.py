from flask import Flask, request, session, g, redirect, \
	url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from user import User, db

app = Flask('flaskdemo')
app.config.from_pyfile('settings.cfg')

def init_db():
	"""Create the initial database tables."""
	db.create_all()

def get_user(username):
	"""Query the database for an instance of a given username."""
	return User.query.filter_by(name=username).first()

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

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Successfully logged out.')
	return redirect(url_for('login'))

@app.route('/user/<name>/')
def view_files(name):
	error = None
	if session['logged_in'] == name:
		return render_template('view_files.html', username=name)
	error = "Must be logged in to access this page."
	return render_template('login.html', error=error)


if __name__ == "__main__":
	init_db()
	app.run()