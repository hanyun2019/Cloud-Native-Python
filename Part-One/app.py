# Haowen Huang modified on Sep 21, 2019
# Implementation of Cloud Native web applications
# Part One: Developing a RESTful micro service in Python 
# 
# Micro services demo
# http://localhost:5000/api/v1/info  
# http://localhost:5000/api/v1/users
#
# Tweets demo:
# GET Method: http://localhost:5000/api/v2/tweets  
# GET Method: http://localhost:5000/api/v2/users/[user_id]
# POST Method: http://localhost:5000/api/v2/tweets
# 

from flask import Flask, request, jsonify
from flask import abort
from flask import make_response, url_for
import json
from time import gmtime, strftime
import sqlite3

app = Flask(__name__)

def list_users():
    conn = sqlite3.connect('mydb.db')
    print ("Open database mydb.db successfully");
    api_list=[]
    cursor = conn.execute("select username, full_name, emailid, password, id from users")
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
    conn = sqlite3.connect('mydb.db')
    print ("Open database mydb.db successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where id=?", (user_id,))
    data = cursor.fetchall()
    if len(data) != 0:
        user = {}
        user['username'] = data[0][0]
        user['name'] = data[0][1]
        user['email'] = data[0][2]
        user['password'] = data[0][3]
        user['id'] = data[0][4]
    conn.close()
    return jsonify(a_dict)

def add_user(new_user):
    conn = sqlite3.connect('mydb.db')
    print ("Open database mydb.db successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("select * from users where username=? or emailid=?", (new_user['username'], new_user['email']))
    data = cursor.fetchall()
    if len(data) != 0:
        abort(409)
    else:
        cursor.execute("insert into users (username, emailid, password, full_name) values(?,?,?,?)", (new_user['username'], new_user['email'], new_user['password'], new_user['name']))
        conn.commit()
        return "Success"
    conn.close()
    return jsonify(a_dict)

#   Use RESTful API to DEBUG:
#   curl -i -H "Content-Type: application/json" -X POST -d '{"username":"michael123", "email": "MichaelJackson@horizonit.com", "password": "mk12345", "name": "Michael Jackson"}' http://localhost:5000/api/v1/users
#   curl -i -H "Content-Type: application/json" -X POST -d '{"username":"alanwalker", "email": "AlanWalker@horizonit.com", "password": "aw12345", "name": "Alan Walker"}' http://localhost:5000/api/v1/users
#

def del_user(del_user):
    conn = sqlite3.connect('mydb.db')
    print ("Open database mydb.db successfully");
    cursor=conn.cursor()
    cursor.execute("select * from users where username=? ", (del_user,))
    data = cursor.fetchall()
    print("Data", data)
    if len(data) == 0:
        abort(404)
    else:
        cursor.execute("delete from users where username==?", (del_user,))
    conn.commit()
    return "Success"

#   Use RESTful API to DEBUG:
#   curl -i -H "Content-Type: application/json" -X delete -d '{"username":"michael123"}' http://localhost:5000/api/v1/users
#

def upd_user(user):
    conn = sqlite3.connect('mydb.db')
    print ("Open database mydb.db successfully");
    cursor=conn.cursor()
    cursor.execute("select * from users where id=? ", (user['id'],))
    data = cursor.fetchall()
    print(data)
    if len(data) == 0:
        abort(404)
    else:
        key_list=user.keys()
        for i in key_list:
            if i != "id":
                print(user, i)
                cursor.execute("""update users set {0} = ? where id=? """.format(i), (user[i], user['id']))
                conn.commit()
    return "Success"

#   Use RESTful API to DEBUG:
#   curl -i -H "Content-Type: application/json" -X put -d '{"password":"aw56789"}' http://localhost:5000/api/v1/users/3
#

#   Tweet
def list_tweets():
    conn = sqlite3.connect('mydb.db')
    print ("Open database mydb.db successfully");
    api_list=[]
    cursor = conn.execute("select username, body, tweet_time, id from tweets")
    data = cursor.fetchall()
    if data != 0:
        for row in cursor:
            tweets = {}

            tweets['Tweet By'] = row[0]
            tweets['Body'] = row[1]
            tweets['Timestamp'] = row[2]
            tweets['id'] = row[3]

            print (tweets)
            api_list.append(tweets)
    else:
        return api_list
    conn.close()
    return jsonify({'tweets_list': api_list})

#   Use RESTful API to DEBUG:
#   curl http://localhost:5000/api/v2/tweets -v
#

def add_tweet(new_tweets):
    conn = sqlite3.connect('mydb.db')
    print ("Open database mydb.db successfully");
    cursor = conn.cursor()
    cursor = conn.execute("select * from users where username=? ", (new_tweets['username'],))
    data = cursor.fetchall()

    if len(data) == 0:
        abort(404)
    else:
        cursor.execute("insert into tweets (username, body, tweet_time) values(?,?,?)", (new_tweets['username'], new_tweets['body'], new_tweets['created_at']))
        conn.commit()
        return "Success"

#   Use RESTful API to DEBUG:
#   curl -i -H "Content-Type: application/json" -X POST -d '{"username":"haowen","body":"It works"}' http://localhost:5000/api/v2/tweets
#   curl -i -H "Content-Type: application/json" -X POST -d '{"username":"alanwalker","body":"Perfect work"}' http://localhost:5000/api/v2/tweets
#

def list_tweet(user_id):
    print("user_id:", user_id)
    conn = sqlite3.connect('mydb.db')
    print ("Open database mydb.db successfully");
    api_list=[]
    cursor = conn.cursor()
    cursor.execute("select * from tweets where id=?", (user_id,))
    data = cursor.fetchall()
    print(data)
    if len(data) == 0:
        abort(404)
    else:
        user = {}
        user['id'] = data[0][0]
        user['username'] = data[0][1]
        user['body'] = data[0][2]
        user['tweet_time'] = data[0][3]

    conn.close()
    return jsonify(user)

 #  Use RESTful API to DEBUG:
#   curl http://localhost:5000/api/v2/tweets/2
#   curl http://localhost:5000/api/v2/tweets/1
#
   

@app.route("/api/v1/info")
def home_index():
    conn = sqlite3.connect('mydb.db')
    print ("Open database mydb.db successfully");
    api_list=[]
    cursor = conn.execute("select buildtime, version, methods, links from apirelease")
    for row in cursor:
        api = {}
        api['version'] = row[0]
        api['buildtime'] = row[1]
        api['methods'] = row[2]
        api['links'] = row[3]
        api_list.append(api)
    conn.close()
    return jsonify({'api_version': api_list}), 200

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name', ""),
        'password': request.json['password']
    }
    return jsonify({'status': add_user(user)}), 201

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json: abort(400)
    user=request.json['username']
    return jsonify({'status': del_user(user)}), 200

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    if not request.json: abort(400)
    user['id']=user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    print(user)
    return jsonify({'status':upd_user(user)}), 200

# Tweet
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

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found.'}), 404)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
