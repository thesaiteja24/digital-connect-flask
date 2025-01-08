from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
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


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.users.find_one({"email": email})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['email'] = email
            session['username'] = user['username']  # Store username in session
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template('login.html')

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
        username = request.form['username']
        password = request.form['password']
        email = request.form["email"]
        role = request.form["role"]

        existing_user = mongo.users.find_one({"email": email})
        if existing_user:
            return "Username already exists. Please choose another."

        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        mongo.users.insert_one(
            {"username": username, "email": email, "password": hashed_password, "role": role})

        return redirect(url_for('login'))

    return render_template('register.html')


@ app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/home")
def home():
    if 'user_id' in session:  # Check if the user is logged in
        user = mongo.users.find_one(
            {"_id": ObjectId(session['user_id'])})  # Get user from DB
        if user:
            username = user['username']
            return render_template('home.html', username=username)
    return redirect(url_for('login'))  # Redirect to login if not logged in


if __name__ == '__main__':
    app.run()
