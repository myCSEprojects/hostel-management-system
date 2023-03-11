from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "M.V.Sriman.N@007"
app.config["MYSQL_DB"] = "hostelmng"

mysql = MySQL(app)

# Defining the pages to support
pages = [
    "home",
    "resident",
    "login"
]

@app.route('/home', methods=['GET'])
def index_page():
    return render_template('home.html', pages=pages)

@app.route('/resident', methods=['GET'])
def ressident_page():
    return render_template('resident.html', pages=pages)

@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html', pages=pages)

# Running the app
if __name__ == '__main__':
    app.run(debug=True)