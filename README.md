# Steps to use our web app
1. Install Virtual env using the command `pip install virtualenv`
2. Navigate to the project folder.
> **_Note_**: Make sure that the python version is greater than 3.10
3. Create a virtual environment using the command `python3 -m venv venv`
4. Activate the virtual environment using 
> For mac/linux: `source venv/bin/activate`\
> For windows: `.\venv\Scripts\activate.bat`\
> **_Note_**: To deactivate the environment use the command `deactivate`
5. Install the required packages using the `requirements.txt` file using the command `pip install -r requirements.txt`.
6. Run the sql files in the folder `sql-files` in the order `TableCreationSQL.sql`, `create_admin.sql`, `triggers.sql`, and `population_final.sql`
7. Set the database configurations in `app.py` and `generate_user_password.py`.
8. Generate the `resident_id` and their `passwords` by running the `generate_user_password.py` using command `python3 generate_user_password.py`.
9. Run the server.


# Used frameworks and libraries
### Frontend Libraries used
1. Bootstrap 
2. CSS 
3. JS
### Backend Libraries used
1. Flask(Python)
2. Jinja templating that comes with flask
3. Numpy(Python)

# Users
1. Admin
2. Resident
3. Public

Login credentials for Admin:  
Admin ID : 00000001  
Admin password : password  

Login credentials for Resident:  
Resident ID: between 20000000 and 20000300  
Resident password: password  

# Screenshots for following operations

## INSERT
Add Resident
### Before
![image](https://user-images.githubusercontent.com/80308830/226424118-8579ca6f-39e1-494f-a493-a5abe1fb5eb7.png)
### Inserting
![image](https://user-images.githubusercontent.com/80308830/226424474-4690c41a-7d36-41fd-8301-2d2117c507b5.png)
### Pop up
![image](https://user-images.githubusercontent.com/80308830/226424617-d51611f2-b3c2-402f-bca1-99e365db21db.png)
### After
![image](https://user-images.githubusercontent.com/80308830/226425784-c7603338-ebef-4158-a31d-d1b8b0875e82.png)

## UPDATE
Resident Details Update
### Updating
![image](https://user-images.githubusercontent.com/80308830/226427265-88bfb783-2f8e-4294-be90-dfe884cb02f7.png)
### Pop up
![image](https://user-images.githubusercontent.com/80308830/226491102-8d8be9e0-93d0-4797-9694-a3f91955a257.png)

### After
![image](https://user-images.githubusercontent.com/80308830/226444197-6eb93c89-ba4d-4bb3-ade0-1050bb6d1077.png)


## DELETE
Outlets Delete
### Before
![image](https://user-images.githubusercontent.com/80308830/226428100-5247ffce-b0a1-4ac3-99e2-a8cc4e7713dd.png)
### Deleting 
clicking on delete button 
![image](https://user-images.githubusercontent.com/80308830/226429972-5a89b455-2a18-453d-9b1f-d89231652f2f.png)

### After
![image](https://user-images.githubusercontent.com/80308830/226428235-22038403-7d59-42d9-b1e0-f4ef544fb039.png)
### Pop up
![image](https://user-images.githubusercontent.com/80308830/226491168-a1155e2c-30f9-435e-a533-daa66f03e104.png)

## RENAME
### Before
![image](https://user-images.githubusercontent.com/80308830/226437381-08913a54-37fe-4276-8c67-72d3dd4897c0.png)
### Renaming
![image](https://user-images.githubusercontent.com/80308830/226437882-cc66a732-c6f3-437a-b371-1ecd866acd61.png)
### After
![image](https://user-images.githubusercontent.com/80308830/226437962-ea2eb640-6ea6-4fac-99bc-6cef206bd8c4.png)


## WHERE clause
Residents filter 
### Before
![image](https://user-images.githubusercontent.com/80308830/226428727-9edd8097-2b5b-4145-ae6e-69422f71d54c.png)
### Applying Filter (Where)
![image](https://user-images.githubusercontent.com/80308830/226429182-569e3bde-625b-4c14-821e-a93acf8e9cdd.png)
### After
![image](https://user-images.githubusercontent.com/80308830/226429375-ea388748-b9f5-42a4-84e9-07401d850d31.png)




# Screenshots of our web app
## Homepage (Login Page)
![image](https://user-images.githubusercontent.com/76489649/226442376-88273631-c79b-4c38-b72d-cb5af4fbeccc.png)


## Admin Dashboard
![image](https://user-images.githubusercontent.com/80308830/226423771-aa566b35-72cf-452f-9c76-e058819bac83.png)
<br>

## Resident HomePage
![image](https://user-images.githubusercontent.com/80308830/226473617-c095cc39-d321-49ea-a86c-11d74dab5cd6.png)




# Contribution 
## G1
1. Kareena
2. Bhavini
3. Hamsini
4. Rajesh
5. Gnana Sai
6. Chaitanya


## G2 
1. Sriman 
2. Manish 
3. Sunny 
4. Siva Sai 
5. Karthik
6. Rishab
