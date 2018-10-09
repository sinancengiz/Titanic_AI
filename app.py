# import necessary libraries
import os
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/titanic_db.sqlite" 

#Use joblib to load the most accurate machine learning model
svc = joblib.load('Resources/models/svc.pkl') 
svc_scaler = joblib.load('Resources/models/svc_scaler.pkl') 

#Initialize app
db = SQLAlchemy(app)
#Define database table structure from Flask app
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    pclass = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    age = db.Column(db.Integer)
    sibsp = db.Column(db.Integer)
    parch = db.Column(db.Integer)
    fare = db.Column(db.Integer)
    embarked = db.Column(db.Integer)
    survived = db.Column(db.Integer)
    
    def __init__(self, name, pclass, sex, age, sibsp, parch, fare, embarked, survived ):
        self.name = name
        self.pclass = pclass
        self.sex = sex
        self.age = age
        self.sibsp = sibsp
        self.parch = parch
        self.fare = fare
        self.embarked = embarked
        self.survived = survived
        

    def __repr__(self):
        return '<User %r>' % (self.name)
#Reflect the train_data table into the Flask app
class Passenger(db.Model):
    __tablename__ = 'train_data'
    db.reflect()
   


@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.create_all()
    
    #Define list to store the input from the form.
    #Pclass, Sex, Age, SibSp, Parch, Fare, Embarked is the newUser format
    newUser=[3,0,35,0,0,100,1]
    newUser = svc_scaler.transform([newUser])

    # make prediction with the form data
    prediction = svc.predict(newUser)
    print(prediction)


@app.route("/")
def index():

    return render_template("index.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    newUser = [0,0,0,0,0,0,0] 
    if request.method == "POST":
               
        userName = request.form["userName"]
        userPclass = request.form["userPclass"]
        userEmbarked = request.form["userEmbarked"]
        userAge = request.form["userAge"]
        userTicket= request.form["userTicket"]
        # userGender= request.form["userGender"]
        userDropDownGender= request.form["userDropDownGender"]

        print(userDropDownGender)

        # newUser[0] = userPclass

        if userPclass.lower() == "f":
            newUser[0] = 0
        elif userPclass.lower() == "s":
            newUser[0] = 1
        elif userPclass.lower() == "t":
            newUser[0] = 2

        # if userGender.lower() == "male":
        #     newUser[1] = 0
        # else:
        #     newUser[1] = 1

        if userDropDownGender == "gender1":
            newUser[1] = 0
        else:
            newUser[1] = 1


        newUser[2] = int(userAge)

        newUser[3] = 0
        newUser[4] = 0
        newUser[5] = userTicket
        
        
        if userEmbarked.lower() == "c":
            newUser[6] = 0
        elif userEmbarked.lower() == "q":
            newUser[6] = 1
        elif userEmbarked.lower() == "s":
            newUser[6] = 2


        testUser = svc_scaler.transform([newUser])
        prediction = svc.predict(testUser)

        user = User(name=userName, pclass=newUser[0], sex=newUser[1],
                    age=userAge, sibsp = 0, parch = 0, fare = newUser[5],
                    embarked = newUser[6], survived=int(prediction[0])
                   )

        db.session.add(user)
        db.session.commit()

        results = db.session.query(User.name, User.pclass, User.sex, 
                                   User.age,  User.sibsp,  User.parch, 
                                   User.fare, User.embarked, User.survived).all()

        name = [result[0] for result in results]
        pclass = [result[1] for result in results]
        sex = [int(result[2]) for result in results]
        age = [int(result[3]) for result in results]
        sibsp = [int(result[4]) for result in results]
        parch = [int(result[5]) for result in results]
        fare = [result[6] for result in results]
        embarked = [result[7] for result in results]
        survived = [int(result[8]) for result in results]


        plot_trace = {
            "name": name,
            "Pclass": pclass,
            "Gender": sex,
            "Age": age,
            "Sibsp": sibsp,
            "Parch": parch,
            "fare": age,
            "Embarked": embarked,
            "Survived": survived,
        }
        
        return redirect("/result", code=302)

    return render_template("form.html")


@app.route("/result")
def result():

    results = db.session.query(User.name, User.pclass, User.sex, 
                                   User.age,  User.sibsp,  User.parch, 
                                   User.fare, User.embarked, User.survived).all()

    name = [result[0] for result in results]
    pclass = [int(result[1]) for result in results]
    sex = [int(result[2]) for result in results]
    age = [int(result[3]) for result in results]
    sibsp = [int(result[4]) for result in results]
    parch = [int(result[5]) for result in results]
    fare = [result[6] for result in results]
    embarked = [result[7] for result in results]
    survived = [int(result[8]) for result in results]


    newUser = [ pclass[-1], sex[-1], age[-1],
                sibsp[-1], parch[-1], fare[-1],
                embarked[-1] ]

    testUser = svc_scaler.transform([newUser])
    prediction = svc.predict(testUser)
    chance = svc.predict_proba(testUser)
    percentage = (chance[0][1]*100)
    percentage = round(percentage, 2)


    if prediction == 1:
        return render_template('result.html', prediction = "Survive", percentage = percentage, result_list = newUser )
    else:
        return render_template('result.html', prediction = "Die", percentage = percentage, result_list = newUser )

@app.route("/embarked")
def embarked():
    
    #Same query method as used in the /plot route
    results = db.session.query(User.embarked,User.survived).all()
    embarkedlist = [result[0] for result in results]
    survivedlist = [result[1] for result in results]
    embarkedes = list(set(embarkedlist))
    embarkedcounts = []
    
    for embarked in embarkedes:
        counter = 0
        for x in range(0, len(embarkedlist)):
            if(str(embarkedlist[x]) == str(embarked) ):
                counter=counter+1
        embarkedcounts.append(counter)
    
    embarked_trace = {
        "x": ["Cherbourg","Queenstown","Southampton"],
        "y": embarkedcounts,
        "type": "bar"
    }
    return jsonify(embarked_trace)

@app.route("/gender")
def gender():
    
    #Same query method as used in the /plot route
    results = db.session.query(User.sex, User.survived).all()
    sexlist = [result[0] for result in results]
    survivedlist = [result[1] for result in results]
    sexes = list(set(sexlist))
    sexcounts = []
    
    for sex in sexes:
        counter = 0
        for x in range(0, len(sexlist)):
            if( str(sexlist[x]) == str(sex) ):
                counter=counter+1
        sexcounts.append(counter)
    
    sex_trace = {
        "x": ["Male","Female"],
        "y": sexcounts,
        "type": "bar"
    }
    return jsonify(sex_trace)

@app.route("/pasgender")
def pasgender():
    
    #Same query method as used in the /plot route
    results = db.session.query(Passenger.Sex, Passenger.Survived).all()
    sexlist = [result[0] for result in results]
    survivedlist = [result[1] for result in results]
    sexes = list(set(sexlist))
    sexcounts = []
    
    for sex in sexes:
        counter = 0
        for x in range(0, len(sexlist)):
            if(str(sexlist[x]) == str(sex) ):
                counter=counter+1
        sexcounts.append(counter)
    
    sex_trace = {
        "x": ["Male","Female"],
        "y": sexcounts,
        "type": "bar"
    }
    return jsonify(sex_trace)


@app.route("/pasclass")
def pasclass():
    
    #Same query method as used in the /plot route
    results = db.session.query(Passenger.Pclass, Passenger.Survived).all()
    sexlist = [result[0] for result in results]
    survivedlist = [result[1] for result in results]
    sexes = list(set(sexlist))
    sexcounts = []
    
    for sex in sexes:
        counter = 0
        for x in range(0, len(sexlist)):
            if(str(sexlist[x]) == str(sex) ):
                counter=counter+1
        sexcounts.append(counter)
    
    sex_trace = {
        "x": ["First Class","Second Class", "Third Class"],
        "y": sexcounts,
        "type": "bar"
    }
    return jsonify(sex_trace)

#Run the app. debug=True is essential to be able to rerun the server any time changes are saved to the Python file
if __name__ == "__main__":
    app.run(debug=True, port=5019)