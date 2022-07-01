from crypt import methods
from email.base64mime import body_decode
from lib2to3.pgen2 import token
from wsgiref import headers
from flask import Flask,request,render_template,url_for,jsonify,make_response,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import numpy as np
import csv
from requests import Request,Response
import requests
import json

app = Flask(__name__)
app.secret_key = "secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
memcache = {}
data = pd.read_csv("static/data/housingDataset.csv")
# churn_df = data[(data['Churn']=="Yes").notnull( )]


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, unique=True, nullable=False)
    completed = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r' % self.id

@app.route('/')
def index():
    return render_template('landingPage.html')

@app.route('/home/<name>')
def hello(name):
    methodType = request.method
    return f"hello {name} {methodType}"

@app.route('/user', methods=["GET","POST"])
def createUser():
    if request.method == "POST":
        memcache.update(request.json)
        return "success"
    else:
        return jsonify(memcache)

@app.route('/graphs', methods=["GET","POST"])
def home():
    districtsList = data['District'].dropna().drop_duplicates()
    populationPerDistrict = []
    districts = []
    for dc in districtsList:
        dist = str(dc)
        districts.append(dc)
        populationPerDistrict.append(data['District'].value_counts()[dc])
    print(districts)
    # print(groupby(["District"]).count().sort_values(["District"],ascending=False))
    print('type : ',populationPerDistrict)
    # for total in list(data['District'].value_counts()):
    #     # print(list(data['District'].value_counts()).index(total),'--->',total)
    #     populationPerDistrict.append(total)
    print('population per district',populationPerDistrict)
    print('districts :',districts)
    return render_template("graph.html", labels=districts , values=populationPerDistrict)

@app.route('/writeData', methods=["GET","POST"])
def appendData():
    row =['Eric', '60']
    with open('static/data/housingDataset.csv','a') as csvFile:   #a to append to existing csv file
        writer = csv.writer(csvFile)
        csvFile.write("\n")    #write your data to new line
        writer.writerow(row)
    csvFile.close()
    print('data appended')
    return "sucess"
    
@app.route('/safeGraph/<district>', methods=["GET","POST"])
def safeGraph(district):
    singleDicData = data.loc[data['District'] == district]
    votesNum = singleDicData['Access to water'].dropna().drop_duplicates()
    votes =[]
    votersPerVote = [] 
    for v in votesNum:
        votes.append(v)
        votersPerVote.append(len(data.loc[data['Access to water'] == v]))
    return render_template("safety.html", labels=votes , values=votersPerVote)

@app.route('/safeGraph/<district>/<ground>', methods=["GET","POST"])
def graphAim(district, ground):
    print(ground)
    singleDicData = data.loc[data['District'] == district]
    # ground needed to be balidated
    votesNum = singleDicData[ground].dropna().drop_duplicates()
    votes =[]
    votersPerVote = [] 
    for v in votesNum:
        votes.append(v)
        votersPerVote.append(len(data.loc[data['Access to water'] == v]))
    return render_template("safety.html", labels=votes , values=votersPerVote)    


@app.route('/viewdataset', methods=["GET","POST"])
def viewDataset():
    return render_template('display.html', tables= [data.to_html(classes='table table-hover table-border', justify='center')], titles=[''])

@app.route('/login')
def loginPage():
    return render_template('login.html')
@app.route('/loginController', methods=["POST"])
def loginController():
    # missing try and catch and same validation
    email = request.form['email']
    password = request.form['password']
    print(email,password)
    headers = {'content-type': 'application/json'}
    r = requests.post('http://localhost:3000/api/v1/auth/login', json= {'email': email, 'password':password})
    data = json.loads(r.content)
    print(data)
    for prop in data:
        print(data[prop])
    if "token" in data:
        session['token'] = data['token']
        return redirect(url_for('dashboardController'))
    else:
        return render_template('login.html', error='Incorrect username or password')

@app.route('/dashboard', methods=["GET","POST"])
def dashboardController():
    # missing try and catch and same validation
    print(session['token'])
    print(request.headers)
    return render_template("dashboard.html")
@app.route('/dt-form', methods=["GET","POST"])
def dataForm():
    return render_template('dataForm.html')
@app.route('/formvalidation', methods=["POST"])
def dataFormController():
    fname = request.form.get('firstname')
    lname = request.form.get('lastname')
    gender = request.form.get('gender')
    nationalId = request.form.get('nationalId')
    district = request.form.get('district')
    sector = request.form.get('sector')
    cell = request.form.get('cell')
    village = request.form.get('village')
    
    ubudehe = request.form.get('ubudehe')
    aWater = request.form.get('aWater')
    sanitation = request.form.get('sanitation')
    aInfo = request.form.get('aInfo')
    wremoval = request.form.get('wremoval')
    energy = request.form.get('energy')
    access = request.form.get('access')
    security = request.form.get('security')
    affordability = request.form.get('affordability')

    print("--->",fname,lname,nationalId,gender,ubudehe,district,sector,cell,village,aWater,sanitation, aInfo, wremoval,energy,security,access,affordability)
    row =["",fname,lname,nationalId,gender,ubudehe,"URBAN",district,sector,cell,village,aWater,sanitation, aInfo, wremoval,energy,security,access,affordability]
    with open('static/data/housingDataset.csv','a') as csvFile:   #a to append to existing csv file
        writer = csv.writer(csvFile)
        # csvFile.write("\n")    #write your data to new line
        writer.writerow(row)
        csvFile.close()

    return "Table validated"
@app.route('/test', methods=["GET","POST"])
def testDashboard():
    return render_template("dashboard.html")
if __name__ == "__main__":
    app.run(debug=True)