from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from utils import check_password
from metadata import *
import datetime
import numpy as np
import operator
from dateutil.parser import parse
app = Flask(__name__)

# setting the admin id and password
admin_id = "00000001"
admin_password = 'password'

# setting the secret key
app.secret_key = 'DONT TELL ANYONE'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "admin"
app.config["MYSQL_PASSWORD"] = "Password@1234"
app.config["MYSQL_DB"] = "hostelmng"

mysql = MySQL(app)

# Defining the pages to support
pages = {
    "home" : "/home",
    "hostel" : "/home/hostel_details" ,
    "outlet"  : "/home/outlet_details",
    "caretaker" : "/home/caretaker_details"
}

admin_pages = {
    "logout": "/admin/logout",
    "dashboard": "/admin/dashboard",
    "residents": "/admin/residents",
    "rooms": "/admin/rooms",
    "academic period":"/admin/academic_period",
    "security": "/admin/security"
}

resident_pages = {
    "logout": "/resident/logout",
    "history": "/resident/history",
    "profile": "/resident/profile",
    'current allocation': "/resident/current_allocation",
}

@app.template_filter('strftime')
def _jinja2_filter_datetime(time_, fmt):
    time_ = parse(str(time_))
    native = time_.replace(tzinfo=None)
    format='%H:%M:%S'
    return native.strftime(fmt)

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home_page():
    cur = mysql.connection.cursor()
    return render_template('home.html', pages=pages)

@app.route('/home/hostel_details')
def hostel():

    cur = mysql.connection.cursor()
    cur.execute(""" (select bf3.*, ca.total_residents
                    from
                    (select hostel_name,sum(total_rooms) as total_rooms, sum(occupancy) as occupancy
                    from
                    (select bf.*,total_rooms*1 as occupancy
                    from 
                    (select hostel_name,room_type,count(*) as total_rooms
                    from ROOM
                    where (room_type = 'single')
                    group by hostel_name, room_type) as bf
                    union
                    select bf.*,total_rooms*2 as occupancy
                    from 
                    (select hostel_name,room_type,count(*) as total_rooms
                    from ROOM
                    where (room_type = 'double')
                    group by hostel_name, room_type) as bf
                    union
                    select bf.*,total_rooms*3 as occupancy
                    from 
                    (select hostel_name,room_type,count(*) as total_rooms
                    from ROOM
                    where (room_type = 'triple')
                    group by hostel_name, room_type) as bf) as bf2
                    group by hostel_name
                    order by hostel_name ) as  bf3
                    left join 
                    (select hostel_name, count(resident_id) as total_residents
                    from CURRENT_ALLOCATION
                    group by hostel_name) as ca
                    on ca.hostel_name = bf3.hostel_name);""")

    table = list(cur.fetchall())
    table.insert(0,['Hostel Name','Total Rooms','Occupancy','Total Residents'])
    return render_template("hostel_details.html",pages=pages, table = table)
    


@app.route('/home/outlet_details')
def outlet():
    cur = mysql.connection.cursor()
    cur.execute("""select outlet_name, open_time, close_time, hostel_name, concat(owner_first_name," ",owner_last_name) as owner_name 
                   from OUTLET;""")
    table5=list(cur.fetchall())
    cur.execute("""select phone_no, OUTLET_PHONE.outlet_name 
                   from OUTLET INNER JOIN OUTLET_PHONE on OUTLET_PHONE.outlet_name=OUTLET.outlet_name;""")
    table6=cur.fetchall()
    cur.execute("select outlet_name from OUTLET")
    table7 = cur.fetchall()

    dict2 = {}
    for i in table7:
        dict2[i[0]] = ""
    table5 = [list(i) for i in table5]
    for i in table6:
        dict2[i[1]] += str(i[0]) +" "
    for i in range(len(table5)):
         table5[i].append(dict2[table5[i][0]])
    table5.insert(0,['Name','Open time','Close time','Hostel Name','Owner Name','Outlet Phoneno']) 
    return render_template("outlet_details.html",pages=pages, table5 = table5)
    pass

@app.route('/home/caretaker_details')
def caretaker_details():

    cur = mysql.connection.cursor()
    cur.execute(""" select HOSTEL.caretaker_id, concat(first_name," ", last_name) as Name, office_no, email_id, hostel_name, contact
                    from CARETAKER INNER JOIN HOSTEL on HOSTEL.caretaker_id=CARETAKER.caretaker_id
                    order by HOSTEL.hostel_name;""")
    table1=list(cur.fetchall())

    cur.execute("select phone_no, CARETAKER.caretaker_id  from CARETAKER INNER JOIN CARETAKER_PHONE on CARETAKER_PHONE.caretaker_id=CARETAKER.caretaker_id order by caretaker_id;")
    table2 = cur.fetchall()
    cur.execute("select caretaker_id from CARETAKER")
    table3 = cur.fetchall()
    dict1 = {}
    for i in table3:
        dict1[i[0]] = ""
    table1 = [list(i) for i in table1]
    for i in table2:
        dict1[i[1]] += str(i[0]) +" "
    for i in range(len(table1)):
         table1[i].append(dict1[table1[i][0]])
    table1.insert(0,['ID','Name','Office Number','Email ID','Hostel Name','Hostel Contact','Caretaker Phoneno']) 
    return render_template('caretaker_details.html', pages=pages, table1  = table1)
@app.route('/admin/academic_period')
def academic_period_details():
    cur = mysql.connection.cursor()
    cur.execute(""" select semester, year
                    from ACADEMIC_PERIOD
                    order by year, semester;""")
    
    table10 = list(cur.fetchall())
    table10.insert(0,['Semester','Year'])
    return render_template("admin_academicperiod.html",pages=admin_pages, table10 = table10)
# Handlign the routes for the residents
@app.route('/resident/<page_name>', methods=['GET', 'POST'])
def resident_page(page_name = None):
    # error handling
    if page_name not in ['login','logout','history','profile','current_allocation']:
        return redirect('/resident/login')
    
    cur = mysql.connection.cursor()
    
    if (page_name == 'login'):
        if (request.method == 'GET'):
            return render_template('resident_login.html', pages = pages, error='')
        else:
            id = request.form['ID'] 
            password = request.form['password']
            cur.execute("SELECT key_ FROM users WHERE id = %s;", (id,))
            actual_key = cur.fetchone()
            if actual_key == None:
                return render_template('resident_login.html', pages = pages, error="Invalid ID")
            elif (check_password(password, actual_key[0])):
                session['logged_in'] = True
                session['id'] = id
                session['name'] = 'resident'
                return redirect('/resident/profile')
            else:
                return render_template('resident_login.html', pages = pages, error="Invalid password")
    elif page_name == 'profile':
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'resident'):
            cur.execute(""" SELECT * 
                            from RESIDENT
                            where resident_id = %s;""",(session['id'],))
            stats = cur.fetchall()[0] # resident details

            cur.execute(""" show columns 
                            from RESIDENT;""" )
            cols = cur.fetchall() # attribute names
            cols = np.array(cols)
            cols = cols[:,0]
            cols = list(cols)
            cols = list(map(operator.methodcaller("replace",'_'," "),cols))
            cols = list(map(str.capitalize,cols))



            cur.execute(""" select phone_no
                            from RESIDENT_PHONE
                            where resident_id = %s;""",(session['id'],))
            contacts = cur.fetchall() # phone numbers

            cur.execute("""select program, branch
                            from ENROLLED_IN 
                            where resident_id = %s; """,(session['id'],))
            
            p_and_b = cur.fetchall() # program and branch
            
            stats_dict = {}

            for i,col in enumerate(cols):
                stats_dict[col] = stats[i]

            
            return render_template('resident_profile.html', pages = resident_pages, stats = stats_dict, contacts = contacts, pb = p_and_b)
        else:
            return redirect('/resident/login')

    elif (page_name == 'history'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'resident'):
            cur.execute(""" select year, semester, hostel_name, room_no,entry_date,exit_date
                            from ALLOCATION
                            where resident_id = %s
                            union
                            select year, semester, hostel_name, room_no,entry_date,null
                            from CURRENT_ALLOCATION
                            where resident_id = %s
                            order by year desc,semester desc;""",(session['id'],session['id'],))

            history = cur.fetchall()
            cols = ['year','semester','hostel_name','room_no','entry_date','exit_date']
            cols = list(map(str.capitalize,cols))
            cols = list(map(operator.methodcaller('replace','_',' '),cols))
            
            return render_template('resident_history.html', pages = resident_pages, history = history,cols = cols)
        else:
            return redirect('/resident/login')

    elif (page_name == 'current_allocation'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'resident'):
             # your code goes here
            cur.execute(""" select rhc.*, ca.entry_date, payment_amount, payment_status, due_amount,due_status
                            from CURRENT_ALLOCATION as ca
                            INNER JOIN 
                            (select  r.room_no, r.room_type ,hc.* from ROOM as r INNER JOIN 
                            (select hostel_name,contact, h.caretaker_id, concat(first_name, " ",last_name) as caretaker_name, office_no, email_id
                            from HOSTEL as h INNER JOIN CARETAKER as c on h.caretaker_id = c.caretaker_id) as hc
                            on r.hostel_name = hc.hostel_name) as rhc
                            on (ca.hostel_name = rhc.hostel_name AND ca.room_no = rhc.room_no)
                            where resident_id=%s;""",(session['id'],))
            current_allocation=cur.fetchall()[0]

            # print(current_allocation)
             
            cols=['Room Number','Room Type', 'Hostel_name', 'Hostel Contact', 'Caretaker ID', 'Caretaker Name','Office Number','Email ID','Entry Date','Payment Amount','Payment status','Due Amount', 'Due Status']

            cur.execute(""" select rhc.phone_no
                            from CURRENT_ALLOCATION as ca
                            INNER JOIN 
                            (select  r.room_no, r.room_type ,hc.* from ROOM as r INNER JOIN 
                            (select hostel_name,contact, h.caretaker_id, concat(first_name, " ",last_name) as caretaker_name, phone_no, office_no, email_id
                            from HOSTEL as h 
                            INNER JOIN 
                            (select phone_no, CARETAKER.caretaker_id, first_name, middle_name, last_name, office_no, email_id from CARETAKER INNER JOIN CARETAKER_PHONE on CARETAKER.caretaker_id=CARETAKER_PHONE.caretaker_id) as c on h.caretaker_id = c.caretaker_id) as hc
                            on r.hostel_name = hc.hostel_name) as rhc
                            on (ca.hostel_name = rhc.hostel_name AND ca.room_no = rhc.room_no)
                            where resident_id=%s;""",(session['id'],))
            contacts=cur.fetchall()


            stats_dict = {}

            for i in range(len((cols))):
                stats_dict[cols[i]] = current_allocation[i]
            return render_template('resident_current_alloc.html',pages = resident_pages, contacts=contacts, stats=stats_dict)
        else:
            return redirect('/resident/login')

    elif (page_name == 'logout'):
        session.pop('logged_in', None)
        session.pop('id', None)
        session.pop('name', None)
        return redirect('/')
# Handling the routes for the admin pages
@app.route('/admin/<page_name>', methods=['GET', 'POST'])
def admin_page(page_name = None):
    cur = mysql.connection.cursor()

    # error handling
    if page_name not in ['login', 'dashboard', 'logout', 'residents', 'add_student', 'add_security','academic_period', 'security', "rooms"]:
        return redirect('/admin/login')    

    if (page_name == 'login'):
        if (request.method == 'GET'):
            return render_template('admin_login.html', pages = pages, error='')
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
    # Handling the rooms route
    elif page_name == 'rooms':
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            if (request.method == 'GET'):
                # Fethcing all the hostel names
                query_string = "select distinct hostel_name from HOSTEL;"
                cur.execute(query_string)
                hostel_names = cur.fetchall()
                
                # Fetching all the room types
                query_string = "select distinct room_type from ROOM;"
                cur.execute(query_string)
                hostel_room_types = cur.fetchall()
                
                # receiving the route parameters
                hostel_name = request.args.get('hostel_name')
                room_type = request.args.get('room_type')
                room_no = request.args.get('room_no')
                occupant_count = request.args.get('occupant_count')

                # Creating the query string
                query_string = ""
                # Processing the search query
                if hostel_name != None and hostel_name != "all":
                    query_string += f" hostel_name = '{hostel_name}' "
                if room_type != None and room_type != "all":
                    if query_string != "":
                        query_string += "and"
                    query_string += f" room_type = '{room_type}' "
                if room_no != None and room_no != "":
                    if query_string != "":
                        query_string += "and"
                    query_string += f" room_no = '{room_no}' "
                if occupant_count != None and occupant_count != "":
                    if query_string != "":
                        query_string += "and"
                    query_string += f" occupied = '{occupant_count}' "
                if query_string != "":
                    query_string = "where" + query_string
                
                # Fetching the rooms info
                query_string = f"select * from ROOM {query_string};"
                cur.execute(query_string)
                rooms_details = cur.fetchall()

                # sending the html page
                return render_template('admin_rooms.html', 
                                    pages = admin_pages, 
                                    hostel_names = hostel_names, 
                                    room_types = hostel_room_types,
                                    rooms_details = rooms_details,
                                    room_details_field_names = list(room_details_field_names.keys()),
                                    )

    elif (page_name == 'add_room'):
        if not ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            return "Invalid authentication"
        hostel_name = request.form['Hostel Name']
        room_type = request.form['Room Type']
        room_no = request.form['Room Number']

        query_string = "INSERT INTO ROOM (" + "hostel_name, room_type, room_no, occupied" + ") VALUES (" + f"'{hostel_name}', '{room_type}', '{room_no}', 0" + ");"
        cur.execute(query_string)
        mysql.connection.commit()
        return redirect(request.referrer)
    
    elif (page_name == 'add_student'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            
            # adding into resident
            query_string = ""
            table_order = ""
            for field in request.form:
                if field != "add" and field != "phone_no" and field != "program" and field != "branch":
                    if query_string != "":
                        query_string += ", "
                    if table_order != "":
                        table_order += ", "
                    query_string += f'"{request.form[field]}"'
                    table_order += resident_details_field_names[field]
            # executing the query and commiting the changes
            cur.execute("INSERT INTO RESIDENT (" + table_order + ") VALUES (" + query_string + ");")
            
            # adding into phone_number
            cur.execute("INSERT INTO RESIDENT_PHONE (" + "resident_id, phone_no" + ") VALUES (" + f"'{request.form['ID']}', '{request.form['phone_no']}'" + ");")
            
            # Adding branch details for student
            if (request.form['Resident Type'] == 'student'):
                cur.execute("INSERT INTO ENROLLED_IN (" + "resident_id, program, branch" + ") VALUES (" + f"'{request.form['ID']}', '{request.form['program']}', '{request.form['branch']}'" + ");")

            # Commiting changes
            mysql.connection.commit()
            # redirecting to the residents page
            return redirect('/admin/residents')
    elif (page_name == 'add_security'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            
            # adding into resident
            query_string = ""
            table_order = ""
            for field in request.form:
                if field != "add" and field != "phone_no":
                    if query_string != "":
                        query_string += ", "
                    if table_order != "":
                        table_order += ", "
                    query_string += f'"{request.form[field]}"'
                    table_order += security_details_field_names[field]
            # executing the query and commiting the changes
            cur.execute("INSERT INTO GUARD (" + table_order + ") VALUES (" + query_string + ");")
            
            # adding into phone_number
            cur.execute("INSERT INTO GUARD_PHONE (" + "security_id, phone_no" + ") VALUES (" + f"'{request.form['ID']}', '{request.form['phone_no']}'" + ");")
            
            # Commiting changes
            mysql.connection.commit()
            # redirecting to the residents page
            return redirect('/admin/security')
    
    elif (page_name == 'dashboard'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            cur.execute(""" SELECT hostel_name, occupied, room_type, COUNT(hostel_name)
                            FROM ROOM
                            where room_type = "triple" or room_type = "single" or room_type = "double"
                            GROUP BY occupied, room_type, hostel_name
                            ORDER BY hostel_name;""")
            stats = cur.fetchall()
            stats_dict = {}
            for i, j, k, l in stats:
                if j == room_types[k]:
                    continue
                if i not in stats_dict:
                    stats_dict[i] = [(j,k,l)]
                else:
                    stats_dict[i].append((j,k,l))
            return render_template('admin_dashboard.html', pages = admin_pages, stats = stats_dict)
        else:
            return redirect('/admin/login')
    elif (page_name=='academic_period'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            if (request.method == 'GET'):
                return render_template('admin_academicperiod.html', pages = admin_pages, error='')
            else:
                semester = request.form['semester'] 
                year = request.form['year']
                cur.execute("select count(*) from ACADEMIC_PERIOD where semester={} and year={};".format(semester, year))
                count=cur.fetchall()[0]
                if count[0]==0:
                    return render_template('admin_academicperiod.html', pages = admin_pages, error="")
                else:
                    return render_template('admin_academicperiod.html', pages = admin_pages, error="Academic period already exists")
        else:
            return redirect('/admin/login')
    elif (page_name == "residents"):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            if request.method == 'GET':
                
                # Getting the query parameters
                search_ID = request.args.get('search_ID')
                is_allocated = request.args.get('is_allocated')
                resident_type = request.args.get('resident_type')
                hostel = request.args.get('hostel')
                program = request.args.get('program')
                branch = request.args.get('branch')
                gender = request.args.get('gender')
                join_year = request.args.get('join_year')
                pending_fees = request.args.get('pending_fees')
                pending_dues = request.args.get('pending_dues')

                a = [search_ID, is_allocated, resident_type, hostel, program, branch, gender, join_year, pending_fees, pending_dues]

                # Generating the sql query string
                query_string = ""
                if (search_ID != None and search_ID != ""):
                    query_string += f" RESIDENT.resident_id = {search_ID} "
                if (is_allocated != None):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" room_no is NOT NULL "
                if (resident_type != None and resident_type != "all"):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" RESIDENT.resident_type = '{resident_type}' "
                if (hostel != None and hostel != "all"):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" hostel_name = '{hostel}' "
                if (program != None and program != "all"):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" program = '{program}' "
                if (branch != None and branch != "all"):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" branch = '{branch}' "
                if (gender != None and gender != "all"):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" gender = '{gender}' "
                if (join_year != None and join_year != "all"):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" RESIDENT.resident_id REGEXP '{join_year[2:]}......' "
                if (pending_fees != None):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" CURRENT_ALLOCATION.payment_status < CURRENT_ALLOCATION.payment_amount "
                if (pending_dues != None):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" CURRENT_ALLOCATION.due_status < CURRENT_ALLOCATION.due_amount "
                
                if (query_string != ""):
                    query_string = "where" + query_string
                
                resident_query = f"""   SELECT RESIDENT.resident_id, CONCAT(first_name, " ", last_name) as full_name
                                        FROM (RESIDENT LEFT JOIN ENROLLED_IN on RESIDENT.resident_id = ENROLLED_IN.resident_id) LEFT JOIN CURRENT_ALLOCATION on CURRENT_ALLOCATION.resident_id = RESIDENT.resident_id
                                        {query_string}  """
                # Getting all the data corresponding to the residents
                cur.execute(resident_query)
                residents = cur.fetchall()
                
                # Defining the field names for the fields of the form
                # field_names = ["ID", "Full Name", "Semester", "Year", "Room No", "Hostel Name", "Entry Date", "Payment Status", "Due Amount", "Due Status", "Payment Amount", "First Name", "Middle Name", "Last Name", "Gender", "Blood Group", "Email ID", "City", "Postal Code", "Home Contact", "Resident Type"]
                
                # Fetching all the availble hostel names
                cur.execute(""" SELECT hostel_name from
                                HOSTEL;""")
                hostel_names = cur.fetchall()
                

                # Getting all the Program types
                cur.execute(""" SELECT distinct program from
                                DEGREE;""")
                program_types = cur.fetchall()

                # Getting all the branch types
                cur.execute(""" SELECT distinct branch from
                                DEGREE;""")
                branch_types = cur.fetchall()

                # Rendering the template
                return render_template('admin_residents.html', 
                                    pages = admin_pages, 
                                    residents = residents, 
                                    hostel_names = hostel_names, 
                                    resident_types=resident_types, 
                                    gender_types = gender_types, 
                                    program_types = program_types,
                                    branch_types = branch_types,
                                    blood_types = blood_types,
                                    resident_details_field_names = list(resident_details_field_names.keys()))
            else:
                return "got the request"
        else:
            return redirect('/admin/login')
    elif (page_name == "security"):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            if request.method == 'GET':
                
                # Getting the query parameters
                search_ID = request.args.get('search_ID')
                hostel = request.args.get('hostel')

                a = [search_ID, hostel]

                # Generating the sql query string
                query_string = ""
                if (search_ID != None and search_ID != ""):
                    query_string += f" SECURITY.security_id = {search_ID} "
                if (hostel != None and hostel != "all"):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" hostel_name = '{hostel}' "
                
                if (query_string != ""):
                    query_string = "where" + query_string
                
                security_query = f"""   select distinct GUARD.security_id, concat(first_name," ",last_name) as full_name
                                        from GUARD LEFT JOIN SECURITY ON SECURITY.security_id = GUARD.security_id
                                        {query_string}  """
                # Getting all the data corresponding to the residents
                cur.execute(security_query)
                securities = cur.fetchall()

                # Fetching all the availble hostel names
                cur.execute(""" SELECT hostel_name from
                                HOSTEL;""")
                hostel_names = cur.fetchall()

                # Rendering the template
                return render_template('admin_securities.html', 
                                        pages = admin_pages, 
                                        securities = securities,
                                        security_details_field_names = list(security_details_field_names.keys()),
                                        hostel_names=hostel_names
                                        )
            else:
                return "got the request"
        else:
            return redirect('/admin/login')
        

    elif (page_name == 'logout'):
        session.pop('logged_in', None)
        session.pop('id', None)
        session.pop('name', None)
        return redirect('/')

# Handling the routes for the admin/rooms pages
@app.route('/admin/rooms/<hostel_name>/<room_no>', methods=['POST'])
def admin_rooms(hostel_name=None, room_no=None):
    # connecting to the database
    cur = mysql.connection.cursor()
    
    # Checking if the user is logged in
    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        # Getting the hostel_details
        query_string = f"SELECT * FROM ROOM WHERE hostel_name='{hostel_name}' AND room_no='{room_no}';"
        cur.execute(query_string)
        room_details = cur.fetchall()[0]

        # Fetching all the room types
        query_string = "select distinct room_type from ROOM;"
        cur.execute(query_string)
        hostel_room_types = cur.fetchall()
        
        # Fethcing all the hostel names
        query_string = "select distinct hostel_name from HOSTEL;"
        cur.execute(query_string)
        hostel_names = cur.fetchall()

        # Fetching all the available semester types
        cur.execute(""" SELECT distinct semester from
                        ACADEMIC_PERIOD;""")
        semester_types = cur.fetchall()

        # Fetching all the available years 
        cur.execute(""" SELECT distinct year from
                        ACADEMIC_PERIOD;""")
        years = cur.fetchall()

        # Fetching the previous allocation details
        query_string = f""" SELECT semester, year, resident_id, entry_date, exit_date, payment_status, due_amount, due_status, payment_amount FROM ALLOCATION WHERE hostel_name='{hostel_name}' AND room_no='{room_no}';"""
        cur.execute(query_string)
        room_allocation_history_details = cur.fetchall()
        
        # Fetching the current allocation details
        query_string = f""" SELECT semester, year, resident_id, entry_date, payment_status, due_amount, due_status, payment_amount
                            FROM CURRENT_ALLOCATION 
                            WHERE hostel_name='{hostel_name}' AND room_no='{room_no}';"""
        cur.execute(query_string)
        room_current_allocation_details = cur.fetchall()

        # Fetching the furniture details
        query_string = f""" SELECT furniture_id, status from FURNITURE WHERE hostel_name='{hostel_name}' AND room_no='{room_no}';"""
        cur.execute(query_string)
        room_furniture_details = cur.fetchall()


        return render_template( "admin_room_data.html",
                                room_types = hostel_room_types,
                                hostel_names = hostel_names,
                                room_details = room_details,
                                hostel_name = hostel_name,
                                room_no = room_no,
                                semester_types = semester_types,
                                years = years,
                                room_details_field_names = list(room_details_field_names.keys()),
                                room_current_allocation_details = room_current_allocation_details,
                                room_current_allocation_field_names = list(room_current_allocation_field_names.keys()),
                                room_allocation_history_details = room_allocation_history_details,
                                room_allocation_history_field_names = list(room_allocation_history_field_names.keys()),
                                room_furniture_details = room_furniture_details,
                               )

@app.route('/admin/furniture/<furniture_id>/<operation>', methods=['POST'])
def admin_furniture_operations(furniture_id=None, operation=None):
    cur = mysql.connection.cursor()
    # Handling the authentication
    if not ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        return "Invalid Authentication"
    # Handling invalid operations
    if operation not in ['remove_furniture_from_room']:
        return "Invalid Operation"
    if operation == 'remove_furniture_from_room':
        query_string = f"UPDATE FURNITURE SET room_no=NULL, hostel_name=NULL WHERE furniture_id='{furniture_id}';"
        cur.execute(query_string)
        cur.connection.commit()

        return redirect(request.referrer)
# Handling operations for the room data
@app.route('/admin/rooms/<hostel_name>/<room_no>/<operation>', methods=['POST'])
def admin_rooms_operations(hostel_name=None, room_no=None, operation=None):
    cur = mysql.connection.cursor()
    # Handling the authentication
    if not ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        return "Invalid Authentication"
    # Handling invalid operations
    if operation not in ['update_room_data', 'update_current_room_allocation', 'update_furniture_details', "add_furniture_to_room", "delete_room"]:
        return "Invalid Operation"
    if operation == 'update_room_data':
        # Getting the form data
        room_type = request.form['room_type']
        
        # Updating the room data
        query_string = f"UPDATE ROOM SET room_type='{room_type}' WHERE hostel_name='{hostel_name}' AND room_no='{room_no}';"
        cur.execute(query_string)
        mysql.connection.commit()
        return redirect('/admin/rooms')
    
    if operation == 'update_current_room_allocation':
        query_string = ""
        for field in request.form:
            if field != 'update':
                if query_string != "":
                    query_string += ", "
                query_string += f"{room_current_allocation_field_names[field]}='{request.form[field]}'"
        query_string = "UPDATE CURRENT_ALLOCATION SET " + query_string + f" WHERE hostel_name='{hostel_name}' AND room_no='{room_no}' AND resident_id='{request.form['ID']}';"
        cur.execute(query_string)
        mysql.connection.commit()
    if operation == 'update_furniture_details':
        status_value = (1 if (request.form.get("status")!="on") else 0)
        furniture_id = request.form["furniture_id"]
        query_string = f"UPDATE FURNITURE SET status='{status_value}' WHERE furniture_id='{furniture_id}';"
        cur.execute(query_string)
        mysql.connection.commit()

        return redirect('/admin/rooms')
    if operation == 'add_furniture_to_room':
        furniture_id = request.form["furniture_id"]
        query_string = f"UPDATE FURNITURE SET hostel_name='{hostel_name}', room_no='{room_no}' WHERE furniture_id='{furniture_id}';"
        cur.execute(query_string)
        mysql.connection.commit()   
        return redirect(request.referrer)
    
    if operation == 'delete_room':
        query_string = f"DELETE FROM ROOM WHERE hostel_name='{hostel_name}' AND room_no='{room_no}';"
        cur.execute(query_string)
        mysql.connection.commit()
        return redirect(request.referrer)


# Handling the post request for the admin/residents/<resident_id> page
@app.route('/admin/residents/<resident_id>', methods=['POST'])
def admin_resident_data(resident_id):
    cur = mysql.connection.cursor()
    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        
        # Fetching the resident details
        cur.execute(f"""select RESIDENT.resident_id, first_name, middle_name, last_name, gender, blood_group, email_id, city, postal_code, home_contact, resident_type
                        from (RESIDENT)
                        where RESIDENT.resident_id = {resident_id};""")
        resident_details = cur.fetchall()[0]

        # Fetching the current allocation details
        cur.execute(f"""select semester, year, hostel_name, room_no, entry_date, payment_status, due_amount, due_status, payment_amount
                        from CURRENT_ALLOCATION
                        where CURRENT_ALLOCATION.resident_id = {resident_id};""")
        resident_current_allocation_details = cur.fetchall()
        try:
            resident_current_allocation_details = resident_current_allocation_details[0]
        except:
            resident_current_allocation_details = []

        # Fetching the phone numbers
        cur.execute(f"""select phone_no
                        from RESIDENT_PHONE
                        where RESIDENT_PHONE.resident_id = {resident_id};""")
        resident_phone_details = cur.fetchall()

        # Fetching the program details
        cur.execute(f"""select program, branch
                        from ENROLLED_IN
                        where ENROLLED_IN.resident_id = {resident_id};""")
        resident_program_details = cur.fetchall()

        # Fetching the history data
        cur.execute(f"""select semester, year, hostel_name, room_no, entry_date, exit_date, payment_status, due_amount, due_status, payment_amount
                        from ALLOCATION
                        where resident_id = {resident_id};""")
        history_data = cur.fetchall()
        
        # Fetching all the availble hostel names
        cur.execute(""" SELECT hostel_name from
                        HOSTEL;""")
        hostel_names = cur.fetchall()
        
        # Getting the years from the acdemic period
        cur.execute(""" SELECT distinct year from
                        ACADEMIC_PERIOD;""")
        years = cur.fetchall()

        # Getting all the Program types
        cur.execute(""" SELECT distinct program from
                        DEGREE;""")
        program_types = cur.fetchall()

        # Getting all the branch types
        cur.execute(""" SELECT distinct branch from
                        DEGREE;""")
        branch_types = cur.fetchall()

        # Fetching all the available semester types
        cur.execute(""" SELECT distinct semester from
                        ACADEMIC_PERIOD;""")
        semester_types = cur.fetchall()

        return render_template('admin_resident_data.html', 
                                resident_details = resident_details, 
                                resident_details_field_names = list(resident_details_field_names.keys()), 
                                resident_current_allocation_details = resident_current_allocation_details,
                                resident_current_allocation_field_names = list(resident_current_allocation_field_names.keys()),
                                resident_program_details = resident_program_details,
                                resident_program_field_names = list(resident_program_field_names.keys()),
                                history_data = history_data, 
                                resident_history_field_names = list(resident_history_field_names.keys()),
                                resident_phone_details = resident_phone_details,
                                hostel_names = hostel_names, 
                                resident_types= resident_types, 
                                gender_types = gender_types, 
                                semester_types = semester_types, 
                                blood_types = blood_types, 
                                years = years,
                                program_types = program_types,
                                branch_types = branch_types,
                                today = datetime.date.today())
# Handling the post request for the admin/security/<security_id> page
@app.route('/admin/security/<security_id>', methods=['POST'])
def admin_security_data(security_id):
    cur = mysql.connection.cursor()
    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        
        # Fetching the resident details
        cur.execute(f"""select GUARD.security_id, first_name, middle_name, last_name
                        from (GUARD)
                        where GUARD.security_id = {security_id};""")
        security_details = cur.fetchall()[0]

        # Fetching the current allocation details
        cur.execute(f"""select hostel_name, start_time, end_time
                        from SECURITY
                        where SECURITY.security_id = {security_id};""")
        security_current_allocation_details = cur.fetchall()
        # try:
        #     resident_current_allocation_details = resident_current_allocation_details[0]
        # except:
        #     resident_current_allocation_details = []

        # Fetching the phone numbers
        cur.execute(f"""select phone_no
                        from GUARD_PHONE
                        where GUARD_PHONE.security_id = {security_id};""")
        security_phone_details = cur.fetchall()
        
        # Fetching all the availble hostel names
        cur.execute(""" SELECT hostel_name from
                        HOSTEL;""")
        hostel_names = cur.fetchall()

        return render_template('admin_security_data.html', 
                                security_details = security_details, 
                                security_details_field_names = list(security_details_field_names.keys()), 
                                security_current_allocation_details = security_current_allocation_details,
                                security_current_allocation_field_names = list(security_current_allocation_field_names.keys()),
                                security_phone_details = security_phone_details,
                                hostel_names = hostel_names, 
                                today = datetime.date.today())  


@app.route('/admin/residents/<resident_id>/<operation>', methods=['POST'])
def resident_operations(resident_id, operation):
    
    # Error handling
    if (operation not in ['update_details', 'update_current_allocation', 'deallocate_resident', 'delete_phone', "add_phone", 'update_program']):
        return redirect('/admin/residents')
    
    # Connecting to the database
    cur = mysql.connection.cursor()

    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        if (operation == 'update_details'):
            # Generating the query string
            query_string = ""
            for field in request.form.keys():
                if (field != "update"):
                    if (query_string != ""):
                        query_string += ", "
                    query_string += f"{resident_details_field_names[field]} = '{request.form[field]}'"
            # Adding the select and where clause
            query_string = f"UPDATE RESIDENT SET {query_string} WHERE resident_id = {resident_id};"
            
            # Executing the query and commiting the changes
            cur.execute(query_string)
            mysql.connection.commit()

            # Redirecting to the resident page
            return redirect(f'/admin/residents')
        
        elif (operation == 'delete_phone'):
            query_string = f"DELETE FROM RESIDENT_PHONE WHERE resident_id = {resident_id} AND phone_no = '{request.form['phone_no']}';"
            # Executing the query and commiting the changes
            cur.execute(query_string)
            mysql.connection.commit()

            # Redirecting to the resident page
            return redirect(f'/admin/residents')
        
        elif (operation == 'update_program'):
            query_string = f"UPDATE ENROLLED_IN SET program='{request.form['program']}', branch = '{request.form['branch']}' where resident_id = {resident_id};"
            # Executing the query and commiting the changes
            cur.execute(query_string)
            mysql.connection.commit()

            # Redirecting to the resident page
            return redirect(f'/admin/residents')
        
        elif operation == 'add_phone':
            query_string = f"INSERT INTO RESIDENT_PHONE(resident_id, phone_no) VALUES ({resident_id}, '{request.form['phone_no']}');"
            # Executing the query and commiting the changes
            cur.execute(query_string)
            mysql.connection.commit()

            # Redirecting to the resident page
            return redirect(f'/admin/residents')

        elif (operation == 'update_current_allocation'):
            # Generating the query string
            query_string = ""
            for field in request.form.keys():
                if (field != "update"):
                    if (query_string != ""):
                        query_string += ", "
                    query_string += f"{resident_current_allocation_field_names[field]} = '{request.form[field]}'"
            
            # Adding the update and where clause
            query_string = f"UPDATE CURRENT_ALLOCATION SET {query_string} WHERE resident_id = {resident_id};"
            
            # Executing the query and commiting the changes
            cur.execute(query_string)
            mysql.connection.commit()

            # Redirecting to the resident page
            return redirect(f'/admin/residents')
        
        elif (operation == 'deallocate_resident'):
            cur.execute(f"""
                            CALL DEALLOCATE({resident_id}, STR_TO_DATE('{request.form['exit_date']}', '%Y-%m-%d'));
                        """)
            mysql.connection.commit()
            return redirect('/admin/residents')
 
@app.route('/admin/security/<security_id>/<operation>', methods=['POST'])
def security_operations(security_id, operation):
    
    # Error handling
    if (operation not in ['update_details', 'add_allocation', 'delete_phone', "add_phone","delete_current_allocation"]):
        return redirect('/admin/security')
    
    # Connecting to the database
    cur = mysql.connection.cursor()

    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        if (operation == 'update_details'):
            # Generating the query string
            query_string = ""
            for field in request.form.keys():
                if (field != "update"):
                    if (query_string != ""):
                        query_string += ", "
                    query_string += f"{security_details_field_names[field]} = '{request.form[field]}'"
            # Adding the select and where clause
            query_string = f"UPDATE GUARD SET {query_string} WHERE security_id = {security_id};"
            
            # Executing the query and commiting the changes
            cur.execute(query_string)
            mysql.connection.commit()

            # Redirecting to the resident page
            return redirect(f'/admin/security')
        
        elif (operation == 'delete_phone'):
            query_string = f"DELETE FROM GUARD_PHONE WHERE security_id = {security_id} AND phone_no = '{request.form['phone_no']}';"
            # Executing the query and commiting the changes
            cur.execute(query_string)
            mysql.connection.commit()

            # Redirecting to the resident page
            return redirect(f'/admin/security')
        
        elif operation=='delete_current_allocation':
            query_string = f"DELETE FROM SECURITY WHERE security_id = {security_id} AND hostel_name = '{request.form['hostel_name']}';"
            # Executing the query and commiting the changes
            cur.execute(query_string)
            mysql.connection.commit()

            # Redirecting to the resident page
            return redirect(f'/admin/security')
        
        elif operation == 'add_phone':
            query_string = f"INSERT INTO GUARD_PHONE(security_id, phone_no) VALUES ({security_id}, '{request.form['phone_no']}');"
            # Executing the query and commiting the changes
            cur.execute(query_string)
            mysql.connection.commit()

            # Redirecting to the resident page
            return redirect(f'/admin/security')

        elif (operation == 'add_allocation'):
            # # Generating the query string
            # query_string = ""
            # for field in request.form.keys():
            #     if (field != "update"):
            #         if (query_string != ""):
            #             query_string += ", "
            #         query_string += f"{security_current_allocation_field_names[field]} = '{request.form[field]}'"
            
            # Adding the update and where clause
            query_string= f"INSERT INTO SECURITY(security_id, hostel_name, start_time, end_time) VALUES({security_id},'{request.form['hostel_name']}','{request.form['start_time']}','{request.form['end_time']}');"
            # Executing the query and commiting the changes
            cur.execute(query_string)
            mysql.connection.commit()

            # Redirecting to the resident page
            return redirect(f'/admin/security')
        


@app.route('/admin/academic_period/<operation>', methods=['POST'])
def academic_period_operations(operation):
    # Error handling
    if (operation not in ['add_academic_period']):
        return redirect('/admin/academic_period')
    # Connecting to the database
    cur = mysql.connection.cursor()
    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        if operation == 'add_academic_period':
            semester = request.form['semester'] 
            year = request.form['year']
            cur.execute("select count(*) from ACADEMIC_PERIOD where semester={} and year={};".format(semester, year))
            count=cur.fetchall()[0]
            if count[0]==0:
                query_string = f"INSERT INTO ACADEMIC_PERIOD(semester, year) VALUES ('{request.form['semester']}', '{request.form['year']}');"
                # Executing the query and commiting the changes
                cur.execute(query_string)
                mysql.connection.commit()

                # Redirecting to the resident page
                return redirect(f'/admin/academic_period')
            else:
                return redirect(f'/admin/dashboard')
# Running the app
if __name__ == '__main__':
    app.run(debug=True)
