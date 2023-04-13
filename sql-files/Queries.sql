use hostelmng;

(select bf3.*, ca.total_residents
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
                    on ca.hostel_name = bf3.hostel_name);
                    
select outlet_name, open_time, close_time, hostel_name, concat(owner_first_name," ",owner_last_name) as owner_name 
                   from OUTLET;
                   
                   
                   
select phone_no, OUTLET_PHONE.outlet_name 
                   from OUTLET INNER JOIN OUTLET_PHONE on OUTLET_PHONE.outlet_name=OUTLET.outlet_name;


ALTER TABLE users
RENAME COLUMN id TO resident_id;

select outlet_name from OUTLET;

 select HOSTEL.caretaker_id, concat(first_name," ", last_name) as Name, office_no, email_id, hostel_name, contact
                    from CARETAKER INNER JOIN HOSTEL on HOSTEL.caretaker_id=CARETAKER.caretaker_id
                    order by HOSTEL.hostel_name;
	
select phone_no, CARETAKER.caretaker_id  from CARETAKER INNER JOIN CARETAKER_PHONE on CARETAKER_PHONE.caretaker_id=CARETAKER.caretaker_id order by caretaker_id;

select caretaker_id from CARETAKER;
select semester, year
                    from ACADEMIC_PERIOD
                    order by year, semester;
                    
                    
show columns 
                                from RESIDENT;
                                
select distinct hostel_name from HOSTEL;

select distinct room_type from ROOM;

SELECT hostel_name, occupied, room_type, COUNT(hostel_name)
                            FROM ROOM
                            where room_type = "triple" or room_type = "single" or room_type = "double"
                            GROUP BY occupied, room_type, hostel_name
                            ORDER BY hostel_name;
                            
select caretaker_id,concat(first_name,' ',last_name) as name, gender, 
                                        office_no, email_id
                                        from CARETAKER;

select hostel_name, caretaker_id
                                from HOSTEL;
                                
select *
                                from CARETAKER_PHONE;
                                
SELECT hostel_name from
                                HOSTEL;
                                
SELECT distinct program from
                                DEGREE;
                                
SELECT distinct branch from
                                DEGREE;
                                
SELECT distinct year from
                                ACADEMIC_PERIOD;




-- The one which includes the parameters are shown below
/*
cur.execute("SELECT key_ FROM users WHERE id = %s;", (id,))

cur.execute(""" SELECT * 
                                from RESIDENT
                                where resident_id = %s;""",(session['id'],))

cur.execute(""" select phone_no
                                from RESIDENT_PHONE
                                where resident_id = %s;""",(session['id'],))
                                

cur.execute("""select program, branch
                                from ENROLLED_IN 
                                where resident_id = %s; """,(session['id'],))

cur.execute(f"SELECT key_ FROM users WHERE id = {session['id']};")

cur.execute(f"UPDATE users SET key_ = '{new_key}' WHERE id = {session['id']};")

cur.execute(""" select year, semester, hostel_name, room_no,entry_date,exit_date
                            from ALLOCATION
                            where resident_id = %s
                            union
                            select year, semester, hostel_name, room_no,entry_date,null
                            from CURRENT_ALLOCATION
                            where resident_id = %s
                            order by year desc,semester desc;""",(session['id'],session['id'],))
                            
                            
cur.execute(""" select rhc.*, ca.entry_date, payment_amount, payment_status, due_amount,due_status
                            from CURRENT_ALLOCATION as ca
                            INNER JOIN 
                            (select  r.room_no, r.room_type ,hc.* from ROOM as r INNER JOIN 
                            (select hostel_name,contact, h.caretaker_id, concat(first_name, " ",last_name) as caretaker_name, office_no, email_id
                            from HOSTEL as h INNER JOIN CARETAKER as c on h.caretaker_id = c.caretaker_id) as hc
                            on r.hostel_name = hc.hostel_name) as rhc
                            on (ca.hostel_name = rhc.hostel_name AND ca.room_no = rhc.room_no)
                            where resident_id=%s;""",(session['id'],))
                            

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
                            where resident_id=%s;""",(session['id'],)
                            

cur.execute(f"select * from ROOM {query_string};")

cur.execute("INSERT INTO ROOM (" + "hostel_name, room_type, room_no, occupied" + ") VALUES (" + f"'{hostel_name}', '{room_type}', '{room_no}', 0" + ");")


cur.execute(f"UPDATE ENROLLED_IN SET program='{request.form['program']}', branch = '{request.form['branch']}' where resident_id = {resident_id};")

cur.execute(f"INSERT INTO GUARD_PHONE(security_id, phone_no) VALUES ({security_id}, '{request.form['phone_no']}');")

cur.execute("INSERT INTO FURNITURE (" + table_order + ") VALUES (" + query_string + ");")

cur.execute("INSERT INTO HOSTEL (" + table_order + ") VALUES (" + query_string + ");")

cur.execute(f""" delete from CARETAKER_PHONE
                                            where caretaker_id = '{caretaker_id}';
                                    """)
                                    
 cur.execute(f""" DELETE FROM  CARETAKER 
                                    where caretaker_id = '{request.form.get('caretaker_id')}'
                                    """)
                                    
*/

-- some of the queries are skipped as they were lot of them, we can simply search for cur.execute() in app.py to get the data.

