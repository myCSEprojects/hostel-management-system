show databases ;

drop database hostelmng;
create database hostelmng;

use hostelmng;

#drop table CARETAKER;
create table  CARETAKER(
    caretaker_id numeric(8) NOT NULL UNIQUE,
    first_name varchar(15) NOT NULL,			
    middle_name varchar(15),
    last_name varchar(15) NOT NULL,
    gender char(1) NOT NULL,
    office_no  varchar(5) NOT NULL UNIQUE,
    email_id varchar(320) NOT NULL UNIQUE,
    primary key(caretaker_id)
);

# drop table DEGREE;
create table DEGREE(
		program varchar(6) NOT NULL,
		branch varchar(10) NOT NULL,
		primary key(program,branch)
);

# Destroying the existing table of ACADEMIC_PERIOD
# drop table ACADEMIC_PERIOD;
# Table for storing the value of the Academic period
create table ACADEMIC_PERIOD(
	semester numeric(1, 0) NOT NULL, # Assuming values from 1 - 8
	year numeric(4,0) NOT NULL, # Considering only 4 digit values for years
    PRIMARY KEY (semester, year)
);

# Destroying the existing table of RESIDENTS
# drop table RESIDENT;
# Table for creating Residents of the Hostel
create table RESIDENT(
	resident_id numeric(8) PRIMARY KEY NOT NULL UNIQUE,
	first_name varchar(15) NOT NULL,
	middle_name varchar(15),
	last_name varchar(15) NOT NULL,
	gender char(1) NOT NULL,
	blood_group char(3) NOT NULL,
	email_id VARCHAR(320) NOT NULL,
	city varchar(85) NOT NULL,
	postal_code numeric(6, 0) NOT NULL,
	home_contact numeric(10, 0) NOT NULL UNIQUE,
	resident_type varchar(15) NOT NULL-- ,
-- 	on_campus bool NOT NULL
);

# Deleting existing resident_phone table
# drop table RESIDENT_PHONE;
# RESIDENT PHONE table
create table RESIDENT_PHONE(
	phone_no numeric(10, 0) NOT NULL UNIQUE,
	resident_id numeric(8) NOT NULL,
    PRIMARY KEY (phone_no, resident_id),
    FOREIGN KEY (resident_id) REFERENCES RESIDENT(resident_id) ON DELETE CASCADE ON UPDATE CASCADE
    
);

# drop table HOSTEL;
create table HOSTEL( 
	hostel_name varchar(10) NOT NULL UNIQUE,
	contact numeric(10) NOT NULL UNIQUE ,
-- 	total_rooms smallint NOT NULL, 
-- 	total_students smallint NOT NULL,
	energy_consumption float(24) NOT NULL,
	water_consumption float(24) NOT NULL,
	caretaker_id numeric(8),
	primary key (hostel_name),
	FOREIGN KEY (caretaker_id) REFERENCES CARETAKER(caretaker_id) ON DELETE SET NULL ON UPDATE CASCADE
);

# drop table ROOM;
create table ROOM(
	room_no  varchar(5) NOT NULL,
	hostel_name varchar(10) NOT NULL,
	room_type varchar(20) NOT NULL,
	occupied tinyint,
	primary key(room_no,hostel_name),
	FOREIGN KEY (hostel_name) REFERENCES HOSTEL(hostel_name) ON DELETE CASCADE ON UPDATE CASCADE
);


# drop table OUTLET;
create table OUTLET(
	outlet_name varchar(40) NOT NULL UNIQUE,
	open_time  TIME NOT NULL,
	close_time TIME  NOT NULL,
	contact  numeric(10) NOT NULL UNIQUE,
	owner_first_name varchar(15) NOT NULL,
	owner_middle_name varchar(15),
	owner_last_name varchar(15) NOT NULL,
	hostel_name varchar(10) NOT NULL,
	primary key (outlet_name),
	FOREIGN KEY (hostel_name) REFERENCES HOSTEL(hostel_name) ON DELETE CASCADE ON UPDATE CASCADE
);

# drop table OUTLET_PHONE;
create table  OUTLET_PHONE(
	phone_no numeric(10) NOT NULL UNIQUE,
	outlet_name varchar(40)  NOT NULL,
	PRIMARY KEY(outlet_name,phone_no),
	FOREIGN KEY (outlet_name)  REFERENCES OUTLET(outlet_name) ON DELETE CASCADE ON UPDATE CASCADE
);

# drop table OUTLET_OWNER_PHONE;
create table  OUTLET_OWNER_PHONE(
	phone_no numeric(10) NOT NULL UNIQUE,
	outlet_name varchar(40)  NOT NULL,
	PRIMARY KEY(outlet_name,phone_no),
	FOREIGN KEY (outlet_name)  REFERENCES OUTLET(outlet_name) ON DELETE CASCADE ON UPDATE CASCADE
);

# drop table CARETAKER_PHONE;
create table  CARETAKER_PHONE(
	phone_no numeric(10) NOT NULL UNIQUE,
	caretaker_id  numeric(8) NOT NULL,
	PRIMARY KEY(caretaker_id,phone_no),
	foreign key (caretaker_id)  REFERENCES CARETAKER(caretaker_id) ON DELETE CASCADE ON UPDATE CASCADE
);

# deleting existing table of Allocation
#drop table ALLOCATION;
# Allocation table


create table ALLOCATION(
	semester numeric(1, 0) NOT NULL,
	year numeric(4, 0) NOT NULL,
	resident_id numeric(8, 0) NOT NULL,
	room_no varchar(5) NOT NULL,
	hostel_name varchar(10) NOT NULL,
	entry_date DATE NOT NULL,
	exit_date DATE,
	payment_status INT NOT NULL,
	due_amount INT NOT NULL,
	due_status INT NOT NULL,
	payment_amount INT NOT NULL,
    PRIMARY KEY (semester, year, resident_id, room_no, hostel_name),
--     FOREIGN KEY (semester, year) REFERENCES ACADEMIC_PERIOD(semester, year) ON DELETE CASCADE,
--     FOREIGN KEY (resident_id) REFERENCES RESIDENT(resident_id) ON DELETE CASCADE,
    CHECK (payment_status <= payment_amount),
    CHECK (due_status <= due_amount),
    CHECK (YEAR(entry_date) >= 2008),
    CHECK (YEAR(exit_date) >= 2008)
);



create table CURRENT_ALLOCATION(
	semester numeric(1, 0) NOT NULL,
	year numeric(4, 0) NOT NULL,
	resident_id numeric(8, 0) NOT NULL,
	room_no varchar(5) NOT NULL,
	hostel_name varchar(10) NOT NULL,
	entry_date DATE NOT NULL,
	payment_status INT NOT NULL,
	due_amount INT NOT NULL,
	due_status INT NOT NULL,
	payment_amount INT NOT NULL,
    PRIMARY KEY (semester, year, resident_id, room_no, hostel_name),
    FOREIGN KEY (semester, year) REFERENCES ACADEMIC_PERIOD(semester, year) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (resident_id) REFERENCES RESIDENT(resident_id) ON DELETE CASCADE ON UPDATE CASCADE, 
    FOREIGN KEY (hostel_name,room_no) REFERENCES ROOM(hostel_name,room_no) ON DELETE CASCADE ON UPDATE CASCADE,
    
    CHECK (payment_status <= payment_amount),
    CHECK (due_status <= due_amount),
    CHECK (YEAR(entry_date) >= 2008)-- ,
--     CHECK (YEAR(exit_date) >= 2008)
);

# drop table ENROLLED_IN;
create table ENROLLED_IN(
	resident_id  numeric(8)  NOT NULL,
	program varchar(6) NOT NULL,
	branch varchar(10) NOT NULL,
	primary key(resident_id),
	foreign key (resident_id) references RESIDENT(resident_id) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key (program, branch) references DEGREE(program, branch) ON DELETE CASCADE ON UPDATE CASCADE
);

# drop table GUARD;
create table GUARD(
	security_id  numeric(8) NOT NULL UNIQUE,
	first_name varchar(15) NOT NULL,
	middle_name varchar(15),
	last_name varchar(15) NOT NULL,
	primary key(security_id)
);

# drop table SECURITY;
create table SECURITY(
	security_id  numeric(8) NOT NULL,
	hostel_name  varchar(10) NOT NULL ,
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	primary key(security_id,hostel_name),
	FOREIGN KEY (hostel_name) REFERENCES  HOSTEL(hostel_name) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (security_id) REFERENCES  GUARD(security_id) ON DELETE CASCADE ON UPDATE CASCADE
    
);

# drop table GUARD_PHONE;
create table  GUARD_PHONE(
	phone_no numeric(10) NOT NULL UNIQUE,
	security_id  numeric(8) NOT NULL,
	PRIMARY KEY(security_id,phone_no),
	foreign key (security_id)  REFERENCES GUARD(security_id) ON DELETE CASCADE ON UPDATE CASCADE
); 

# Deleting existing Furniture table
# drop table FURNITURE;
# Furniture
create table FURNITURE(
	furniture_id varchar(32) PRIMARY KEY NOT NULL UNIQUE,
	status bool NOT NULL ,# 1 Denotes that it is damaged
    room_no varchar(5),
    hostel_name varchar(10) ,
    foreign key (hostel_name,room_no)  references ROOM(hostel_name,room_no) ON DELETE SET NULL ON UPDATE CASCADE
);


