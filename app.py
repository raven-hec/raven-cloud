from flask import Flask, request
from flask import jsonify
from flask import make_response, url_for
from flask import abort
from flask import render_template
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
	api_list = []
	db = connection.raven_cloud.users
	for row in db.find():
		api_list.append(str(row))
	return jsonify({'user_list': api_list})

def list_user(user_id):
	api_list=[]
	db = connection.raven_cloud.users
	for row in db.find({'id':user_id}):
		api_list.append(str(row))
	if api_list == []:
		abort(404)
	return jsonify({'user_list': api_list})

def add_user(new_user):
	api_list = []
	print(new_user)
	db = connection.raven_cloud.users
	user = db.find({'$or':[{"username":new_user['username']},{"email":new_user['email']}]})
	for row in user:
		print(str(row))
		api_list.append(str(row))
	
	if api_list == []:
		db.insert(new_user)
		return "Success"
	else:
		abort(409)
	return jsonify(api_list)

def del_user(del_user):
	db = connection.raven_cloud.users
	api_list = []
	for row in db.find({'username': del_user}):
		api_list.append(str(row))
	if api_list == []:
		abort(404)
	else:
		db.remove({"username":del_user})
		return "Success"

def upd_user(user):
	api_list = []
	print(user)
	db_user = connection.raven_cloud.users
	users = db_user.find_one({"id":user['id']})
	for row in users:
		api_list.append(str(row))
	if api_list == []:
		abort(409)
	else:
		db_user.update({'id':user['id']},{'$set':user}, upsert=False)
		return "Success"

def list_tweets():
	api_list = []
	db = connection.raven_cloud.tweets
	for row in db.find():
		api_list.append(str(row))
	return jsonify({'tweets_list': api_list})

def list_tweet(user_id):
	db = connection.raven_cloud.tweets
	api_list = []
	tweet = db.find({'id': user_id})
	for row in tweet:
		api_list.append(str(row))
	if api_list == []:
		abort(404)
	return jsonify({'tweet': api_list})

def add_tweet(new_tweet):
	api_list = []
	db_user = connection.raven_cloud.users
	db_tweet = connection.raven_cloud.tweets
	users = db_user.find({'username': new_tweet['tweetedby']})
	'''也可以这样写？
	if len(users) != 0:
		db_tweet.insert(new_tweet)
	'''
	for row in users:
		api_list.append(str(row))
		if api_list == []:
			abort(404)
		else:
			db_tweet.insert(new_tweet)		
	return "Success"

@app.route("/api/v1/info")
def home_index():
	api_list=[]
	db = connection.raven_cloud.apirelease
	for row in db.find():
		api_list.append(str(row))

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

### app api route
@app.route('/adduser')
def adduser():
	return render_template('adduser.html')

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
	if not request.json or not 'tweetedby' in request.json or not 'body' in request.json:
		abort(400)

	user_tweet['tweetedby'] = request.json['tweetedby']
	user_tweet['body'] = request.json['body']
	user_tweet['created_at'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
	print(user_tweet)
	return jsonify({'status': add_tweet(user_tweet)}), 201

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
	return list_tweet(id)

@app.route('/index')
def index():
	return render_template('index.html')

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



