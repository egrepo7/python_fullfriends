from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "shh"
mysql = MySQLConnector(app, 'friendsdb')

@app.route('/')
def index():
	query = "SELECT * FROM friends" 
	friends = mysql.query_db(query)
	return render_template('index.html', all_friends=friends)

@app.route('/friends', methods = ['POST'])
def create():
	query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
	data = {
		'first_name':request.form['first_name'],
		'last_name':request.form['last_name'],
		'occupation': request.form['occupation']
	}
	mysql.query_db(query, data)
	return redirect('/')

@app.route('/friends/<id>/edit')
def edit(id):
	query = "SELECT * FROM friends WHERE id = :id"
	data = {'id' : id}
	friend = mysql.query_db(query, data)
	return render_template('edit.html', friend = friend[0])

@app.route('/friends/<id>', methods = ['POST'])
def update(id):
	query = "UPDATE friends SET first_name = :newfirst, last_name = :newlast, occupation = :newocc WHERE id = :id"
	data = {
		'newfirst': request.form['newfirst'],
		'newlast': request.form['newlast'],
		'newocc': request.form['newocc'],
		'id': id
		}
	mysql.query_db(query,data)
	return redirect('/')

@app.route('/friends/<id>/delete')
def delete(id):
	query = "DELETE FROM friends WHERE id = :id"
	data ={'id': id}
	mysql.query_db(query, data)
	return redirect('/')


app.run(debug=True)