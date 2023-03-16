from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from utils import check_password

app = Flask(__name__)

# setting the admin id and password
admin_id = "00000001"
admin_password = 'password'

# setting the secret key
app.secret_key = 'DONT TELL ANYONE'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "M.V.Sriman.N@007"
app.config["MYSQL_DB"] = "hostelmng"

mysql = MySQL(app)

# Defining the pages to support
pages = {
    "home" : "/home"
}

admin_pages = {
    "logout": "/admin/logout",
}

resident_pages = {
    "logout": "/resident/logout",
}

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home_page():
    return render_template('home.html', pages=pages)
        
# Handlign the routes for the residents
@app.route('/resident/<page_name>', methods=['GET', 'POST'])
def resident_page(page_name = None):
    # error handling
    if page_name not in ['login', 'dashboard', 'logout']:
        return redirect('/resident/login')
    
    if (page_name == 'login'):
        if (request.method == 'GET'):
            return render_template('resident_login.html', pages = pages, error=None)
        else:
            id = request.form['ID'] 
            password = request.form['password']
            cur = mysql.connection.cursor()
            cur.execute("SELECT key_ FROM users WHERE id = %s;", (id,))
            actual_key = cur.fetchone()
            if actual_key == None:
                return render_template('resident_login.html', pages = pages, error="Invalid ID")
            elif (check_password(password, actual_key[0])):
                session['logged_in'] = True
                session['id'] = id
                session['name'] = 'resident'
                return redirect('/resident/dashboard')
            else:
                return render_template('resident_login.html', pages = pages, error="Invalid password")
    elif page_name == 'dashboard':
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'resident'):
            return render_template('resident_dashboard.html', pages = resident_pages)
        else:
            return redirect('/resident/login')
    elif (page_name == 'logout'):
        session.pop('logged_in', None)
        session.pop('id', None)
        session.pop('name', None)
        return redirect('/')
# Handling the routes for the admin
@app.route('/admin/<page_name>', methods=['GET', 'POST'])
def admin_page(page_name = None):
    # error handling
    if page_name not in ['login', 'dashboard', 'logout']:
        return redirect('/admin/login')
    
    if (page_name == 'login'):
        if (request.method == 'GET'):
            return render_template('admin_login.html', pages = pages, error=None)
        else:
            id = request.form['ID'] 
            password = request.form['password']
            if id == admin_id and password == admin_password:
                session['logged_in'] = True
                session['id'] = id
                session['name'] = 'admin'
                return redirect('/admin/dashboard')
            else:
                return render_template('admin_login.html', pages = pages, error="Invalid Username or Password")
    elif (page_name == 'dashboard'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            return render_template('admin_dashboard.html', pages = admin_pages)
        else:
            return redirect('/admin/login')
    elif (page_name == 'logout'):
        session.pop('logged_in', None)
        session.pop('id', None)
        session.pop('name', None)
        return redirect('/')
# Running the app
if __name__ == '__main__':
    app.run(debug=True)