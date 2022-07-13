from datetime import timedelta
from setting import DB
import requests
from flask import Blueprint, render_template, redirect, json, url_for
import mysql.connector
from mysql.connector import Error
from flask import request, session, jsonify
from flask import Flask
# about blueprint definition
from flask import request, session
import time
import random

import app

assignment_4 = Blueprint('assignment_4', __name__, static_folder='static', static_url_path='/assignment_4',
                         template_folder='templates')

@assignment_4.route('/assignment_4')
def ass4_func():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment_4.html', users=users_list)

@assignment_4.route('/assignment4/outer_source')
def frontend_func():
    return render_template('assignment4_outerSource.html')

@assignment_4.route('/assignment4/users')
def assignment4_users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    users_json = json.dumps(users_list)
    return users_json

@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    username = request.form['user_name']
    email = request.form['email']
    password=request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    user_age = request.form['user_age']
    city = request.form['city']
    fav_player = request.form['fav_player']
    user_id = request.form['id']
    errorMSG = ""
    goodMSG = ""

    try:
        query = "INSERT INTO users(user_name, email,password_user , first_name,last_name,age,city,fav_player, user_id) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
        username, email, password, first_name, last_name, user_age, city, fav_player, user_id)

        interact_db(query=query, query_type='commit')
        session['goodMSG'] = username + " added successfully"
    except Error as er:
        session['errorMSG'] = username + " already exists"
    return redirect('/assignment_4')


@assignment_4.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_id = request.form['id']
    connection = mysql.connector.connect(**DB)
    #connection = mysql.connector.connect(host='localhost',
     #                                    user='root',
       #                                  passwd='root',
        #                                 database='ass4schema')
    check = "select * FROM users WHERE user_id='%s';" % user_id
    users_list = interact_db(check, query_type='fetch')
    if len(users_list) > 0:
        query = "DELETE FROM users WHERE user_id='%s';" % user_id
        # print(query)
        interact_db(query, query_type='commit')
        session['goodMSG'] = user_id + " deleted"
    else:
        session['errorMSG']="User id: "+user_id + " do not exist"

    return redirect('/assignment_4')

@assignment_4.route('/update_user', methods=['POST'])
def update_user_func():
    username = request.form['user_name']
    email = request.form['email']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    user_age = request.form['user_age']
    city = request.form['city']
    fav_player = request.form['fav_player']
    user_id = request.form['id']

    try:
        connection = mysql.connector.connect(**DB)
       # connection = mysql.connector.connect(host='localhost',
       #                                      user='root',
       #                                      passwd='root',
       #                                      database='ass4schema')
        check = "select * FROM users WHERE user_id='%s';" % user_id
        users_list = interact_db(check, query_type='fetch')
        if len(users_list) > 0:
            updateCursor = connection.cursor()
            updateCursor.execute('''
                        UPDATE users
                        SET user_name = %s, email = %s,password_user = %s, first_name = %s, last_name = %s, age = %s, city = %s, fav_player = %s
                        WHERE user_id = %s
                        ''', (username, email, password, first_name, last_name, user_age, city, fav_player, user_id))
            connection.commit()
            session['goodMSG'] = username + " details updates"
        else:
            session['errorMSG']="User id: "+user_id + " do not exist"
    except Error as er:
        session['errorMSG'] = "Error happend " + username

    finally:
        connection.close()

    return redirect('/assignment_4')

@assignment_4.route('/fetch_be')
def fetch_be_func():
    if 'type' in request.args:
        id = int(request.args['num_id'])
        session['num'] = id
        avatars = get_avatar(id)
        print(avatars)
        print(len(avatars))
        save_users_to_session(avatars)
    else:
        session.clear()
    return redirect('/assignment4/outer_source')

def get_avatar(id):

    avatars = []
    res = requests.get(f'https://reqres.in/api/users/{id}')
    if res.status_code==404:
        rnd = random.randint(1, 10)
        res = requests.get(f'https://reqres.in/api/users/{rnd}')

    print(res)
    avatars.append(res.json())
    return avatars


def save_users_to_session(avatars):
    users_list_to_save = []
    print(avatars)
    if avatars=="[{}]":
        print("true")
        avatars = get_avatar(5)

    for avatar in avatars:
        avatars_dict = {
            'data': {
                'avatar': avatar['data']['avatar']
            },
            'email': avatar['data']['email'],
            'first_name': avatar['data']['first_name'],

        }
        users_list_to_save.append(avatars_dict)
    session['avatars'] = users_list_to_save
    session['start'] = True

@assignment_4.route('/assignment4/restapi_users', defaults={'USER_ID': -1})
@assignment_4.route('/assignment4/restapi_users/<int:USER_ID>')
def get_users_func(USER_ID):
    if USER_ID == -1:
        print("yes -1")
        return_dict = {}
        query = 'select * from users;'
        users = interact_db(query, query_type='fetch')
        return_DefaultUser = {
            'status': 'success',
            'user_name': users[0].user_name,
            'email': users[0].email,
            'age': users[0].age,
        }
    else:
        print(USER_ID)
        query = "select * from users where user_id='%s';" % USER_ID
        users = interact_db(query=query, query_type='fetch')
        print(len(users))
        if len(users) == 0:
            return_dict = {
                'status': 'failed',
                'message': 'user not found'
            }
        else:

            return_dict = {
                'status': 'success',
                'user_name': users[0].user_name,
                'email': users[0].email,
                'age': users[0].age,
            }
    return jsonify(return_dict)

def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(**DB)
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    #

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value