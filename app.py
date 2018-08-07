from flask import Flask, render_template, request, jsonify
import pymysql.cursors
import pymysql
import psycopg2
import sys
import json
import requests
from urllib.parse import urlparse
import os






app = Flask(__name__)
app.config['DATABASE_URL'] = os.environ['DATABASE_URL']

# RETRIEVE POST
@app.route('/getFeed', methods=['GET', 'POST'])
def getFeedPost():
    data = request.json

    connection = psycopg2.connect(app.config["DATABASE_URL"])
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM post INNER JOIN followings ON 'post.userID' = followings.followingID WHERE followings.userID = '{userID}'".format(userID=data["userID"])


            cursor.execute(sql)

            result = cursor.fetchall()
            print(result)

            connection.commit()
    finally:
        connection.close()
    return jsonify(result)

@app.route('/getUserPost', methods=['GET', 'POST'])
def getUserPost():
    data = request.json
    connection = psycopg2.connect(app.config["DATABASE_URL"])
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
    connection = psycopg2.connect(app.config["DATABASE_URL"])

    data = request.json
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (userID, email, name,username,profileImageURL) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, (data["userID"], data["email"],data["name"],data["username"],data["profileImageURL"]))

            connection.commit()
    finally:
        connection.close()

    return "success"

@app.route('/getUserInfo', methods=['GET', 'POST'])
def getUserInfo():
    connection = psycopg2.connect(app.config["DATABASE_URL"])

    data = request.json
    try:
        with connection.cursor() as cursor:
            sql = "SELECT 1 FROM users WHERE userID = %s"
            cursor.execute(sql, data["userID"])
            result = cursor.fetchall()
            print(result)

            connection.commit()
    finally:
        connection.close()

    return jsonify(result)


# EDIT AND ADD POST

@app.route('/newPost', methods=['GET', 'POST'])
def newPost():
    connection = psycopg2.connect(app.config["DATABASE_URL"])

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
    connection = psycopg2.connect(app.config["DATABASE_URL"])

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
    connection = psycopg2.connect(app.config["DATABASE_URL"])
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
@app.route('/checkFollow', methods=['GET', 'POST'])
def checkFollow():
    data = request.json
    connection = psycopg2.connect(app.config["DATABASE_URL"])
    try:
        with connection.cursor() as cursor:
            sql = "select 1 FROM followings WHERE userID = '{userID}' AND followingID = '{otherUserID}'".format(
                userID=data["userID"], otherUserID=data["otherUserID"])
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            connection.commit()
    finally:
        connection.close()
    return jsonify(result)



@app.route('/followUser', methods=['GET', 'POST'])
def followUser():
    data = request.json
    connection = psycopg2.connect(app.config["DATABASE_URL"])
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO followings (userID, followingID) VALUES ('{userID}','{followingID}')".format(userID=data["userID"], followingID=data["followingID"])
            print(sql)
            cursor.execute(sql)

            connection.commit()
    finally:
        connection.close()
    return "success"

@app.route('/unfollowUser', methods=['GET', 'POST'])
def unfollowUser():
    data = request.json

    connection = psycopg2.connect(app.config["DATABASE_URL"])
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM followings WHERE userID = '{userID}' AND followingID = '{followingID}'".format(userID=data["userID"], followingID=data["followingID"])
            print(sql)
            cursor.execute(sql)

            connection.commit()
    finally:
        connection.close()
    return "success"

if __name__ == '__main__':
    app.run()
