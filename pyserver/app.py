from crypt import methods
from email.base64mime import body_decode
from lib2to3.pgen2 import token
from this import d
from tokenize import group
from wsgiref import headers
from flask import Flask,request,render_template,url_for,jsonify,make_response,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import csv
from requests import Request,Response
import requests
import json
from os import listdir
from os.path import isfile, join

app = Flask(__name__)
app.secret_key = "secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
memcache = {}
data = pd.read_csv("static/data/housingDataset.csv")
# churn_df = data[(data['Churn']=="Yes").notnull( )]

UPLOAD_FOLDER = 'static/data/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    district = district
    ground = ground
    singleDicData = data.loc[data['District'] == district]
    # ground needed to be validated
    votesNum = singleDicData[ground].dropna().drop_duplicates()
    votes =[]
    votersPerVote = [] 
    for v in votesNum:
        votes.append(v)
        votersPerVote.append(len(data.loc[data[ground] == v]))
    return render_template("safety.html", labels=votes , values=votersPerVote, ground= ground , district=district)    
@app.route('/test/<district>/<ground>', methods=['GET','POST'])
def testTemplate(district, ground):
    ground ='Affordability'
    district = 'Gasabo'
    singleDicData = data.loc[data['District'] == district]
    # ground needed to be validated
    votesNum = singleDicData[ground].dropna().drop_duplicates()
    votes =[]
    votersPerVote = [] 
    for v in votesNum:
        votes.append(v)
        votersPerVote.append(len(data.loc[data[ground] == v]))
    # return render_template('test.html')
    return render_template("test.html", labels=votes , values=votersPerVote)

@app.route('/viewdataset', methods=["GET","POST"])
def viewDataset():
    sample = data.drop(['No'], axis=1).head(1000)
    # return sample.to_html(classes='table table-hover table-border', justify='center')
    return render_template('display.html', tables= [sample.to_html(classes='table table-hover table-border', justify='center')], titles=[''])

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
    for prop in data:
        print(data[prop])
    if "token" in data:
        session['token'] = data['token']
        session['role'] = data['user']['role']
        url = 'http://localhost:3000/api/v1/roles/'+str(session.get('role'))
        r = requests.get(url)
        user = json.loads(r.content)
        if 'name' not in user:
            return render_template('401.html')
        if user['name'] == 'collector':
            return render_template('upload.html')
        return redirect(url_for('dashboardController'))
    else:
        return render_template('login.html', error='Incorrect username or password')




# --------get token api------------------
@app.route('/userToken', methods=["GET"])
def getToken():
    if session.get('token') == None:
        return 'no token found', 404
    token = session['token']
    return token
# -------dashboard table------------

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
    num = len(data["No"])+1
    print("--->",fname,lname,nationalId,gender,ubudehe,district,sector,cell,village,aWater,sanitation, aInfo, wremoval,energy,security,access,affordability)
    row =[num,fname,lname,nationalId,gender,ubudehe,"URBAN",district,sector,cell,village,aWater,sanitation, aInfo, wremoval,energy,security,access,affordability]
    with open('static/data/housingDataset.csv','a') as csvFile:   #a to append to existing csv file
        writer = csv.writer(csvFile)
        # csvFile.write("\n")    #write your data to new line
        writer.writerow(row)
        csvFile.close()

    return render_template('dataForm.html')
@app.route('/dashboard', methods=["GET","POST"])
def dashboardController():
    if session.get('token') == None:
        return render_template('401.html')
    token = session['token']
    values = ["Access to water","Access to sanitation","Access information","Waste removal","Energy","Security of tenure","Accessibility","Affordability"]
    print(len(data.loc[data['Affordability']==0]))
    affordabilityPer = len(data.loc[data[values.pop()]==0])*100/len(data)
    print(affordabilityPer)
    # aWater = data['Access to water']
    # sanitation = data['Access to sanitation']
    # aInfo = data['Access information']
    # wremoval = data['Waste removal']
    # energy = data['Energy']
    # access = data['Accessibility']
    # security = data['Security of tenure']
    # affordability = data['Affordability']
    districtsList = data['District'].dropna().drop_duplicates()
    districts = []
    noPop = []
    yesPop = []
    for dc in districtsList:
        dist = str(dc)
        districts.append(dc)
        
        districtData = data.loc[data['District']==dc]
        dcSafety = []
        for item in values:
            dcSafety.append(len(districtData.loc[districtData[item]==0])*100/len(districtData))
        dcAffordability = len(districtData.loc[districtData["Affordability"]==0])*100/len(districtData)
        total = (np.average(np.array(dcSafety)) + dcAffordability) /2
        noPop.append(total)
        yesPop.append(100-total)


    temp = []
    for item in values:
        column = data[item]
        temp.append(len(column.loc[column==0])*100/len(column))
    # totalAverage = np.average(np.array(temp))
    
    safety = []
    for item in values:
        safety.append(len(data.loc[data[item]==0])*100/len(data))
    safetyPercentage = np.average(np.array(safety))
    totalAverage = (safetyPercentage + affordabilityPer) /2
    districtNum = len(districts)
    household = len(data)
    return render_template("dashboard.html",
     totalAverage = totalAverage,
    safetyPercentage=safetyPercentage,
    affordabilityPer = affordabilityPer,
    districtNum= districtNum,
    household = household,
    districts = districts,
    noPop = noPop,
    yesPop = yesPop,
     token = token)

@app.route('/genderView', methods=["GET","POST"])
def genderViewController():
    singleDicData = data.loc[data['District'] == "Gasabo"].dropna()
    values = ["Access to water","Access to sanitation","Access information","Waste removal","Energy","Security of tenure","Accessibility","Affordability"]
    labels = []
    menValues = []
    for item in values:
        print(item)
        # labels.append(len(singleDicData.loc[singleDicData[item] == 0] & singleDicData["Sex"] =="FEMALE"))
        labels.append(len(singleDicData.loc[(singleDicData[item]) == 1 &(singleDicData["Sex"] =="FEMALE")]))
        menValues.append(len(singleDicData.loc[(singleDicData[item]) == 1 &(singleDicData["Sex"] =="MALE")]))
    for item in menValues:
        print(item)
    # print('Female:',len(singleDicData.loc[(singleDicData["Access to sanitation"])]))
    # print('male:',len(singleDicData.loc[(singleDicData["Access to sanitation"] == 0) &(singleDicData["Sex"] =="MALE")]))
       
        # aWater = request.form.get('aWater')
        # sanitation = request.form.get('sanitation')
        # aInfo = request.form.get('aInfo')
        # wremoval = request.form.get('wremoval')
        # energy = request.form.get('energy')
        # access = request.form.get('access')
        # security = request.form.get('security')
        # affordability = request.form.get('affordability')
    
    # votesNum = singleDicData['Access to water'].dropna().drop_duplicates()
    # votes =[]
    # votersPerVote = [] 
    # for v in votesNum:
    #     votes.append(v)
    #     votersPerVote.append(len(data.loc[data['Access to water'] == v]))
    return render_template("gender.html",  labels=values , menValues=menValues, values=labels)
    # return render_template("gender.html")

# -------------Data upload--------------------------------------
@app.route('/upload', methods=["GET","POST"])
def upload():
    onlyfiles = [f for f in listdir('./static/data/') if isfile(join('./static/data/', f))]
    return render_template('upload.html', filenames = onlyfiles)
@app.route('/view/<filename>', methods=["GET","POST"])
def view(filename):
    try:
        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()
        return content
    except:
        return "Content Not found"
# ------------data upload backend ------------------------------
@app.route('/uploader', methods=["GET","POST"])
def dataUpload():
    if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      f.save(app.config['UPLOAD_FOLDER'] + filename)
      return render_template('upload.html')
    
@app.route('/sectors', methods=['GET','POST'])
def viewSectorsStatus():
    sectors = data['Sector'].dropna().drop_duplicates()
    values = ["Access to water","Access to sanitation","Access information","Waste removal","Energy","Security of tenure","Accessibility","Affordability"]
    secArray = []
    for sec in sectors:
        num = 0
        sectorInfo = {}
        sectorInfo['sector'] = sec
        avg = 0
        for item in values:
            num = len(data.loc[(data['Sector'] == sec) & (data[item]==0)])
            total = len(data.loc[data['Sector'] == sec])
            dt = data.loc[data['Sector'] == sec]
            print(dt)
            sectorInfo[item] = "{:.2f}".format((num * 100)/total)
            avg += (num * 100)/total
        sectorInfo['Average'] = "{:.2f}".format(avg / len(values))
        secArray.append(sectorInfo)
    newlist = sorted(secArray, key=lambda d: d['Average'], reverse=True)
    # ubudehe issues
    qauntile = data['Ubudehe(Wealth Quintile)'].dropna().drop_duplicates()
    values = ["Access to water","Access to sanitation","Access information","Waste removal","Energy","Security of tenure","Accessibility","Affordability"]
    avg = []
    qList = []
    for q in qauntile:
        num = 0
        qList.append(q)
        for item in values:
            total =  len(data.loc[data['Ubudehe(Wealth Quintile)'] == q])
            temp = len(data.loc[(data['Ubudehe(Wealth Quintile)'] == q) & (data[item]==0)])
            num += (temp * 100) / total
        avg.append("{:.2f}".format(num/len(values)))
    return render_template('sector.html',secArray=newlist, labels=qList, values=avg)
# -------------------- Ubudehe pages --------------------------------------
@app.route('/ubudehe', methods=['GET','POST'])
def testUbudehe():
    qauntile = data['Ubudehe(Wealth Quintile)'].dropna().drop_duplicates()
    values = ["Access to water","Access to sanitation","Access information","Waste removal","Energy","Security of tenure","Accessibility","Affordability"]
    avg = []
    qList = []
    for q in qauntile:
        num = 0
        qList.append(q)
        for item in values:
            total =  len(data.loc[data['Ubudehe(Wealth Quintile)'] == q])
            print(q,total)
            temp = len(data.loc[(data['Ubudehe(Wealth Quintile)'] == q) & (data[item]==0)])
            num += (temp * 100) / total
        print(q)
        avg.append("{:.2f}".format(num/len(values)))
    return render_template('sector.html', labels=qList, values=avg)

# --------------------error handle--------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# --------------------Get INFO according to region(district or sector etc)---------------------------
@app.route('/region/<region>', methods=['GET','POST'])
def viewRegionStatus(region):
    name = data[region].dropna().drop_duplicates()
    values = ["Access to water","Access to sanitation","Access information","Waste removal","Energy","Security of tenure","Accessibility","Affordability"]
    secArray = []
    for sec in name:
        num = 0
        sectorInfo = {}
        sectorInfo[region] = sec
        avg = 0
        for item in values:
            num = len(data.loc[(data[region] == sec) & (data[item]==0)])
            total = len(data.loc[data[region] == sec])
            dt = data.loc[data[region] == sec]
            sectorInfo[item] = "{:.2f}".format((num * 100)/total)
            avg += (num * 100)/total
        sectorInfo['Average'] = "{:.2f}".format(avg / len(values))
        secArray.append(sectorInfo)
    newlist = sorted(secArray, key=lambda d: d['Average'], reverse=True)
    # ubudehe issues
    qauntile = data['Ubudehe(Wealth Quintile)'].dropna().drop_duplicates()
    values = ["Access to water","Access to sanitation","Access information","Waste removal","Energy","Security of tenure","Accessibility","Affordability"]
    total = len(data)
    avg = []
    for item in values:
        num = len(data.loc[data[item]==0])
        avg.append("{:.2f}".format((num * 100) / total))
    
    
    # qList = []
    # for q in qauntile:
    #     num = 0
    #     qList.append(q)
    #     for item in values:
    #         total =  len(data.loc[data['Ubudehe(Wealth Quintile)'] == q])
    #         temp = len(data.loc[(data['Ubudehe(Wealth Quintile)'] == q) & (data[item]==0)])
    #         num += (temp * 100) / total
    #     avg.append("{:.2f}".format(num/len(values)))
    return render_template('region.html',secArray=newlist, labels=values, values=avg)
#  ---------------filter-------------------------------
@app.route('/filter/<region>/<name>', methods=['GET','POST'])
def filterBy(region,name):
    if session.get('token') == None:
        return render_template('401.html')
    values = ["Access to water","Access to sanitation","Access information","Waste removal","Energy","Security of tenure","Accessibility","Affordability"]
    regionData = data.loc[data[region]==name]
    nextName = ''
    print(name)
    if region == 'District':
        nextName = 'Sector'
    elif region == 'Sector':
        nextName= 'Cell'
    elif region == 'Cell':
        nextName = 'Village'
    else:
        nextName = 'Village'
    print(nextName)
    regionNames = regionData[nextName].dropna().drop_duplicates()
    regionArray = []
    
    for regionName in regionNames:
        num = 0
        regionInfo = {}
        regionInfo[nextName] = regionName
        avg = 0
        for item in values:
            num = len(regionData.loc[(regionData[nextName] == regionName) & (regionData[item]==0)])
            total = len(regionData.loc[regionData[nextName] == regionName])
            regionInfo[item] = "{:.2f}".format((num * 100)/total)
            avg += (num * 100)/total
        regionInfo['Average'] = "{:.2f}".format(avg / len(values))
        regionArray.append(regionInfo)
    newlist = sorted(regionArray, key=lambda d: d['Average'], reverse=True)

    
    # region analytics
    total = len(regionData)
    if total == 0:
        return render_template('404.html')
    avg = []
    for item in values:
        num = len(regionData.loc[(regionData[region]==name) & (data[item]==0)])
        avg.append("{:.2f}".format((num * 100) / total))
    
    return render_template('region.html',secArray=newlist, labels=values, values=avg)
# ----------------------Data collection------------------------------
@app.route('/collector', methods=['GET','POST'])
def dtCollectionDashboard():
    if session.get('token') == None:
        return render_template('401.html')
    if session.get('role') == None:
        return render_template('401.html')
    url = 'http://localhost:3000/api/v1/roles/'+str(session.get('role'))
    r = requests.get(url)
    user = json.loads(r.content)
    if 'name' not in user:
        return render_template('401.html')
    if user['name'] != 'collector':
        return render_template('401.html')
    return render_template('upload.html')
# ----------------------signup------------------------------------
@app.route('/signup', methods=['GET','POST'])
def userSignup():
    return render_template('signup.html')
@app.route('/signupController', methods=['GET','POST'])
def signupController():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    birthday = request.form['birthday']
    gender = request.form['gender']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    phone = request.form['phone']
    headers = {
        'content-type': 'application/json',
        'authorization':'Bearer '+session.get('token')}
    r = requests.post('http://localhost:3000/api/v1/users', json= {
        'email': email,
        'firstName':firstName,
        'lastName':lastName,
        'dateofbirth':birthday,
        'gender':gender,
        'address':address,
        'phoneNo':phone
         },
         headers=headers)
    data = json.loads(r.content)
    print(data)
    # ------------required error message
    error = data['message']
    return render_template('signup.html',error= error)
# ----------------render to filter page---------
@app.route('/filter' , methods=['GET','POST'])
def renderToFilter():
    return render_template('region.html')
# ----------------LOGOUT---------
@app.route('/logout' , methods=['GET','POST'])
def logout():
    try:
        headers = {
            'content-type': 'application/json',
            'authorization':'Bearer '+session.get('token')}
        r = requests.post('http://localhost:3000/api/auth/logout',headers=headers)
        session.clear()
    except:
        return render_template('index.html')
    return render_template('index.html')

@app.route('/test' , methods=['GET','POST'])
def getHomePage():
    return render_template('index.html')
@app.route('/num')
def getLastNum():
    num = len(data["No"])
    print(num)
    return render_template('dataForm.html')
if __name__ == "__main__":
    app.run(debug=True)