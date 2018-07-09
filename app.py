from flask import Flask, render_template, request, jsonify
import pymysql.cursors
import pymysql
import sys
import json
import requests


connection = pymysql.connect(host='adnap.co',
                             user='cfarley9_Admin',
                             password='Heero4501',
                             db='cfarley9_fashion',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print(connection)
try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()


app = Flask(__name__)

@app.route('/getFeedPost', methods=['GET', 'POST'])
def getFeedPost():
    data = request.json
    return 'Hello, World!'

@app.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
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
    data = request.json
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO 'post' ('name', 'description', 'category','userID') VALUES (%s,%s)"
            cursor.execute(sql, (data["name"], data["description"],data["category"],data["userID"]))

            connection.commit()
    finally:
        connection.close()

    return "success"

@app.route('/updatePost', methods=['GET', 'POST'])
def updatePost():
    data = request.json
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE 'post' SET '%s' = '%s' WHERE 'clothingID' = %s"
            cursor.execute(sql, (data["key"], data["value"],data["clothingID"]))

            connection.commit()
    finally:
        connection.close()

    return "success"