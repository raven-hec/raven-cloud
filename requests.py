from pymongo import MongoClient
from flask import jsonify
from flask import abort

connection = MongoClient("mongodb://localhost:27017")


class Requests:
    @staticmethod
    def list_users():
        api_list = []
        db = connection.raven_cloud.users
        for row in db.find():
            api_list.append(str(row))
        return jsonify({'user_list': api_list})
    
    @staticmethod
    def list_user(user_id):
        api_list = []
        db = connection.raven_cloud.users
        for row in db.find({'id': user_id}):
            api_list.append(str(row))
        if api_list == []:
            abort(404)
        return jsonify({'user_list': api_list})

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def list_tweets():
        api_list = []
        db = connection.raven_cloud.tweets
        for row in db.find():
            api_list.append(str(row))
        return jsonify({'tweets_list': api_list})

    @staticmethod
    def list_tweet(user_id):
        db = connection.raven_cloud.tweets
        api_list = []
        tweet = db.find({'id': user_id})
        for row in tweet:
            api_list.append(str(row))
        if api_list == []:
            abort(404)
        return jsonify({'tweet': api_list})

    @staticmethod
    def add_tweet(new_tweet):
        api_list = []
        if len(new_tweet) == 0:
            abort(405)

        print(new_tweet['tweetedby'])
        db_user = connection.raven_cloud.users
        db_tweet = connection.raven_cloud.tweets
        users = db_user.find({'username': new_tweet['tweetedby']})
        '''也可以这样写？
        if len(users) != 0:
            db_tweet.insert(new_tweet)
        '''
        for row in users:
            api_list.append(str(row))
            print(api_list)
            if api_list == []:
                abort(408)
            else:
                db_tweet.insert(new_tweet)		
        return "Success"
