from flask import Flask, request
from flask import jsonify
from flask import make_response, url_for
from flask import abort
from pymongo import MongoClient
from time import gmtime,strftime 
import json
import sqlite3

app = Flask(__name__)
connection = MongoClient("mongodb://localhost:27017")

def create_mongodatabase():
	try:
		dbnames = connection.database_names()
		if 'raven_cloud' not in dbnames:
			db = connection.raven_cloud.users
			db_tweets = connection.raven_cloud.tweets
			db_api = connection.raven_cloud.apirelease

			db.insert({
				"email": "eric.strom@google.com",
				"id": 33,
				"name": "Eric stromerg",
				"password": "eric@123",
				"username": "eric.strom"
			})
			db_tweets.insert({
				"body": "New blog post, Launch your app with the AWS Startup Kit! #AWS",
				"id": 18,
				"timestamp": "2017-01-01T06：39：40Z",
				"tweetedby": "eric.strom"
			})
			db_api.insert({
				"buildtime": "2017-01-01 10:00:00",
				"links": "/api/v1/users",
				"methods": "get, post, put, delete",
				"version": "v1"
			})
			db_api.insert({
				"buildtime": "2017-01-11 10:00:00",
				"links": "/api/v2/tweets",
				"methods": "get, post",
				"version": "v2"
			})
			print("Database Initialize completred!")
		else:
			print("Database already Initialized!")
	except:
		print("Database creation failed!")

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

def list_user(user_id):
	conn = sqlite3.connect("mydb.db")
	print ("Opened database successfully")
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

def add_user(new_user):
	conn = sqlite3.connect('mydb.db')
	print("Opened database successfully");
	api_list = []
	cursor = conn.cursor()
	cursor.execute("SELECT username, full_name, emailid, password, id FROM users WHERE username=? or emailid=?", 
		(new_user['username'], new_user['email']))
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

def del_user(del_user):
	conn = sqlite3.connect('mydb.db')
	print("Opened database sucessfully")
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM users WHERE username=?", (del_user,))
	data = cursor.fetchall()
	print("Data", data)
	if len(data) == 0:
		abort(404)
	else:
		cursor.execute("DELETE FROM users WHERE username=?", (del_user,))
		conn.commit()
		return "Sucess"

def upd_user(user):
	conn = sqlite3.connect('mydb.db')
	print("Opened database sucessfully")
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM users WHERE id=? ", (user['id'],))
	data = cursor.fetchall()
	print(data)

	if len(data) == 0:
		abort(404)
	else:
		key_list = user.keys()
		for i in key_list:
			if i != "id":
				print(user, i)
				cursor.execute("UPDATE users SET {0} = ? WHERE id = ?".format(i), (user[i], user['id'],))
				#cursor.execute("""UPDATE users SET {0} = ? WHERE id = ?""".format(i),（user[i], user['id']))
				conn.commit()
		return "Sucess"

def list_tweets():
	conn = sqlite3.connect('mydb.db')
	print("Opened database sucessfully")
	api_list = []
	cursor = conn.cursor()
	cursor.execute("SELECT username,body,tweet_time,id FROM tweets")
	for row in cursor:
		tweets = {}
		tweets['TweetBy'] = row[0]
		tweets['Body'] = row[1]
		tweets['Timestamp'] = row[2]
		tweets['id'] = row[3]
		api_list.append(tweets)

	conn.close()
	return jsonify({'tweets_list': api_list})

def add_tweet(new_tweet):
	conn = sqlite3.connect('mydb.db')
	print("Opened database successfully")
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM users WHERE username=?", (new_tweet['username'],))
	data = cursor.fetchall()

	if len(data) != 0:
		abort(404)
	else:
		cursor.execute("INSERT INTO tweets(username, body, tweet_time) VALUES(?,?,?)", 
			(new_tweet['username'], new_tweet['body'],new_tweet['created_at']))
		conn.commit()
		return "Success"

def list_tweet(user_id):
	print(user_id)
	conn = sqlite3.connect('mydb.db')
	print("Opened database successfully")
	user = {}
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM tweets WHERE id=?", (user_id,))
	data = cursor.fetchall()
	print(data)
	if len(data) == 0:
		abort(404)
	else:
		user['id'] = data[0][0]
		user['username'] = data[0][1]
		user['body'] = data[0][2]
		user['tweet_time'] = data[0][3]

	conn.close()
	return jsonify(user)


@app.route("/api/v1/info")
def home_index():
	conn = sqlite3.connect('mydb.db')
	print ("Opened database successfully")
	api_list=[]
	cursor = conn.execute("SELECT version,buildtime,methods,links from apirelease")

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

@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
	return list_user(user_id)

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

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
	if not request.json or not 'username' in request.json: 
		abort(400)
	user = request.json['username']
	return jsonify({'status': del_user(user)}), 200

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
	user = {}
	if not request.json:
		abort(4000)
	
	user['id'] = user_id
	key_list = request.json.keys()
	for i in key_list:
		user[i] = request.json[i]
	print(user)
	return jsonify({'status': upd_user(user)}), 200

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
	return list_tweets()

@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
	user_tweet = {}
	if not request.json or not 'username' in request.json or not 'body' in request.json:
		abort(400)

	user_tweet['username'] = request.json['username']
	user_tweet['body'] = request.json['body']
	user_tweet['created_at'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
	print(user_tweet)
	return jsonify({'status': add_tweet(user_tweet)}), 201

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
	return list_tweet(id)

@app.errorhandler(400)
def invalid_request(error):
	return make_response(jsonify({'error': 
		'Bad Request'}), 400)

@app.errorhandler(404)
def resource_not_found(error):
	return make_response(jsonify({'error':
		'Resource not found'}), 404)


if __name__ == '__main__':
	create_mongodatabase()
	app.run(host='0.0.0.0', port=5000, debug=True)



