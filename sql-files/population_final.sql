-- use hostelmng;

use hostelmng;

# drop procedure populate_hostel;
delimiter //
CREATE PROCEDURE populate_hostel()
BEGIN
	DECLARE counter INT DEFAULT 1;
	DECLARE hostel_name varchar(10);
    DECLARE contact numeric(10) DEFAULT 1000000000;
--     DECLARE total_rooms smallint;
--     DECLARE total_students smallint;
    DECLARE energy_consumption float(24);
    DECLARE water_consumption float(24);
    DECLARE caretaker_id numeric(8);
    DECLARE temp int default 0;
	WHILE (counter <= 12) DO -- change 10 to the desired number of tuples to insertw
		
		SET hostel_name = elt(counter, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l') ; 
-- 		SET total_rooms = 301; -- generates random total rooms
-- 		SET total_students = 450 + FLOOR(RAND() * 50) ; -- generates random total students
		SET energy_consumption = ROUND(RAND()*1000, 2) ; -- generates random energy consumption
		SET water_consumption = ROUND(RAND()*1000, 2) ; -- generates random water consumption
        set temp = 0 + (counter-1) %7;
        SET caretaker_id = (SELECT CARETAKER.caretaker_id FROM CARETAKER LIMIT temp, 1);
		INSERT INTO HOSTEL (hostel_name, contact, energy_consumption, water_consumption, caretaker_id)
		VALUES (hostel_name, contact, energy_consumption, water_consumption, caretaker_id);
		
		SET counter = counter + 1;
        SET contact = contact + 1;
	END WHILE ;

END //
delimiter ;

# drop procedure populate_caretaker;

delimiter //
CREATE PROCEDURE populate_caretaker()
BEGIN
    DECLARE caretaker_id numeric(8) DEFAULT 10000000;
    DECLARE first_name varchar(15);
    DECLARE middle_name varchar(15);
    DECLARE last_name varchar(15);
    DECLARE gender char(1);
    DECLARE office_no  varchar(5);
    DECLARE email_id varchar(320);
    DECLARE counter INT DEFAULT 1;
    WHILE (counter <= 7) DO -- change 10 to the desired number of tuples to insertw
        SET caretaker_id = caretaker_id + 1 ; 
        SET first_name = concat("caretakerfname", cast(counter as CHAR(2)));
        SET middle_name = concat("caretakermname", cast(counter as CHAR(2))); 
        SET last_name = concat("caretakerlname" , cast(counter as CHAR(2))); 
        SET gender = elt(FLOOR(1 + rand()*2 ), "F", "M") ; 
        SET office_no = concat(elt(counter, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'), cast(100 + FLOOR(RAND()*100) as char(3))) ; 
        SET email_id = concat(concat("caretakeremail", cast(counter as CHAR(2))), "@iitgn.ac.in");

        INSERT INTO CARETAKER (caretaker_id, first_name, middle_name, last_name, gender, office_no, email_id)
        VALUES (caretaker_id, first_name, middle_name, last_name, gender, office_no, email_id);

        SET counter = counter + 1;
    END WHILE ;

END //
delimiter ;
# drop procedure populate_caretaker_phone;
delimiter //
CREATE PROCEDURE populate_caretaker_phone()
BEGIN
	DECLARE phone_no numeric(10) DEFAULT 7000000000;
	DECLARE caretaker_id  numeric(8) DEFAULT 10000000;
    DECLARE count int;
    DECLARE counter int DEFAULT 1;
	WHILE (counter <= 7) DO -- change 10 to the desired number of tuples to insertw
		SET caretaker_id = caretaker_id + 1 ; 
		SET count = FLOOR(1 + rand() * 4);
        while(count > 0) Do
			SET phone_no = phone_no + 1;
            INSERT INTO CARETAKER_PHONE (phone_no, caretaker_id)
			VALUES (phone_no, caretaker_id);
            SET count = count - 1;
        end while;
		SET counter = counter + 1;
	END WHILE ;
END //
delimiter ;

# drop procedure populate_guard;
delimiter //
CREATE PROCEDURE populate_guard()
BEGIN
	DECLARE counter INT DEFAULT 1;
	DECLARE security_id numeric(8) DEFAULT 80000000;
    DECLARE first_name varchar(15);
    DECLARE middle_name varchar(15);
    DECLARE last_name varchar(15);
    
    while (counter <=10) DO 
		SET security_id = security_id + 1 ; -- generates random security ID
        SET first_name = concat("guardFName", cast(counter as char));
        SET middle_name = concat("guardMName", cast(counter as char));
        SET last_name = concat("guardLName", cast(counter as char));
        
        INSERT INTO GUARD (security_id, first_name, middle_name, last_name)
        VALUES (security_id, first_name, middle_name, last_name);
        SET counter = counter+1;
	END WHILE;
END //
delimiter;

# drop PROCEDURE populate_guard_phone;

delimiter //
CREATE PROCEDURE populate_guard_phone()
BEGIN
	DECLARE phone_no numeric(10) DEFAULT 7000000000;
	DECLARE security_id  numeric(8) DEFAULT 80000000;
    DECLARE count int;
    DECLARE counter int DEFAULT 1;
	WHILE (counter <= 10) DO -- change 10 to the desired number of tuples to insertw
		SET security_id = security_id + 1 ; 
		SET count = FLOOR(1 + rand() * 4);
        while(count > 0) Do
			SET phone_no = phone_no + 1;
            INSERT INTO GUARD_PHONE (phone_no, security_id)
			VALUES (phone_no, security_id);
            SET count = count - 1;
        end while;
		SET counter = counter + 1;
	END WHILE ;
END //
delimiter ;

# drop procedure populate_resident;
delimiter //
CREATE PROCEDURE populate_resident()
BEGIN
	DECLARE counter INT DEFAULT 1;
    DECLARE email_no INT DEFAULT 10;
    DECLARE resident_id numeric(8) DEFAULT 20000000;
    DECLARE first_name varchar(15);
    DECLARE middle_name varchar(15);
    DECLARE last_name varchar(15);
    DECLARE gender char(1);
    DECLARE blood_group char(3);
    DECLARE email_id VARCHAR(320);
    DECLARE city varchar(85);
    DECLARE postal_code numeric(6,0) DEFAULT 100000;
    DECLARE home_contact numeric(10,0) DEFAULT 5000000000;
    DECLARE resident_type varchar(15);
--     DECLARE on_campus bool;
    
    DECLARE hostel_num INT default 1;
    
	WHILE (counter <= 300) DO -- change 10 to the desired number of tuples to insertw
		
		SET resident_id = resident_id ; -- generates random hostel name
        SET first_name = concat("residentfn" , CAST(counter as char)) ;
        SET middle_name = concat("residentmn" , CAST(counter as char)) ;
        SET last_name = concat("residentln" , CAST(counter as char)) ;
		SET gender = CASE WHEN ROUND(RAND()*10,0) % 2 =0 THEN 'M' ELSE 'F' END;
        SET blood_group = concat(elt(floor(1 + rand() * 3), "O", "A", "B"), elt(floor(1 + rand() * 2), "+", "-"));
        SET email_id = concat("residentemail", cast(counter as CHAR),"@iitgn.ac.in");
        SET city = concat("city", CAST(counter as char)) ;
        SET postal_code = postal_code ;
        SET home_contact = home_contact ;
        SET resident_type = elt(floor(1 + rand() * 3), "student", "visitor", "faculty") ;
--         SET on_campus = CASE WHEN ROUND(RAND()*10,0) % 2 =0 THEN 0 ELSE 1 END;
        
		INSERT INTO RESIDENT(resident_id, first_name, middle_name, last_name, gender, blood_group, email_id, city, postal_code, home_contact, resident_type)
		VALUES (resident_id, first_name, middle_name, last_name, gender, blood_group, email_id, city, postal_code, home_contact, resident_type);
		SET counter = counter + 1;
        SET resident_id = resident_id + 1 ;
        SET postal_code = postal_code + 1 ;
        SET home_contact = home_contact + 1 ;
	END WHILE ;

END //
delimiter ;

# drop procedure populate_acadperiod;
delimiter //
CREATE PROCEDURE populate_acadperiod()
BEGIN
	DECLARE counter INT DEFAULT 1;
    DECLARE semester numeric(1,0) DEFAULT 8;
    DECLARE year numeric(4,0) DEFAULT 2008;
	WHILE (counter <= 15) DO -- change 10 to the desired number of tuples to insert
		set semester = 8;
        while (semester > 0) do
			INSERT INTO ACADEMIC_PERIOD (semester, year)
			VALUES (semester, year);
            set semester = semester - 1;
        end while;
		SET year = year + 1;
		SET counter = counter + 1;
	END WHILE ;
END //
delimiter ;

# drop PROCEDURE populate_degree;
delimiter //
CREATE PROCEDURE populate_degree()
BEGIN
	declare program1 varchar(6) ;
	declare branch1 varchar(10) ;
    DECLARE count INT DEFAULT 6;
	DECLARE counter INT DEFAULT 1;
	WHILE (counter <= 4) DO -- change 10 to the desired number of tuples to insertw
		
		SET program1 = concat("p" , counter) ; 
        set count = 6;
		while (count > 0) do
			SET branch1 = concat("b" , cast(count as char)) ; 
            INSERT INTO  DEGREE 
			VALUES (program1,branch1);
            set count = count - 1;
        end while;
		SET counter = counter + 1;
	END WHILE ;

END //
delimiter ;


# drop PROCEDURE populate_resident_phone;
delimiter //
CREATE PROCEDURE populate_resident_phone()
BEGIN
	DECLARE phone_no numeric(10, 0) default 5000000000;
	DECLARE resident_id numeric(8) default 20000000;
    DECLARE count INT DEFAULT 6;
	DECLARE counter INT DEFAULT 1;
	WHILE (counter <= 300) DO -- change 10 to the desired number of tuples to insertw
        set count = floor(1 + rand() * 4);
		while (count > 0) do
			SET phone_no = phone_no + 1 ; 
            INSERT INTO  RESIDENT_PHONE 
			VALUES (phone_no,resident_id);
            set count = count - 1;
        end while;
        SET resident_id = resident_id + 1 ; 
		SET counter = counter + 1;
	END WHILE ;

END //
delimiter ;

# drop procedure populate_outlet;
delimiter //
# Incomplete
create procedure populate_outlet()
begin
	Declare outlet_name varchar(40);
	Declare open_time  TIME ;
	Declare close_time TIME ;
	Declare contact  numeric(10) default 4000000000;
	Declare owner_first_name varchar(15) ;
	Declare owner_middle_name varchar(15);
	Declare owner_last_name varchar(15);
	Declare hostel_name varchar(10);
    declare counter int default 1;
    WHILE (counter <= 6) DO -- change 10 to the desired number of tuples to insertw
		set open_time = time(concat(4 + floor(rand()*10), ":0:0"));
        set close_time = time(concat(0 + floor(rand()*3), ":0:0"));
        set outlet_name = concat("outlet", counter);
		set hostel_name = elt(1 + floor(counter/2), "e", "a", 'h');
		set owner_first_name = concat("ownerfname", counter);
        set owner_middle_name = concat("ownermname", counter);
        set owner_last_name = concat("ownerlname", counter);
        INSERT INTO  OUTLET 
			VALUES (outlet_name,open_time, close_time, contact, owner_first_name, owner_middle_name, owner_last_name,hostel_name);
		SET counter = counter + 1;
        SET contact = contact + 1;
		set owner_first_name = concat("ownerfname", counter);
        set owner_middle_name = concat("ownermname", counter );
        set owner_last_name = concat("ownerlname", counter );
        set open_time = time(concat(4 + floor(rand()*10), ":0:0"));
        set close_time = time(concat(0 + floor(rand()*3), ":0:0"));
        set outlet_name = concat("outlet", counter);
		INSERT INTO  OUTLET 
			VALUES (outlet_name,open_time, close_time, contact, owner_first_name, owner_middle_name, owner_last_name,hostel_name);
		SET counter = counter + 1;
        SET contact = contact + 1;
	END WHILE ;
end //
delimiter ;

# drop procedure populate_outlet_phone;
delimiter //
# Incomplete 
create procedure  populate_outlet_phone()
begin
	Declare  phone_no numeric(10) default 4100000000;
	Declare  outlet_name varchar(40);
	declare counter int default 1;
	WHILE (counter <= 6) DO 
        set phone_no = phone_no + 1;
        set outlet_name = concat("outlet", counter);
        INSERT INTO  OUTLET_PHONE 
			VALUES (phone_no,outlet_name);
		set phone_no = phone_no + 1;
        INSERT INTO  OUTLET_PHONE 
			VALUES (phone_no,outlet_name);
		SET counter = counter + 1;
	END WHILE ;
end //
delimiter ;

# drop procedure populate_outlet_owner_phone;
delimiter //
CREATE PROCEDURE populate_outlet_owner_phone()
BEGIN
	DECLARE counter INT DEFAULT 1;
	DECLARE phone_no numeric(10) default 4200000000;
    DECLARE outlet_name varchar(40);
	WHILE (counter <= 6) DO 
        set phone_no = phone_no + 1;
        set outlet_name = concat("outlet", counter);
        INSERT INTO OUTLET_OWNER_PHONE
        values (phone_no, outlet_name);
        set phone_no = phone_no + 1;
        INSERT INTO OUTLET_OWNER_PHONE
        values (phone_no, outlet_name);
		SET counter = counter + 1;
	END WHILE ;
end //
delimiter ;

# drop PROCEDURE populate_allocation;
delimiter //



CREATE PROCEDURE populate_allocation()
BEGIN
	DECLARE counter INT DEFAULT 1;
	DECLARE semester numeric(1, 0);
    DECLARE year numeric(4, 0);
    DECLARE resident_id numeric(8, 0) default 20000000; 
    DECLARE room_no varchar(5);
    DECLARE hostel_name varchar(10);
    DECLARE entry_date DATE;
    DECLARE exit_date DATE;
    DECLARE payment_status INT;
    DECLARE due_amount INT;
    DECLARE due_status INT;
    DECLARE payment_amount INT;
    DECLARE del INT default 0;
    

    
    while(counter <= 300) do
        set year = 2019 + floor(rand() * 4);
        set semester = 1;
        set due_amount = 0;
        set due_status = 0;
        set payment_status = 5000;
        set payment_amount = 5000;
        set room_no = counter  + 100;
        if (room_no %25 = 0) then
        begin
         set room_no = counter+100 + 2+ (counter+1)%2;
          if ( counter+100 >= 400)then 
            set  room_no = counter+100 -1 ;
          end if ;
			
        end;
        end if;

        if ((select gender from RESIDENT where resident_id = RESIDENT.resident_id) = "F") then
        begin
			set hostel_name = 'a';
        end;
        else
        begin
			set hostel_name = 'j';
        end;
        end if;
		while(year <= 2021) do
			set entry_date = DATE(concat(year, "-09-01"));
            set exit_date = DATE(concat(year, "-11-30"));
            INSERT INTO ALLOCATION (semester, year, resident_id, room_no, hostel_name, entry_date, exit_date, payment_status, due_amount, due_status, payment_amount)
			values (semester, year, resident_id, room_no, hostel_name, entry_date, exit_date, payment_status, due_amount, due_status, payment_amount);
            set semester = semester + 1;
            set entry_date = DATE(concat(year, "-01-02"));
            set exit_date = DATE(concat(year, "-04-30"));
            INSERT INTO ALLOCATION (semester, year, resident_id, room_no, hostel_name, entry_date, exit_date, payment_status, due_amount, due_status, payment_amount)
			values (semester, year, resident_id, room_no, hostel_name, entry_date, exit_date, payment_status, due_amount, due_status, payment_amount);
            INSERT INTO ALLOCATION (semester, year, resident_id, room_no, hostel_name, entry_date, exit_date, payment_status, due_amount, due_status, payment_amount)
			values (semester, year, resident_id - 10000000, room_no, hostel_name, entry_date, exit_date, payment_status, due_amount, due_status, payment_amount);
            set semester = semester + 1;
            set year = year + 1;
        end while;
	
        set entry_date = DATE(concat(year, "-09-01"));
	    
		INSERT INTO CURRENT_ALLOCATION (semester, year, resident_id, room_no, hostel_name, entry_date,  payment_status, due_amount, due_status, payment_amount)
		values (semester, year, resident_id, room_no, hostel_name, entry_date,  payment_status, due_amount, due_status, payment_amount);
		
 --        UPDATE ROOM 
--         SET ROOM.occupied = 1 + ROOM.occupied 
--         where ROOM.room_no = room_no and ROOM.hostel_name = hostel_name;
--         
--         UPDATE HOSTEL
--         SET HOSTEL.total_students = HOSTEL.total_students + 1
--         where HOSTEL.hostel_name = hostel_name;
--         
        set semester = semester + 1;
        set resident_id = resident_id + 1;
        set counter = counter + 1;
	END WHILE ;
end //
delimiter ;

# drop procedure populate_room;
delimiter //
CREATE PROCEDURE populate_room()
BEGIN
	DECLARE room_no  varchar(5) ;
	DECLARE hostel_name varchar(10) ;
	DECLARE room_type varchar(20) ;
	DECLARE occupied tinyint ;
    declare count  int default 1 ;
    declare COUNTER INT  DEFAULT  100 ;
    	WHILE (counter <= 400) DO -- change 10 to the desired number of tuples to insertw

			set room_no  = cast(counter as  char);
			SET room_type  = elt(counter%2+1,"single","triple");
            set occupied = 0 ; 
			CASE  counter%50
				WHEN (0) THEN 
                begin
					set room_type = "bathroom";  

                end;
				WHEN (25) THEN 
                begin
					set room_type = "electrical" ;
      
				end;
                else
                begin end;
			END CASE;
            
		set count  = 1 ;
        while  (count < 12) do 
           SET hostel_name = elt(count, "a", "b", 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l') ;
           insert into ROOM (room_no,hostel_name,room_type,occupied)
           values (room_no,hostel_name,room_type,occupied);
           set count = count +1 ;
        end while ;
		SET counter = counter + 1;
	END WHILE ;
END //
delimiter ;

# drop PROCEDURE populate_enrolled_in;
delimiter //

CREATE PROCEDURE populate_enrolled_in()
BEGIN 
    Declare program varchar(6) ;
    declare branch varchar(10) ;
    DECLARE resident_id numeric(8) DEFAULT 20000000;
    DECLARE counter INT DEFAULT 0;
    declare type1 varchar(15);
    WHILE (counter <= 299) DO -- change 10 to the desired number of tuples to insertw

        SET program = concat("p" ,1+ counter%3) ; 
        SET branch = concat("b" , 1+counter%5) ; 
        set type1 = (select resident_type from RESIDENT limit counter,1 );
        if type1 = "student"  then 

        INSERT INTO  ENROLLED_IN (resident_id,program ,branch )
        VALUES (resident_id,program ,branch );
         end if;
        SET counter = counter + 1;
        SET resident_id = resident_id + 1 ;
    END WHILE ;

END //
delimiter ;


# drop procedure populate_security;

delimiter //
CREATE PROCEDURE populate_security()
BEGIN
	DECLARE counter INT DEFAULT 1;
    DECLARE security_id numeric(8) DEFAULT 80000000;
    DECLARE hostel_name varchar(10);
    DECLARE hostel_name1 varchar(10);
	DECLARE start_time TIME ; 
    DECLARE end_time TIME;
    
    while (counter <=10) DO 
		SET security_id = security_id +1; -- generates random security ID
        SET hostel_name = elt(1 + floor(rand() * 12), "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l");
        set start_time = time(concat(floor(24*rand()), ":00:00"));
        set end_time = time(concat(floor(24*rand()), ":00:00"));
        
        INSERT INTO SECURITY (security_id, hostel_name, start_time, end_time)
        VALUES (security_id, hostel_name, start_time, end_time);
        SET hostel_name1 = elt(1 + floor(rand() * 12), "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l");
        
        if (hostel_name1 != hostel_name) then
        begin 
			INSERT INTO SECURITY (security_id, hostel_name, start_time, end_time)
			VALUES (security_id, hostel_name1, start_time, end_time);
        end;
        end if;
        SET counter = counter+1;
	END WHILE;
END //
delimiter ;

# drop procedure populate_furniture;

delimiter //
CREATE PROCEDURE populate_furniture()
BEGIN

	DECLARE furniture_id varchar(32); 
    DECLARE status bool;
    DECLARE room_no varchar(5);
    DECLARE hostel_name varchar(10);
    Declare counter int default 100;
    declare count int default 0 ;
    
    while (counter <= 400) do
       set count  = 1 ;
       set status = floor(1+rand()) ;
       set room_no  = cast(counter as char);
       if  (counter%25 != 0) then 
       while (count < 12) do
		 SET hostel_name = elt(count, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l') ;
         
         set furniture_id = concat("furniture",counter);
         set furniture_id = concat(furniture_id, hostel_name);
         insert into FURNITURE (furniture_id,status,room_no,hostel_name)
         values (furniture_id,status,room_no,hostel_name);
        set count  = count +1 ;
       end while ;
       end if;
      set counter  = counter +1  ;
    end while ;
END //
delimiter ;

call populate_caretaker();
call populate_hostel();
call populate_caretaker_phone();
call populate_guard();
call populate_guard_phone();
call populate_resident();
CALL populate_acadperiod() ;
CALL populate_degree() ;
call populate_resident_phone();
call populate_outlet();
call populate_outlet_phone();
call populate_outlet_owner_phone();
call populate_room();
SET SQL_SAFE_UPDATES = 0;
call populate_allocation();
CALL populate_security();
call  populate_furniture();
call populate_enrolled_in();
