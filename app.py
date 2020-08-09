from flask import Flask, render_template, request, redirect, url_for, flash

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['MONGO_URI'] = "mongodb://localhost:27017/Flask"

mongo = PyMongo(app)


# This is the index route where we are going to
# query on all our employee data
@app.route('/')
def Index():
    all_data = mongo.db.employees.find()

    return render_template("index.html", employees=all_data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        datas = mongo.db.employees.find()
        resp = dumps(datas)
        print(resp)
        a = len(resp)
        a = a+1

        mongo.db.employees.insert(
            {"no": a, "name": name, "email": email, "phone": phone})

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        mongo.db.employees.find_one_and_update({"no": request.form['no']}, {"$set": {
                                               "name": request.form['name'], "email": request.form['email'], "phone": request.form['phone']}})

        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))


# This route is for deleting our employee
@app.route('/delete/<no>/', methods=['GET', 'POST'])
def delete(no):
    mongo.db.employees.delete_one({"no": no})
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)