from flask import Flask
from flask import jsonify
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


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)



