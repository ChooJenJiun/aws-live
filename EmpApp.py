from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')


@app.route("/addemp", methods=['POST'])
def AddEmp():
    empid = request.form['empid']
    date = request.form['date']
    time = request.form['time']

    insert_sql = "INSERT INTO attendance VALUES (%s, %s, %s)"
    cursor = db_conn.cursor()

    

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', id=empid, date=date, time=time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
