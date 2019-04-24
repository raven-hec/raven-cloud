from flask import Flask, request
from flask import jsonify
from flask import make_response, url_for
from flask import abort
from flask import render_template
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from time import gmtime,strftime 
from requests import Requests
import json
import sqlite3

app = Flask(__name__)
CORS(app)

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


@app.route("/api/v1/info")
def home_index():
	api_list=[]
	db = connection.raven_cloud.apirelease
	for row in db.find():
		api_list.append(str(row))

	return jsonify({'api_version': api_list}), 200
	
@app.route("/api/v1/users", methods=['GET'])	
def get_users():
	return Requests.list_users()

@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
	return Requests.list_user(user_id)

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

	return jsonify({'status': Requests.add_user(user)}), 201

### app api route
@app.route('/adduser')
def adduser():
	return render_template('adduser.html')

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
	if not request.json or not 'username' in request.json: 
		abort(400)
	user = request.json['username']
	return jsonify({'status': Requests.del_user(user)}), 200

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
	return jsonify({'status': Requests.upd_user(user)}), 200

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
	return Requests.list_tweets()

@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
	user_tweet = {}
	if not request.json or not 'tweetedby' in request.json or not 'body' in request.json:
		abort(400)

	user_tweet['tweetedby'] = request.json['tweetedby']
	user_tweet['body'] = request.json['body']
	user_tweet['created_at'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
	if len(user_tweet) == 0:
		return 405
	return jsonify({'status': Requests.add_tweet(user_tweet)}), 201

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
	return Requests.list_tweet(id)

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



