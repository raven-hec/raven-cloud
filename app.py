from flask import Flask, request
from flask import jsonify
from flask import make_response, url_for
from flask import abort
from time import gmtime,strftime 
import json
import sqlite3

app = Flask(__name__)

@app.route("/api/v1/info")
def home_index():
	conn = sqlite3.connect('mydb.db')
	print ("Opened database successfully")
	api_list=[]
	cursor = conn.execute("SELECT buildtime,version,methods,links from apirelease")

	for row in cursor:
		api = {}
		api['version'] = row[0]
		api['buildtime'] = row[1]
		api['methods'] = row[2]
		api['links'] = row[3]
		api_list.append(api)

		conn.close()
		return jsonify({'api_version': api_list}), 200
	
@app.route("/api/v1/users", methods=['GET'])	
def get_users():
	return list_users()

def list_users():
	conn = sqlite3.connect('mydb.db')
	print ("Opened database sucessfully")

	api_list = []
	cursor = conn.execute("SELECT username, full_name, emailid, password, id from users")

	for row in cursor:
		a_dict = {}
		a_dict['username'] = row[0]
		a_dict['name'] = row[1]
		a_dict['email'] = row[2]
		a_dict['password'] = row[3]
		a_dict['id'] = row[4]
		api_list.append(a_dict)

	conn.close()
	return jsonify({'user_list': api_list})


@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
	return list_user(user_id)

def list_user(user_id):
	conn = sqlite3.connect("mydb.db")
	print ("Opened database successfully");
	api_list=[]

	cursor = conn.cursor()
	cursor.execute("SELECT * FROM users where id=?", (user_id,))
	data = cursor.fetchall()

	if len(data) != 0:
		user = {}
		user['username'] = data[0][0]
		user['name'] = data[0][1]
		user['email'] = data[0][2]
		user['password'] = data[0][3]
		user['id'] = data[0][4]

		api_list.append(user)

	conn.close()
	return jsonify({'user_list': api_list})
	#api_list.append(user)

##-----新建用户----##
@app.route('/api/v1/users', methods=['POST'])
def creatre_user():
	if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
		abort(4000)

	user = {
		'username': request.json['username'],
		'email': request.json['email'],
		'name': request.json.get('name'""),
		'password': request.json['password']
	}

	return jsonify({'status': add_user(user)}), 201

def add_user(new_user):
	conn = sqlite3.connect('mydb.db')
	print("Opened database successfully");
	api_list = []
	cursor = conn.cursor()
	cursor.execute("SELECT username, full_name, emailid, password, id FROM users WHERE username=? or emailid=?", (new_user['username'], new_user['email']))
	data = cursor.fetchall()

	if len(data) != 0:
		a_dict = {}
		a_dict['username'] = row[0]
		a_dict['name'] = row[1]
		a_dict['email'] = row[2]
		a_dict['password'] = row[3]
		a_dict['id'] = row[4]
		api_list.append(a_dict)

		abort(409)
	else:
		cursor.execute("INSERT INTO users(username,emailid,password,full_name) VALUES(?,?,?,?)", (new_user['username'],
		 new_user['email'], new_user['password'], new_user['name']))
		conn.commit()
		return "Sucess"

	conn.close()
	return jsonify(api_list)

@app.errorhandler(404)
def resource_not_found(error):
	return make_reponse(jsonify({'error':
		'Resource not found'}), 404)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)



