# Haowen Huang modified on Sep 21, 2019
# Implementation of Cloud Native web applications
# Part One: Developing a RESTful micro service in Python 
# 
# http://localhost:5000/api/v1/info  
# http://localhost:5000/api/v1/users
#
#

from flask import Flask, request, jsonify
from flask import make_response
import json
import sqlite3

app = Flask(__name__)

def list_users():
    conn = sqlite3.connect('mydb.db')
    print ("Open database mydb.db successfully");
    api_list=[]
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

#   Use API to DEBUG:
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

#   Use API to DEBUG:
#   curl -i -H "Content-Type: application/json" -X delete -d '{"username":"michael123"}' http://localhost:5000/api/v1/users
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


@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found.'}), 404)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

