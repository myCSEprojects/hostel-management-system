# Mapping for room types
room_types = {
    "single": 1,
    "double": 2,
    "triple": 3,
}

# Defining the gender types for the residents
gender_types = [
    "F",
    "M",
    "O"
]

# Defining the resident types for the residents
resident_types = [
    "student",
    "visitor",
    "faculty"
]

housekeeping_types = [
    "Bathroom",
    "Room",
    "Corridor"
]

# Blood types for the residents
blood_types = [
    "A+",
    "A-",
    "B+",
    "B-",
    "AB+",
    "AB-",
    "O+",
    "O-",
]

resident_details_field_names = {
    "ID": "resident_id",
    "First Name": "first_name", 
    "Middle Name": "middle_name", 
    "Last Name": "last_name", 
    "Gender": "gender",
    "Blood Group": "blood_group", 
    "Email id": "email_id", 
    "City": "city", 
    "Postal Code": "postal_code",  
    "Resident Type": "resident_type", 
    "Guardian Name" : "Guardian_first_name",
    "Guardian Type": "Guardian_type",
    "Home Contact": "home_contact",

}

resident_current_allocation_field_names = {
    "Semester": "semester", 
    "Year": "year",
    "Hostel Name": "hostel_name", 
    "Room Number": "room_no", 
    "Entry Date": "entry_date", 
    "Payment Status": "payment_status", 
    "Due Amount": "due_amount", 
    "Due Status": "due_status", 
    "Payment Amount": "payment_amount",
}
security_details_field_names = {
    "ID": "security_id",
    "First Name": "first_name", 
    "Middle Name": "middle_name", 
    "Last Name": "last_name",
}

housekeeping_details_field_names = {
    "ID": "housekeeper_id",
    "First Name": "first_name", 
    "Middle Name": "middle_name", 
    "Last Name": "last_name",
    "Gender": "gender",
}

furniture_details_field_names = {
    "ID": "furniture_id",
    "Hostel Name": "hostel_name", 
    "Room Number": "room_no", 
    "Status": "status",
}

hostel_details_field_names = {
    "Hostel Name": "hostel_name",
    "Hostel Contact": "contact", 
    "Energy Consumption": "energy_consumption",
    "Water Consumption": "water_consumption",
    "Caretaker ID": "caretaker_id",
}

housekeeping_current_allocation_field_names = {
    "Hostel Name": "hostel_name", 
    "House Keeping Type": "type"
}

security_current_allocation_field_names = {
    "Hostel Name": "hostel_name", 
    "Start Time": "start_time", 
    "End Time": "end_time",
}

resident_program_field_names = {
    "Program": "program", 
    "Branch": "branch", 
}

resident_history_field_names = {
    "Semester" : "semester",
    "Year" : "year", 
    "Hostel Name" : "hostel_name", 
    "Room Number" : "room_no", 
    "Entry Date" : "entry_date", 
    "Exit Date" : "exit_date", 
    "Payment Status" : "payment_status", 
    "Due Amount" : "due_amount", 
    "Due Status" : "due_status", 
    "Payment Amount" : "payment_amount"
}

room_details_field_names = {
    "Room Number": "room_no",
    "Hostel Name": "hostel_name",
    "Room Type": "room_type",
    "Current occupancy": "occupied",
}
room_current_allocation_field_names = {
    "Semester": "semester",
    "Year": "year",
    "ID": "resident_id",
    "Entry Date": "entry_date",
    "Payment Status": "payment_status",
    "Due Amount": "due_amount",
    "Due Status": "due_status",
    "Payment Amount": "payment_amount",
}

room_allocation_history_field_names = {
    "Semester": "semester",
    "Year": "year",
    "ID": "resident_id",
    "Entry Date": "entry_date",
    "Exit Date": "exit_date",
    "Payment Status": "payment_status",
    "Due Amount": "due_amount",
    "Due Status": "due_status",
    "Payment Amount": "payment_amount",
}

