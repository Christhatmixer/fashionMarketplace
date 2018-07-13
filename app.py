from flask import Flask, render_template, request, jsonify
import pymysql.cursors
import pymysql
import sys
import json
import requests







app = Flask(__name__)
# RETRIEVE POST
@app.route('/getFeedPost', methods=['GET', 'POST'])
def getFeedPost():
    data = request.json
    connection = pymysql.connect(host='adnap.co',
                                 user='cfarley9_Admin',
                                 password='Heero4501',
                                 db='cfarley9_fashion',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM post, followings WHERE userID = '{userID}'".format(userID=data["userID"])
            cursor.execute(sql)

            result = cursor.fetchall()
            print(result)

            connection.commit()
    finally:
        connection.close()
    return 'Hello, World!'

@app.route('/getUserPost', methods=['GET', 'POST'])
def getUserPost():
    data = request.json
    connection = pymysql.connect(host='adnap.co',
                                 user='cfarley9_Admin',
                                 password='Heero4501',
                                 db='cfarley9_fashion',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM post WHERE userID = '{userID}'".format(userID=data["userID"])
            cursor.execute(sql)

            result = cursor.fetchall()
            print(result)

            connection.commit()
    finally:
        connection.close()
    return jsonify(result)
@app.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
    connection = pymysql.connect(host='adnap.co',
                                 user='cfarley9_Admin',
                                 password='Heero4501',
                                 db='cfarley9_fashion',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    data = request.json
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (userID, email, name,username,profileImageURL) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, (data["userID"], data["email"],data["name"],data["profileImageURL"]))

            connection.commit()
    finally:
        connection.close()

    return "success"


#EDIT AND ADD POST

@app.route('/newPost', methods=['GET', 'POST'])
def newPost():
    connection = pymysql.connect(host='adnap.co',
                                 user='cfarley9_Admin',
                                 password='Heero4501',
                                 db='cfarley9_fashion',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    data = request.json
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO post (name,description,category,userID,clothingID) VALUES ('{name}','{description}','{category}','{userID}','{clothingID}')".format(name=data["name"],description=data["description"],category=data["category"],
                                                                                                                                                        userID=data["userID"],clothingID=data["clothingID"])
            cursor.execute(sql)
            print(sql)
            connection.commit()
    finally:
        connection.close()

    return "success"

@app.route('/updatePost', methods=['GET', 'POST'])
def updatePost():
    data = request.json
    connection = pymysql.connect(host='adnap.co',
                                 user='cfarley9_Admin',
                                 password='Heero4501',
                                 db='cfarley9_fashion',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "UPDATE post SET {key} = '{value}' WHERE clothingID = '{clothingID}'".format(key=data["key"], value=data["value"],clothingID=data["clothingID"])
            print(sql)
            cursor.execute(sql)

            connection.commit()
    finally:
        connection.close()

    return "success"


# SEARCHING
@app.route('/searchUsers', methods=['GET', 'POST'])
def searchUsers():
    data = request.json
    connection = pymysql.connect(host='adnap.co',
                                 user='cfarley9_Admin',
                                 password='Heero4501',
                                 db='cfarley9_fashion',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE userName LIKE '{query}%' LIMIT 10".format(query=data["query"])
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            connection.commit()
    finally:
        connection.close()
    return jsonify(result)



# RELATIONSHOP MANAGEMENT
@app.route('/followUser', methods=['GET', 'POST'])
def followUser():
    data = request.json
    connection = pymysql.connect(host='adnap.co',
                                 user='cfarley9_Admin',
                                 password='Heero4501',
                                 db='cfarley9_fashion',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO followings (userID, followingID, dateCreated) VALUES ('{userID}','{followingID}')".format(userID=data["userID"], followingID=data["followingID"])
            print(sql)
            cursor.execute(sql)

            connection.commit()
    finally:
        connection.close()
    return "success"

if __name__ == '__main__':
    app.run()