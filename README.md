# Features, Views
## Resident
## Hostel
## -

# Steps
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
### Backend Libraries used
1. Flask(Python)
2. Jinja templating that comes with flask