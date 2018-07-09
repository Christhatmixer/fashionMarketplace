from flask import Flask, render_template, request, jsonify
import pymysql.cursors
import pymysql
import sys
import json
import requests







app = Flask(__name__)

@app.route('/getFeedPost', methods=['GET', 'POST'])
def getFeedPost():
    data = request.json
    return 'Hello, World!'

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
            sql = "INSERT INTO 'users' ('userID', 'email', 'name','profileImageURL') VALUES (%s,%s)"
            cursor.execute(sql, (data["userID"], data["email"],data["name"],data["profileImageURL"]))

            connection.commit()
    finally:
        connection.close()

    return "success"

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
            sql = "INSERT INTO 'post' (name, description, category,userID) VALUES (%s,%s,%s,%s,%s)" % (data["name"], data["description"],data["category"],data["userID"],data["clothingID"])
            cursor.execute(sql)

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
            sql = "UPDATE 'post' SET {key} = '{value}' WHERE clothingID = '{clothingID}'".format(key=data["key"], value=data["value"],clothingID=data["clothingID"])
            cursor.execute(sql)

            connection.commit()
    finally:
        connection.close()

    return "success"

if __name__ == '__main__':
    app.run()