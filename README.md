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
6. Run the sql files in the folder `sql-files` in the order `TableCreationSQL.sql`, `triggers.sql`, and `population_final.sql`
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

# Users
1. Admin
2. Resident

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

## DELETE
Outlets Delete
### Before
![image](https://user-images.githubusercontent.com/80308830/226428100-5247ffce-b0a1-4ac3-99e2-a8cc4e7713dd.png)
### Deleting 
clicking on delete button 
### After
![image](https://user-images.githubusercontent.com/80308830/226428235-22038403-7d59-42d9-b1e0-f4ef544fb039.png)
### Pop up

## RENAME

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
screenshot

## Admin Dashboard
![image](https://user-images.githubusercontent.com/80308830/226423771-aa566b35-72cf-452f-9c76-e058819bac83.png)
<br>
For each page in the navigation bar, we can update, add, or delete to the database. Here, we show only for the admin-resident page.


## Resident HomePage
ss



# Contribution 
## G1
1. Kareena
2. Bhavini
3. Hamsini
4. Rajesh
5. Gnana Sai
6. Chaitanya
7. Rishab

## G2 
1. Sriman 
2. Manish 
3. Sunny 
4. Siva Sai 
5. Karthik
