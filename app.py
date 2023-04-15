from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from utils import check_password, generate_key
from metadata import *
import datetime
import numpy as np
import operator
from dateutil.parser import parse
import pandas as pd
import time

app = Flask(__name__)


# setting the secret key
app.secret_key = 'DONT TELL ANYONE'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "admin"
app.config["MYSQL_PASSWORD"] = "Password@1234"
app.config["MYSQL_DB"] = "hostelmng"
app.config['SESSION_COOKIE_HTTPONLY'] = True

mysql = MySQL(app)

# Defining the pages to support
pages = {
    "Home" : "/home",
    "Hostel" : "/home/hostel_details" ,
    "Caretaker" : "/home/caretaker_details",
    "Outlet"  : "/home/outlet_details",
}

admin_pages = {
    "Dashboard": "/admin/dashboard",
    "Residents": "/admin/residents",
    "Rooms": "/admin/rooms",
    "Security": "/admin/security",
    "Housekeeping": "/admin/housekeeping",
    "Furniture": "/admin/furniture",
    "Hostel":"/admin/hostel",
    'Caretakers': "/admin/caretakers",
    "Academic period":"/admin/academic_period",
    "Outlets": "/admin/outlets",
    "Logout": "/admin/logout",
}

resident_pages = {
    "Profile": "/resident/profile",
    'Current allocation': "/resident/current_allocation",
    "History": "/resident/history",
    "Logout": "/resident/logout",
}

# To prevent dictionary attacks or bruteforce attacks
resident_login_attempts = {}

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
        if len(dict2[i[1]]) == 0 :
              dict2[i[1]] += str(i[0]) 
        else:
            dict2[i[1]] += ", " +str(i[0]) 
             
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
    cur.execute("select caretaker_id from CARETAKER;")
    table3 = cur.fetchall()
    dict1 = {}
    for i in table3:
        dict1[i[0]] = ""
    table1 = [list(i) for i in table1]
    for i in table2:
        if len(dict1[i[1]]) == 0 :
              dict1[i[1]] += str(i[0]) 
        else:
            dict1[i[1]] += ", " +str(i[0]) 
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
            
            if (request.method == 'GET'):
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
            else :
                current_password = request.form['current_password']
                new_password = request.form['new_password']
                confirm_password = request.form['confirm_password']
                cur.execute(f"SELECT key_ FROM users WHERE id = {session['id']};")

                actual_key = cur.fetchone()
                if (check_password(current_password, actual_key[0]) == False):
                    return {"success": False, "reload": False, "message": "Incorrect password"}
                if (new_password != confirm_password):
                    return {"success": False, "reload": False, "message": "Passwords do not match"}

                new_key = generate_key(new_password)
                cur.execute(f"UPDATE users SET key_ = '{new_key}' WHERE id = {session['id']};")
                mysql.connection.commit()
                return {"success": True, "reload": True, "message": "Password Changed Successfully"}
                
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
            cur.execute(f""" select rhc.*, ca.entry_date, payment_amount, payment_status, due_amount,due_status
                            from CURRENT_ALLOCATION as ca
                            INNER JOIN 
                            (select  r.room_no, r.room_type ,hc.* from ROOM as r INNER JOIN 
                            (select hostel_name,contact, h.caretaker_id, concat(first_name, " ",last_name) as caretaker_name, office_no, email_id
                            from HOSTEL as h INNER JOIN CARETAKER as c on h.caretaker_id = c.caretaker_id) as hc
                            on r.hostel_name = hc.hostel_name) as rhc
                            on (ca.hostel_name = rhc.hostel_name AND ca.room_no = rhc.room_no)
                            where resident_id='{session['id']}';""")
            try:
                current_allocation=cur.fetchall()[0]
            except:
                current_allocation = []


            # print(current_allocation)
             
            cols=['Room Number','Room Type', 'Hostel_name', 'Hostel Contact', 'Caretaker ID', 'Caretaker Name','Office Number','Email ID','Entry Date','Payment Amount','Payment status','Due Amount', 'Due Status']

            cur.execute(f""" select rhc.phone_no
                            from CURRENT_ALLOCATION as ca
                            INNER JOIN 
                            (select  r.room_no, r.room_type ,hc.* from ROOM as r INNER JOIN 
                            (select hostel_name,contact, h.caretaker_id, concat(first_name, " ",last_name) as caretaker_name, phone_no, office_no, email_id
                            from HOSTEL as h 
                            INNER JOIN 
                            (select phone_no, CARETAKER.caretaker_id, first_name, middle_name, last_name, office_no, email_id from CARETAKER INNER JOIN CARETAKER_PHONE on CARETAKER.caretaker_id=CARETAKER_PHONE.caretaker_id) as c on h.caretaker_id = c.caretaker_id) as hc
                            on r.hostel_name = hc.hostel_name) as rhc
                            on (ca.hostel_name = rhc.hostel_name AND ca.room_no = rhc.room_no)
                            where resident_id='{session['id']}';""")
            contacts=cur.fetchall()


            stats_dict = {}
            if (len(current_allocation) > 0):
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
    print(page_name)
    # error handling
    if page_name not in ['login', 'dashboard', 'logout', 'residents', 'deallocate_all_students','add_student_csv', 'add_allocation_csv','add_student', 'add_security','add_housekeeping','academic_period', 'security', "housekeeping", "rooms", "add_room", "outlets", "caretakers", "furniture", "add_furniture","hostel","add_hostel"]:
        return redirect('/admin/login')    

    elif(page_name ==  'add_student_csv'):
        app.logger.info(request)
        csv_file = request.files['file']
        df = pd.read_csv(csv_file)
        # Iterate over the rows of the DataFrame and insert them into the MySQL table
        try:
            for i   in range(len(df)):
                cur  = mysql.connection.cursor();
                query = "INSERT INTO RESIDENT "  +" VALUES " +  str(tuple(df.iloc[i].tolist()))
                cur.execute(query)
                mysql.connection.commit()
            return {"success": True, "reload": True, "message": "Students added successfully"}
        except Exception as e:
            return {"success": False, "reload": False, "message": str(e.args[1])}
        
    elif(page_name == "add_allocation_csv"):
            
        app.logger.info(request)
        csv_file = request.files['file']
        df = pd.read_csv(csv_file)
        # Iterate over the rows of the DataFrame and insert them into the MySQL table
        try:
            for i  in range(len(df)):
                cur  = mysql.connection.cursor();
                query = "INSERT INTO CURRENT_ALLOCATION "  +" VALUES " +  str(tuple(df.iloc[i].tolist()))
                cur.execute(query)
                mysql.connection.commit()
            return {"success": True, "reload": True, "message": "Allocated successfully"}
        except Exception as e:
            return {"success": False, "reload": False, "message": str(e.args[1])}
        
    elif (page_name == 'deallocate_all_students'):
        try:
            cur  = mysql.connection.cursor();
            query = " DELETE FROM CURRENT_ALLOCATION"
            cur.execute(query)
            mysql.connection.commit()
            return {"success": True, "reload": True, "message": "Deallocated successfully"}
        except Exception as e:
            return {"success": False, "reload": False, "message": str(e.args[1])}
        
    if (page_name == 'login'):
        if (request.method == 'GET'):
            return render_template('admin_login.html', pages = pages, error='')
        else:
            id = request.form['ID'] 
            password = request.form['password']
            import time
            # Preventing multiple logins(after 3 attempts) for 10 mins
            if (id in resident_login_attempts):
                if (resident_login_attempts[id][0] >= 3):
                    if (time.time() - resident_login_attempts[id][1] < 600):
                        return render_template('admin_login.html', pages = pages, error='Too many attempts. Try again after 10 minutes')
                    else:
                        resident_login_attempts[id] = [0, time.time()]
                else:
                    resident_login_attempts[id][1] = time.time()
                    resident_login_attempts[id][0] += 1

            else:
                resident_login_attempts[id] = [0, time.time()]
            if resident_login_attempts[id][0] < 3:
                query = f"SELECT key_ FROM admins WHERE id = '{id}' AND key_ = '{password}' ;"
                print('query',query)
                cur.execute(f"SELECT key_ FROM admins WHERE id = '{id}' AND key_ = '{password}' ;")
                app.logger.info(query)
                actual_key = cur.fetchone()
                print(actual_key)
                if actual_key == None:
                    return redirect('/admin/login')
                else :
                    session['logged_in'] = True
                    session['id'] = id
                    session['name'] = 'admin'
                    return redirect('/admin/dashboard')
            else:
                return redirect('/admin/login')
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
        try:
            cur.execute(query_string)
            mysql.connection.commit()
            return {"success": True, "reload": True, "message": "Room added successfully"}
        except Exception as e:
            return {"success": False, "reload": False, "message": e.args[1]}
    
    elif (page_name == 'add_student'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            
            # adding into resident
            query_string = ""
            table_order = ""
            for field in request.form:
                if field != "add" and field != "phone_no" and field != "program" and field != "branch" and request.form[field]!='':
                    if query_string != "":
                        query_string += ", "
                    if table_order != "":
                        table_order += ", "
                    query_string += f'"{request.form[field]}"'
                    table_order += resident_details_field_names[field]
            try:
                # executing the query and commiting the changes
                cur.execute("INSERT INTO RESIDENT (" + table_order + ") VALUES (" + query_string + ");")
                
                # adding into phone_number
                cur.execute("INSERT INTO RESIDENT_PHONE (" + "resident_id, phone_no" + ") VALUES (" + f"'{request.form['ID']}', '{request.form['phone_no']}'" + ");")
                
                # Adding branch details for student
                if (request.form['Resident Type'] == 'student'):
                    cur.execute("INSERT INTO ENROLLED_IN (" + "resident_id, program, branch" + ") VALUES (" + f"'{request.form['ID']}', '{request.form['program']}', '{request.form['branch']}'" + ");")

                # Commiting changes
                mysql.connection.commit()
                # Sending the response
                return {"success": True, "reload": True, "message": "Student added successfully"}
            
            except Exception as e:
                app.logger.info(type(e))
                return {"success": False, "reload": False, "message": str(e.args[1])}
        
    elif (page_name == 'add_furniture'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            
            # adding into resident
            query_string = ""
            table_order = ""
            for field in request.form:
                if field != "add" and request.form[field]!='':
                    if query_string != "":
                        query_string += ", "
                    if table_order != "":
                        table_order += ", "
                    query_string += f'"{request.form[field]}"'
                    table_order += furniture_details_field_names[field]
            try:
                # executing the query and commiting the changes
                cur.execute("INSERT INTO FURNITURE (" + table_order + ") VALUES (" + query_string + ");")
                
                # Commiting changes
                mysql.connection.commit()
                return {"success": True, "reload": True, "message": "Furniture added successfully"}
            except Exception as e:
                return {"success": False, "reload": False, "message": str(e.args[1])}
        
    elif (page_name == 'add_security'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            
            # adding into resident
            query_string = ""
            table_order = ""
            for field in request.form:
                if field != "add" and field != "phone_no" and request.form[field]!='':
                    if query_string != "":
                        query_string += ", "
                    if table_order != "":
                        table_order += ", "
                    query_string += f'"{request.form[field]}"'
                    table_order += security_details_field_names[field]
            try:
                # executing the query and commiting the changes
                cur.execute("INSERT INTO GUARD (" + table_order + ") VALUES (" + query_string + ");")
                
                # adding into phone_number
                cur.execute("INSERT INTO GUARD_PHONE (" + "security_id, phone_no" + ") VALUES (" + f"'{request.form['ID']}', '{request.form['phone_no']}'" + ");")
                
                # Commiting changes
                mysql.connection.commit()
                return {"success": True, "reload": True, "message": "Security added successfully"}
            except Exception as e:
                return {"success": False, "reload": False, "message": str(e.args[1])}
            
    elif (page_name == 'add_housekeeping'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            
            # adding into housekeeping
            query_string = ""
            table_order = ""
            for field in request.form:
                if field != "add" and field != "phone_no" and request.form[field]!='':
                    if query_string != "":
                        query_string += ", "
                    if table_order != "":
                        table_order += ", "
                    query_string += f'"{request.form[field]}"'
                    table_order += housekeeping_details_field_names[field]
            try:
                # executing the query and commiting the changes
                cur.execute("INSERT INTO HOUSE_KEEPING (" + table_order + ") VALUES (" + query_string + ");")
                
                # adding into phone_number
                cur.execute("INSERT INTO HOUSE_KEEPING_PHONE (" + "housekeeper_id, phone_no" + ") VALUES (" + f"'{request.form['ID']}', '{request.form['phone_no']}'" + ");")
                
                # Commiting changes
                mysql.connection.commit()
                return {"success": True, "reload": True, "message": "House Keeper added successfully"}
            except Exception as e:
                return {"success": False, "reload": False, "message": str(e.args[1])}
    
    elif (page_name == 'add_hostel'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            
            # adding into resident
            query_string = ""
            table_order = ""
            for field in request.form:
                if field != "add" and request.form[field]!='':
                    if query_string != "":
                        query_string += ", "
                    if table_order != "":
                        table_order += ", "
                    query_string += f'"{request.form[field]}"'
                    table_order += hostel_details_field_names[field]
            try:
                # executing the query and commiting the changes
                cur.execute("INSERT INTO HOSTEL (" + table_order + ") VALUES (" + query_string + ");")
                
                # Commiting changes
                mysql.connection.commit()
                return {"success": True, "reload": True, "message": "Hostel added successfully"}
            except Exception as e:
                return {"success": False, "reload": False, "message": str(e.args[1])}
        

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

    elif (page_name == 'caretakers'):
        print(page_name)
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            
            if request.method == 'GET': 
                # getting the query parameters

                caretaker_query = f"""  select caretaker_id,concat(first_name,' ',last_name) as name, gender, 
                                        office_no, email_id
                                        from CARETAKER
                                        ;"""
                cur.execute(caretaker_query)
                caretaker_details = cur.fetchall()

                caretaker_dict = {}
                for row in caretaker_details:
                    caretaker_dict[row[0]] = list(row)
                    caretaker_dict[row[0]].append([])
                    caretaker_dict[row[0]].append([])

                
                cur.execute(f"""select hostel_name, caretaker_id
                                from HOSTEL;
                                """)

                hostel_details = list(cur.fetchall())

                print(hostel_details)

                for row in hostel_details:
                    if (row[1] != None):
                        caretaker_dict[row[1]][-1].append(row[0])
                

                cur.execute(f""" select *
                                from CARETAKER_PHONE    
                                 """)

                phone_details = list(cur.fetchall())

                for row in phone_details:
                    if (len(caretaker_dict[row[1]][-2]) <2):
                        caretaker_dict[row[1]][-2].append(str(row[0]))

                for k,v in caretaker_dict.items():
                    v[-1]= ','.join(v[-1])
                    v[-2] = ','.join(v[-2])

                # Fetching all the availble hostel names
                cur.execute(""" SELECT hostel_name from
                                HOSTEL;""")
                hostel_names = cur.fetchall()

                field_names = ["Caretaker ID",'Name',"Gender","Office Number","Email ID","Contact", "Hostel"]
                
                return render_template('admin_caretaker.html',
                                        pages=admin_pages,
                                        field_names = field_names,
                                        c_dict = caretaker_dict,
                                        hostel_names = hostel_names)
            else:
                
                if (request.form.get('button') == 'add'):

                    caretaker_id = request.form.get('caretaker_id')
                    first_name = request.form.get('first_name')
                    middle_name = request.form.get('middle_name')
                    last_name = request.form.get('last_name')
                    gender = request.form.get('gender')
                    office_no = request.form.get('office_no')
                    email_id = request.form.get('email_id')
                    phone_no = request.form.get('phone_no_1')
                    phone_no_ = request.form.get('phone_no_2')
                    hostel = request.form.get('hostel')

                    cur  = mysql.connection.cursor();
                    cur.execute(f"select count(*) from CARETAKER where caretaker_id = {caretaker_id}")
                    no = cur.fetchall()



                    if no[0][0] == 0 :
                        try:
                            cur.execute(f"INSERT INTO CARETAKER (caretaker_id, first_name, middle_name, last_name, gender, office_no, email_id) VALUES ( '{caretaker_id}','{first_name}','{middle_name}', '{last_name}', '{gender}', '{office_no}', '{email_id}');")
                            
                            cur.execute(f""" INSERT into CARETAKER_PHONE 
                                        VALUES ('{phone_no}','{caretaker_id}')
                                    """)
                            if (phone_no_ is not None and len(phone_no_) == 10):
                                cur.execute(f""" INSERT into CARETAKER_PHONE 
                                            VALUES ('{phone_no_}','{caretaker_id}')
                                        """)
                            
                            cur.execute(f''' UPDATE HOSTEL SET caretaker_id = '{caretaker_id}' where hostel_name = '{hostel}' ''') 
                            mysql.connection.commit()
                            return {"success": True, "reload": True, "message": "Caretaker added successfully"}
                        except Exception as e:
                            return {"success": False, "reload":False, "message": e.args[1]}

                    else:
                        try:
                            cur.execute(f'''UPDATE CARETAKER SET caretaker_id = '{caretaker_id}', first_name ='{first_name}' ,
                                            middle_name = '{middle_name}', last_name ='{last_name}' , gender = '{gender}', office_no = '{office_no}' ,
                                            email_id ='{email_id}' where caretaker_id = '{caretaker_id}' ''')
                            cur.execute(f""" delete from CARETAKER_PHONE
                                                where caretaker_id = '{caretaker_id}';
                                        """)
                            cur.execute(f""" INSERT into CARETAKER_PHONE 
                                            VALUES ('{phone_no}','{caretaker_id}')
                                        """)
                            if (phone_no_ is not None and len(phone_no_) == 10):
                                cur.execute(f""" INSERT into CARETAKER_PHONE 
                                            VALUES ('{phone_no_}','{caretaker_id}')
                                        """)

                            cur.execute(f''' UPDATE HOSTEL SET caretaker_id = '{caretaker_id}' where hostel_name = '{hostel}' ''') 
                            mysql.connection.commit()
                            return {"success":True, "reload": True, "message":"Caretaker updated successfully"}
                        except Exception as e:
                            return {"success":False, "reload": False, "message":str(e.args[1])}
                    

                elif (request.form.get('button') == 'delete'):
                    try:
                        cur.execute(f""" DELETE FROM  CARETAKER 
                                        where caretaker_id = '{request.form.get('caretaker_id')}'
                                        """)
                        mysql.connection.commit()
                        return {"success":True, "reload": True, "message":"Caretaker deleted successfully"}
                    except Exception as e:
                        return {"success":False, "reload": False, "message":str(e.args[1])}
                
                else:
                    return redirect('/admin/caretakers')
            
        else:
            return redirect('/admin/login')

    elif (page_name == 'outlets'):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            
            if request.method == 'GET': 
                # getting the query parameters
                outlet_name = request.args.get('outlet_name')
                hostel_name = request.args.get('hostel_name')
                time = request.args.get('time')

                a = [outlet_name,hostel_name,time]
                
                outlet_query = ''

                if (outlet_name != '' and outlet_name != None):
                    outlet_query = f' outlet_name like "%{outlet_name}%" '
                if (hostel_name != None and hostel_name != 'all'):
                    if (outlet_query != ''):
                        outlet_query += 'and'
                    outlet_query += f' hostel_name = "{hostel_name}" '
                if (time != '' and time != None):
                    if (outlet_query != ''):
                        outlet_query += 'and'
                    outlet_query += f""" if (open_time < close_time, 
                                        time('{time}') between open_time and close_time, 
                                        time('{time}') = close_time or time('{time}') = open_time or time('{time}') not between close_time and open_time ) """
                if (outlet_query != '') :
                    outlet_query = ' where ' + outlet_query




                outlet_query = f""" select outlet_name,
                                    hostel_name, open_time, close_time, 
                                    contact, concat(owner_first_name,' ',owner_last_name) 
                                    as owner_name
                                    from OUTLET{outlet_query};"""
                cur.execute(outlet_query)

                outlets = cur.fetchall()


                # Fetching all the availble hostel names
                cur.execute(""" SELECT hostel_name from
                                HOSTEL;""")
                hostel_names = cur.fetchall()

                field_names = ['Outlet',"Hostel Name","Open Time","Close Time","Contact","Owner Name"]
                
                return render_template('admin_outlet.html',
                                        pages=admin_pages,
                                        outlets = outlets,
                                        field_names = field_names,
                                        hostel_names = hostel_names)
            else:
                
                print(request.form)
                if (request.form.get('button') == 'add'):
                    print("innermost")
                    app.logger.info("added")
                    outlet_name = request.form['outlet_name']
                    open_time = request.form['open_time']
                    close_time = request.form['close_time']
                    contact = request.form['contact']
                    owner_first_name = request.form['owner_first_name']
                    owner_middle_name = request.form['owner_middle_name']
                    owner_last_name = request.form['owner_last_name']
                    hostel_name = request.form['hostel_name']
                    phone_no = request.form['phone_no']
                    print(f"select count(*) from OUTLET where outlet_name = '{outlet_name}';")
                    cur.execute(f"select count(*) from OUTLET where outlet_name = '{outlet_name}';")
                    no  = cur.fetchall()
                    if no[0][0] == 0 : 
                        try:
                            cur.execute(f'''INSERT INTO  OUTLET (outlet_name,open_time, close_time, contact, owner_first_name, owner_middle_name, owner_last_name,hostel_name)
                                            VALUES ('{outlet_name}','{open_time}', '{close_time}', '{contact}', '{owner_first_name}', '{owner_middle_name}', '{owner_last_name}','{hostel_name}');
                                        ''')
                            cur.execute(f""" INSERT into OUTLET_PHONE 
                                            VALUES ('{contact}','{outlet_name}')
                                        """)
                            cur.execute(f""" INSERT into OUTLET_OWNER_PHONE 
                                            VALUES ('{phone_no}','{outlet_name}')
                                        """)
                            mysql.connection.commit()
                            return {"success":True, "reload":True, "message":"Outlet Added Successfully"}
                        except Exception as e:
                            return {"success":False, "reload": False, "message":e.args[1]}
                    else:
                        try:
                            cur.execute(f'''UPDATE  OUTLET  SET outlet_name  = '{outlet_name}' ,open_time = '{open_time}', close_time = '{close_time}',
                                            contact = {contact}, owner_first_name = '{owner_first_name}', owner_middle_name = '{owner_middle_name}',
                                            owner_last_name = '{owner_last_name}',hostel_name = '{hostel_name}' where outlet_name ='{outlet_name}';''')
                            cur.execute(f""" UPDATE OUTLET_PHONE SET   
                                                phone_no = '{contact}', outlet_name = '{outlet_name}'
                                                where outlet_name = '{outlet_name}';
                                        """)
                            cur.execute(f""" UPDATE OUTLET_OWNER_PHONE SET   
                                                phone_no = '{phone_no}', outlet_name = '{outlet_name}'
                                                where outlet_name = '{outlet_name}';
                                        """)
                            mysql.connection.commit()
                            return {"success":True, "reload":True, "message":"Updated Successfully"}
                        except Exception as e:
                            return {"success":False, "reload":False, "message":str(e.args[0])}
                    
                    return redirect('/admin/outlets')
                elif (request.form.get('button') == 'delete'):
                    try:
                        cur.execute(f""" DELETE FROM  OUTLET 
                                        where outlet_name = '{request.form.get('outlet_name')}'
                                        """)
                        mysql.connection.commit()
                        return {"success":True, "reload":True, "message":"Deleted Successfully"}
                    except Exception as e:
                        return {"success":False, "reload":False, "message":str(e.args[0])}
                else:
                    return redirect('/admin/outlets')



            
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
                
                resident_query = f"""   SELECT RESIDENT.resident_id, CONCAT(first_name, " ", last_name), RESIDENT.gender, room_no, hostel_name, RESIDENT.email_id as full_name
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

                # Fetching all the available years 
                cur.execute(""" SELECT distinct year from
                                ACADEMIC_PERIOD;""")
                years = cur.fetchall()

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
                                    years = years,
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
        
    elif (page_name == "housekeeping"):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            if request.method == 'GET':
                
                # Getting the query parameters
                search_ID = request.args.get('search_ID')
                hostel = request.args.get('hostel_name')
                housekeeping_type = request.args.get('type_name')

                a = [search_ID, hostel, housekeeping_type]

                # Generating the sql query string
                query_string = ""
                if (search_ID != None and search_ID != ""):
                    query_string += f" HOUSE_KEEPING.housekeeper_id = {search_ID} "
                if (hostel != None and hostel != "all"):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" hostel_name = '{hostel}' "
                if (housekeeping_type != None and housekeeping_type != "all"):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" type = '{housekeeping_type}' "
                if (query_string != ""):
                    query_string = "where" + query_string
                app.logger.info(query_string)
                
                housekeeping_query = f"""   select HOUSE_KEEPING.housekeeper_id, concat(first_name," ",last_name) as full_name
                                        from HOUSE_KEEPING LEFT JOIN HOUSE_KEEPING_SHIFTS ON HOUSE_KEEPING.housekeeper_id = HOUSE_KEEPING_SHIFTS.housekeeper_id
                                        {query_string}  """
                # Getting all the data corresponding to the residents
                cur.execute(housekeeping_query)
                housekeeping = cur.fetchall()

                # Fetching all the availble hostel names
                cur.execute(""" SELECT hostel_name from
                                HOSTEL;""")
                hostel_names = cur.fetchall()

                cur.execute(""" SELECT distinct type from
                                HOUSE_KEEPING_SHIFTS;""")
                types = cur.fetchall()

                # Rendering the template
                return render_template('admin_housekeeping.html', 
                                        pages = admin_pages, 
                                        housekeeping = housekeeping,
                                        housekeeping_details_field_names = list(housekeeping_details_field_names.keys()),
                                        hostel_names=hostel_names,
                                        housekeeping_types=housekeeping_types,
                                        gender_types=gender_types
                                        )
            else:
                return "got the request"
        else:
            return redirect('/admin/login')
        
    elif(page_name=="furniture"):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            if request.method == 'GET':
                
                # Getting the query parameters
                search_ID = request.args.get('search_ID')
                status=request.args.get('status')
                hostel = request.args.get('hostel')
                room_no=request.args.get('room_no')

                a = [search_ID, status, hostel, room_no]

                # Generating the sql query string
                query_string = ""
                if (search_ID != None and search_ID != ""):
                    query_string += f" FURNITURE.furniture_id = '{search_ID}' "
                if (hostel != None and hostel != "all"):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" hostel_name = '{hostel}' "
                if (room_no != None and room_no != ""):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" room_no = '{room_no}' "
                if (status != None and status != "all"):
                    if (query_string != ""):
                        query_string += "and"
                    query_string += f" status = '{status}' "
                if (query_string != ""):
                    query_string = "where" + query_string
                # app.logger.info("SELECT FURNITURE.furniture_id, status FROM FURNITURE {query_string}")
                furniture_query = f"""  SELECT FURNITURE.furniture_id, status
                                        FROM FURNITURE
                                        {query_string}  """
                # Getting all the data corresponding to the residents
                cur.execute(furniture_query)
                furnitures = cur.fetchall()
                
                # Defining the field names for the fields of the form
                # field_names = ["ID", "Full Name", "Semester", "Year", "Room No", "Hostel Name", "Entry Date", "Payment Status", "Due Amount", "Due Status", "Payment Amount", "First Name", "Middle Name", "Last Name", "Gender", "Blood Group", "Email ID", "City", "Postal Code", "Home Contact", "Resident Type"]
                
                # Fetching all the availble hostel names
                cur.execute(""" SELECT hostel_name from
                                HOSTEL;""")
                hostel_names = cur.fetchall()
                

                # Getting all the Program types
                cur.execute(""" SELECT distinct status from
                                FURNITURE;""")
                status_types = cur.fetchall()

                # Getting all the branch types
                cur.execute(""" SELECT distinct room_no from
                                ROOM;""")
                diff_rooms = cur.fetchall()

                # Rendering the template
                return render_template('admin_furnitures.html', 
                                    pages = admin_pages, 
                                    furnitures = furnitures, 
                                    hostel_names = hostel_names, 
                                    status_types=status_types,
                                    diff_rooms=diff_rooms,
                                    furniture_details_field_names = list(furniture_details_field_names.keys()))
            else:
                return "got the request"    
        else:
            return redirect('/admin/login')

    elif(page_name=="hostel"):
        if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
            if request.method == 'GET':
                hostel_query = f"""  SELECT HOSTEL.hostel_name
                                        FROM HOSTEL  order by hostel_name"""
                # Getting all the data corresponding to the residents
                cur.execute(hostel_query)
                hostels = cur.fetchall()
                # Rendering the template
                return render_template('admin_hostels.html', 
                                    pages = admin_pages, 
                                    hostels=hostels,
                                    hostel_details_field_names = list(hostel_details_field_names.keys()))
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

# @app.route('/admin/furniture/<furniture_id>/<operation>', methods=['POST'])
# def admin_furniture_operations(furniture_id=None, operation=None):
#     cur = mysql.connection.cursor()
#     # Handling the authentication
#     if not ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
#         return "Invalid Authentication"
#     # Handling invalid operations
#     if operation not in ['remove_furniture_from_room']:
#         return "Invalid Operation"
#     if operation == 'remove_furniture_from_room':
#         query_string = f"UPDATE FURNITURE SET room_no=NULL, hostel_name=NULL WHERE furniture_id='{furniture_id}';"
#         cur.execute(query_string)
#         cur.connection.commit()

#         return redirect(request.referrer)     
        
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
        try:
            cur.execute(query_string)
            mysql.connection.commit()
            return {"success":True, "reload":True, "message":"Room Data Updated Successfully"}
        except Exception as e:
            return {"success":False, "reload":False, "message":str(e.args[1])}
    
    if operation == 'update_current_room_allocation':
        query_string = ""
        for field in request.form:
            if field != 'update':
                if query_string != "":
                    query_string += ", "
                query_string += f"{room_current_allocation_field_names[field]}='{request.form[field]}'"
        query_string = "UPDATE CURRENT_ALLOCATION SET " + query_string + f" WHERE hostel_name='{hostel_name}' AND room_no='{room_no}' AND resident_id='{request.form['ID']}';"
        try:
            cur.execute(query_string)
            mysql.connection.commit()
            return {"success":True, "reload":True, "message":"Room Allocation Updated Successfully"}
        except Exception as e:
            return {"success":False, "reload":False, "message":str(e.args[1])}
    
    if operation == 'update_furniture_details':
        status_value = (1 if (request.form.get("status")!="on") else 0)
        furniture_id = request.form["furniture_id"]
        query_string = f"UPDATE FURNITURE SET status='{status_value}' WHERE furniture_id='{furniture_id}';"
        try:
            cur.execute(query_string)
            mysql.connection.commit()
            return {"success":True, "reload":True, "message":"Furniture Details Updated Successfully"}
        except Exception as e:
            return {"success":False, "reload":False, "message":str(e.args[1])}

        return redirect('/admin/rooms')
    if operation == 'add_furniture_to_room':
        furniture_id = request.form["furniture_id"]
        query_string = f"UPDATE FURNITURE SET hostel_name='{hostel_name}', room_no='{room_no}' WHERE furniture_id='{furniture_id}';"
        try:
            cur.execute(query_string)
            mysql.connection.commit()   
            return {"success":True, "reload":True, "message":"Furniture Added Successfully to Room"}
        except Exception as e:
            return {"success":False, "reload":False, "message":str(e.args[1])}
    
    if operation == 'delete_room':
        query_string = f"DELETE FROM ROOM WHERE hostel_name='{hostel_name}' AND room_no='{room_no}';"
        try:
            cur.execute(query_string)
            mysql.connection.commit()
            return {"success":True, "reload":True, "message":"Room Deleted Successfully"}
        except Exception as e:
            return {"success":False, "reload":False, "message":str(e.args[1])}


# Handling the post request for the admin/residents/<resident_id> page
@app.route('/admin/residents/<resident_id>', methods=['POST'])
def admin_resident_data(resident_id):
    cur = mysql.connection.cursor()
    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        
        # Fetching the resident details
        cur.execute(f"""select RESIDENT.resident_id, first_name, middle_name, last_name, gender, blood_group, email_id, city, postal_code, resident_type, Guardian_first_name, Guardian_type, home_contact
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

# Handling the post request for the admin/housekeeping/<housekeeper_id> page
@app.route('/admin/housekeeping/<housekeeper_id>', methods=['POST'])
def admin_housekeeping_data(housekeeper_id):
    cur = mysql.connection.cursor()
    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        
        # Fetching the resident details
        cur.execute(f"""select HOUSE_KEEPING.housekeeper_id, first_name, middle_name, last_name, gender
                        from (HOUSE_KEEPING)
                        where HOUSE_KEEPING.housekeeper_id = {housekeeper_id};""")
        housekeeping_details = cur.fetchall()[0]

        # Fetching the current allocation details
        cur.execute(f"""select hostel_name, type
                        from HOUSE_KEEPING_SHIFTS
                        where HOUSE_KEEPING_SHIFTS.housekeeper_id = {housekeeper_id};""")
        housekeeping_current_allocation_details = cur.fetchall()
        # try:
        #     resident_current_allocation_details = resident_current_allocation_details[0]
        # except:
        #     resident_current_allocation_details = []

        # Fetching the phone numbers
        cur.execute(f"""select phone_no
                        from HOUSE_KEEPING_PHONE
                        where HOUSE_KEEPING_PHONE.housekeeper_id = {housekeeper_id};""")
        housekeeping_phone_details = cur.fetchall()
        
        # Fetching all the availble hostel names
        cur.execute(""" SELECT hostel_name from
                        HOSTEL;""")
        hostel_names = cur.fetchall()

        cur.execute(""" SELECT distinct type from
                        HOUSE_KEEPING_SHIFTS;""")
        types = cur.fetchall()

        return render_template('admin_housekeeping_data.html', 
                                housekeeping_details = housekeeping_details, 
                                housekeeping_details_field_names = list(housekeeping_details_field_names.keys()), 
                                housekeeping_current_allocation_details = housekeeping_current_allocation_details,
                                housekeeping_current_allocation_field_names = list(housekeeping_current_allocation_field_names.keys()),
                                housekeeping_phone_details = housekeeping_phone_details,
                                hostel_names = hostel_names, 
                                housekeeping_types=housekeeping_types,
                                gender_types=gender_types,
                                today = datetime.date.today())  

@app.route('/admin/furniture/<furniture_id>', methods=['POST'])
def admin_furniture_data(furniture_id):
    cur = mysql.connection.cursor()
    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        
        # Fetching the resident details
        cur.execute(f"""select furniture_id, hostel_name, room_no, status
                        from (FURNITURE)
                        where FURNITURE.furniture_id = '{furniture_id}';""")
        furniture_details = cur.fetchall()
        try:
            furniture_details = furniture_details[0]
        except:
            furniture_details = []

        
        # Fetching all the availble hostel names
        cur.execute(""" SELECT hostel_name from
                        HOSTEL;""")
        hostel_names = cur.fetchall()

        return render_template('admin_furniture_data.html', 
                                furniture_details = furniture_details, 
                                furniture_details_field_names = list(furniture_details_field_names.keys()), 
                                hostel_names = hostel_names, 
                                today = datetime.date.today())  

@app.route('/admin/hostel/<hostel_name>', methods=['POST'])
def admin_hostel_data(hostel_name):
    cur = mysql.connection.cursor()
    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        
        # Fetching the resident details
        cur.execute(f"""select hostel_name, contact, energy_consumption, water_consumption, caretaker_id
                        from (HOSTEL)
                        where hostel_name = '{hostel_name}';""")
        hostel_details = cur.fetchall()
        try:
            hostel_details = hostel_details[0]
        except:
            hostel_details = []

        
        # Fetching all the availble hostel names
        cur.execute(""" SELECT hostel_name from
                        HOSTEL;""")
        hostel_names = cur.fetchall()

        return render_template('admin_hostel_data.html', 
                                hostel_details = hostel_details, 
                                hostel_details_field_names = list(hostel_details_field_names.keys()), 
                                hostel_names = hostel_names, 
                                today = datetime.date.today())  


@app.route('/admin/residents/<resident_id>/<operation>', methods=['POST'])
def resident_operations(resident_id, operation):
    
    # Error handling
    if (operation not in ['update_details', 'update_current_allocation', 'deallocate_resident', 'delete_phone', "add_phone", 'update_program', "add_allocation"]):
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
            try:
                # Adding the select and where clause
                query_string = f"UPDATE RESIDENT SET {query_string} WHERE resident_id = {resident_id};"
                
                # Executing the query and commiting the changes
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success": True, "reload":True, "message": "Succesfully updated details"}
            
            except Exception as e:
                return {"success": False, "reload":False, "message":e.args[1]}
        
        elif (operation == 'delete_phone'):
            query_string = f"DELETE FROM RESIDENT_PHONE WHERE resident_id = {resident_id} AND phone_no = '{request.form['phone_no']}';"
            try:
                # Executing the query and commiting the changes
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success": True, "reload":True, "message": "Succesfully deleted phone number"}
            except Exception as e:
                return {"success": False, "reload":False, "message":e.args[1]}

        
        elif (operation == 'add_allocation'):
            query_string = ""
            text_string = ""
            for field in request.form.keys():
                if (field != "add"):
                    if (query_string != ""):
                        query_string += ", "
                    if (text_string != ""):
                        text_string += ", "
                    text_string += f"{resident_current_allocation_field_names[field]}"
                    query_string += f"'{request.form[field]}'"
            query_string = f"INSERT INTO CURRENT_ALLOCATION(resident_id, {text_string}) VALUES ({resident_id}, {query_string});"
            try:
                # Executing the query and commiting the changes
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success": True, "reload":True, "message": "Succesfully added allocation"}
            except Exception as e:
                return {"success": False, "reload":False, "message":e.args[1]}
        
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
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success": True, "reload":True, "message": "Succesfully added phone number"}
            except Exception as e:
                return {"success": False, "reload":False, "message":e.args[1]}

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
            try:
                cur.execute(f"""
                                CALL DEALLOCATE({resident_id}, STR_TO_DATE('{request.form['exit_date']}', '%Y-%m-%d'));
                            """)
                mysql.connection.commit()
                return {"success": True, "reload":True, "message": "Succesfully deallocated"}
            except Exception as e:
                return {"success": False, "reload":False, "message":e.args[1]}
 
@app.route('/admin/security/<security_id>/<operation>', methods=['POST'])
def security_operations(security_id, operation):
    
    # Error handling
    if (operation not in ['update_details', 'add_allocation', 'delete_phone', "add_phone","delete_current_allocation","delete_security"]):
        return redirect('/admin/security')
    
    # Connecting to the database
    cur = mysql.connection.cursor()

    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        if (operation == 'update_details'):
            # Generating the query string
            query_string = ""
            for field in request.form.keys():
                if (field != "update" and request.form[field]!=''):
                    if (query_string != ""):
                        query_string += ", "
                    query_string += f"{security_details_field_names[field]} = '{request.form[field]}'"
            # Adding the select and where clause
            query_string = f"UPDATE GUARD SET {query_string} WHERE security_id = {security_id};"
            try:
                # Executing the query and commiting the changes
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success": True, "reload":True, "message": "Succesfully updated details"}
            except Exception as e:
                return {"success": False, "reload":False, "message":e.args[1]}
        
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
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":True, "reload": True, "message":"Removed Security from Hostel"}
            except Exception as e:
                return {"success":False, "reload": False, "message":str(e.args[1])}
        
        elif operation == 'add_phone':
            query_string = f"INSERT INTO GUARD_PHONE(security_id, phone_no) VALUES ({security_id}, '{request.form['phone_no']}');"
            # Executing the query and commiting the changes
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":True, "reload": True, "message":"Added Phone Number"}
            except Exception as e:
                return {"success":False, "reload": False, "message":str(e.args[1])}

            # Redirecting to the resident page
            return redirect(f'/admin/security')
        elif operation=="delete_security":
            query_string = f"DELETE FROM GUARD WHERE security_id='{security_id}';"
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":True, "reload": True, "message":"Deleted Security"}
            except Exception as e:
                return {"success":False, "reload": False, "message":str(e.args[1])}


        elif (operation == 'add_allocation'):
            # Adding the update and where clause
            query_string= f"INSERT INTO SECURITY(security_id, hostel_name, start_time, end_time) VALUES({security_id},'{request.form['hostel_name']}','{request.form['start_time']}','{request.form['end_time']}');"
            # Executing the query and commiting the changes
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":True, "reload": True, "message":"Allocated Security"}
            except Exception as e:
                return {"success":False, "reload": False, "message":str(e.args[1])}


@app.route('/admin/housekeeping/<housekeeper_id>/<operation>', methods=['POST'])
def housekeeping_operations(housekeeper_id, operation):
    
    # Error handling
    if (operation not in ['update_details', 'add_allocation', 'delete_phone', "add_phone","delete_current_allocation","delete_housekeeping"]):
        return redirect('/admin/housekeeping')
    
    # Connecting to the database
    cur = mysql.connection.cursor()

    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        if (operation == 'update_details'):
            # Generating the query string
            query_string = ""
            for field in request.form.keys():
                if (field != "update" and request.form[field]!=''):
                    if (query_string != ""):
                        query_string += ", "
                    query_string += f"{housekeeping_details_field_names[field]} = '{request.form[field]}'"
            # Adding the select and where clause
            query_string = f"UPDATE HOUSE_KEEPING SET {query_string} WHERE housekeeper_id = {housekeeper_id};"
            try:
                # Executing the query and commiting the changes
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success": True, "reload":True, "message": "Succesfully updated details"}
            except Exception as e:
                return {"success": False, "reload":False, "message":e.args[1]}
        
        elif (operation == 'delete_phone'):
            query_string = f"DELETE FROM HOUSE_KEEPING_PHONE WHERE housekeeper_id = {housekeeper_id} AND phone_no = '{request.form['phone_no']}';"
            # Executing the query and commiting the changes
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success": True, "reload":True, "message": "Succesfully updated details"}
            except Exception as e:
                return {"success": False, "reload":False, "message":e.args[1]}
        
        elif operation=='delete_current_allocation':
            query_string = f"DELETE FROM HOUSE_KEEPING_SHIFTS WHERE housekeeper_id = {housekeeper_id} AND hostel_name = '{request.form['hostel_name']}';"
            # Executing the query and commiting the changes
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":True, "reload": True, "message":"Removed House Keeper from Hostel"}
            except Exception as e:
                return {"success":False, "reload": False, "message":str(e.args[1])}
        
        elif operation == 'add_phone':
            query_string = f"INSERT INTO HOUSE_KEEPING_PHONE(housekeeper_id, phone_no) VALUES ({housekeeper_id}, '{request.form['phone_no']}');"
            # Executing the query and commiting the changes
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":True, "reload": True, "message":"Added Phone Number"}
            except Exception as e:
                return {"success":False, "reload": False, "message":str(e.args[1])}
            
        elif operation=="delete_housekeeping":
            query_string = f"DELETE FROM HOUSE_KEEPING WHERE housekeeper_id='{housekeeper_id}';"
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":True, "reload": True, "message":"Deleted Housekeeper"}
            except Exception as e:
                return {"success":False, "reload": False, "message":str(e.args[1])}


        elif (operation == 'add_allocation'):
            # Adding the update and where clause
            query_string= f"INSERT INTO HOUSE_KEEPING_SHIFTS(housekeeper_id, type, hostel_name) VALUES({housekeeper_id},'{request.form['type_name']}','{request.form['hostel_name']}');"
            # Executing the query and commiting the changes
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":True, "reload": True, "message":"Allocated Housekeeper"}
            except Exception as e:
                return {"success":False, "reload": False, "message":str(e.args[1])}


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
                try:
                    # Executing the query and commiting the changes
                    cur.execute(query_string)
                    mysql.connection.commit()
                    return {"success":True, "reload": True, "message":"Academic Period added successfully"}
                except Exception as e:
                    return {"success":False, "reload": False, "message": e.args[1]}
            else:
                return {"success":False, "reload": False, "message":"Academic Period already exists"}
@app.route('/admin/furniture/<furniture_id>/<operation>', methods=['POST'])
def admin_furniture_operations(furniture_id, operation):
    # Error handling
    if (operation not in ['update_furniture_details', 'delete_furniture','remove_furniture_from_room']):
        return redirect('/admin/furniture')
    
    # Connecting to the database
    cur = mysql.connection.cursor()

    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        if (operation == 'update_furniture_details'):
            # Generating the query string
            query_string = ""
            for field in request.form.keys():
                if (field != "update"   ):
                    if (query_string != ""):
                        query_string += ", "
                    query_string += f"{furniture_details_field_names[field]} = '{request.form[field]}'"
            # Adding the select and where clause
            query_string = f"UPDATE FURNITURE SET {query_string} WHERE FURNITURE.furniture_id = '{furniture_id}';"
            try:
                # Executing the query and commiting the changes
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":True, "reload":True, "message":"Furniture details updated"}
            except Exception as e:
                return {"success":False, "reload":False, "message":str(e.args[1])}

        if operation == 'delete_furniture':
            query_string = f"DELETE FROM FURNITURE WHERE furniture_id='{furniture_id}';"
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":True, "reload":True, "message":"Furniture deleted"}
            except Exception as e:
                return {"success":False, "reload":False, "message":str(e.args[1])}
        
        if operation == 'remove_furniture_from_room':
            query_string = f"UPDATE FURNITURE SET room_no=NULL, hostel_name=NULL WHERE furniture_id='{furniture_id}';"
            try:
                cur.execute(query_string)
                cur.connection.commit()
                return {"success":True, "reload":True, "message":"Furniture removed from room"}
            except Exception as e:
                return {"success":False, "reload":False, "message":str(e.args[1])}
        
@app.route('/admin/hostel/<hostel_name>/<operation>', methods=['POST'])
def admin_hostel_operations(hostel_name, operation):
    # Error handling
    if (operation not in ['update_hostel_details', 'delete_hostel']):
        return redirect('/admin/hostel')
    
    # Connecting to the database
    cur = mysql.connection.cursor()

    if ('logged_in' in session and "name" in session and session['logged_in'] == True and session['name'] == 'admin'):
        if (operation == 'update_hostel_details'):
            # Generating the query string
            query_string = ""
            for field in request.form.keys():
                if (field != "update" and request.form[field]!=''):
                    if (query_string != ""):
                        query_string += ", "
                    query_string += f"{hostel_details_field_names[field]} = '{request.form[field]}'"
            # Adding the select and where clause
            query_string = f"UPDATE HOSTEL SET {query_string} WHERE hostel_name = '{hostel_name}';"
            try:
                # Executing the query and commiting the changes
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":False, "reload":False, "message": "Succssfully updated the hostel details"}
            except Exception as e:
                return {"success":False, "reload":False, "message": e.args[1]}
 
        if operation == 'delete_hostel':
            query_string = f"DELETE FROM HOSTEL WHERE hostel_name='{hostel_name}';"
            try:
                cur.execute(query_string)
                mysql.connection.commit()
                return {"success":True, "reload":True, "message": "Succssfully deleted the hostel"}
            except Exception as e:
                return {"success":False, "reload":False, "message": e.args[1]}
# Running the app
if __name__ == '__main__':
    app.run(debug=True)
