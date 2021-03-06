from flask import Flask, render_template, request
from unittest import result
from pymysql import connections
import os
import boto3
from config import *
import datetime
import webbrowser

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

@app.route("/addatt", methods=['GET', 'POST'])
def addAtt():
    return render_template('AddAtt.html')

@app.route("/getatt", methods=['GET'])
def GetAtt():
    return render_template('GetAtt.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')



@app.route("/addemp", methods=['POST'])
def AddEmp():
    empid = request.form['empid']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    gender = request.form['gender']
    phone = request.form['phone']
    rate_per_day = request.form['rate_per_day']
    postiion = request.form['postiion']
    location = request.form['location']
    hired_date = request.form['hired_date']
    emp_image_file = request.files['emp_image_file']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (empid, name, gender, phone, rate_per_day, postiion, location, hired_date))
        db_conn.commit()
        name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "empid-" + str(empid) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)



@app.route("/addatt2", methods=['GET','POST'])
def AddAttOutPut():
    empid = request.form['empid']
    cursor = db_conn.cursor()
    
    now = datetime.datetime.now()
    now.strftime("%d-%m-%Y, %H:%M:%S")

    insert_sql = "INSERT INTO attendance VALUES (%s, %s)"
    cursor = db_conn.cursor()

    if empid == "":
        return "Please enter an Employee ID!"

    try:
        cursor.execute(insert_sql, (empid, now))
        db_conn.commit()

    except Exception as e:
            return str(e)

    finally:
        cursor.close()
    return render_template('AddAttOutPut.html', id=empid, now=datetime)

@app.route("/getatt2", methods=['GET', 'POST'])
def GetAttOutPut():
    cursor = db_conn.cursor()
    cursor.execute('Select * from attendance')
    results = cursor.fetchall()
    lresults = list(results)

    return render_template('GetAttOutput.html', results=lresults,)

 
