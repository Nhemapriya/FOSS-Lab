from flask import Flask, render_template, request
import pymongo


app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://practiceUser:practiceUser@cluster0.vm6pv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = client["Railways"]
mycol = mydb["UserData"]


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/addPage")
def addPage():
    return render_template("bookTicket.html")

@app.route("/add", methods=['POST'])
def addTicket():
    tno = request.form['tno']
    tname = request.form['tname']
    tstart = request.form['tstart']
    tend = request.form['tend']
    tpass = request.form['tpass']
    tamt = (int(tpass)*500)

    ticket = {
        "tno":tno, "tname":tname, "tstart" :tstart, "tend" :tend, "tpass":tpass, "tamt" :tamt
    }
    mycol.insert_one(ticket)
    return "values inserted successfully"


@app.route("/view")
def view():
    temp = []
    for entry in mycol.find():
        temp.append(entry)
    return render_template("view.html", tickets=temp)

@app.route("/deletePage")
def deletePage():
    return render_template("deletePage.html")

@app.route("/delete", methods=['POST'])
def delete():
    tno = request.form['no']
    temp = {"tno": tno}
    mycol.delete_one(temp)

    #remianing values
    arr = []
    for x in mycol.find():
        arr.append(x)

    return render_template("view.html", tickets=arr)

@app.route("/updatePage")
def updatePages():
    return render_template("updatePage.html")

@app.route("/update", methods=["POST"])
def deleteEntry():
    tfield = request.form['tfield']
    old = request.form['oldvalue']
    newval = request.form["newvalue"]
    query = {tfield:old}
    updated =  {"$set" : {tfield:newval}}
    mycol.update_one(query, updated)

    arr=[]
    for x in mycol.find():
        arr.append(x)

    return render_template("view.html", tickets=arr)

if __name__ == "__main__":
    app.run(debug=True)