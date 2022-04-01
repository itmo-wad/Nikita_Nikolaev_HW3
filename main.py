from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/general"
mongo = PyMongo(app)


@app.route('/')
def home_page():
    online_users=mongo.db.users.find({})
    return render_template("homepage.html",users=online_users)

@app.route("/auth", methods=["GET","POST"])
def auth():
    if request.method == "GET":
        return render_template("auth.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        print(username)
        print(password)
        if mongo.db.general.find_one({"username": username, "password": password}):
            return redirect('profile')
        else:
            return 'Incorrect!!!'


@app.route('/history', methods =['GET','POST'])
def history():
    if request.method == 'POST':
        posts=list(mongo.db.history.find())
        for data in posts:
            print(data)
        return render_template('history.html',posts=posts)


@app.route('/profile')
def profile():
        return render_template("blog.html")

@app.route('/postpage', methods=['POST'])
def postblog():
    if request.method == "POST":
        return render_template('message.html')


@app.route('/postmessage', methods=['POST'])
def postmessage():
    if request.method == "POST":
        message=request.form.get("message")
        mongo.db.history.insert_one({"message":message})
        return render_template('blog.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)