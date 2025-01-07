from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
import certifi
import os

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI") + certifi.where()
app.secret_key = "your_secret_key"

# Initialize PyMongo
mongo = PyMongo(app).db
bcrypt = Bcrypt(app)


@app.route("/")
def render_login():
    return render_template('login.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.users.find_one({"email": email})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['email'] = email
            return redirect(url_for('home'))
        else:
            flash("User not found. Please sign up.", "danger")

    return render_template('login.html')

@ app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        email=request.form["email"]
        role=request.form["role"]

        existing_user=mongo.users.find_one({"email": email})
        if existing_user:
            return "Username already exists. Please choose another."

        hashed_password=bcrypt.generate_password_hash(
            password).decode('utf-8')
        mongo.users.insert_one(
            {"username": username, "email": email, "password": hashed_password, "role": role})

        return redirect(url_for('user_routes.render_login'))

    return render_template('register.html')

@ app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
