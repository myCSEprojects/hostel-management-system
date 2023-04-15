use hostelmng;
drop USER 'admin'@'localhost';
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'Password@1234';
GRANT all privileges on hostelmng.* TO 'admin'@'localhost';

-- drop user 'public'@'localhost';
CREATE USER 'public'@'localhost' IDENTIFIED BY 'Passoword@public1234';

-- granting permissions to public user 
GRANT SELECT ON  CARETAKER TO "public"@'localhost';
GRANT SELECT ON CARETAKER_PHONE TO "public"@'localhost';
GRANT SELECT ON public_hostelview TO "public"@'localhost';
GRANT SELECT ON OUTLET TO "public"@'localhost';
GRANT SELECT ON OUTLET_PHONE TO "public"@'localhost';
GRANT SELECT ON OUTLET_OWNER_PHONE TO "public"@'localhost';
GRANT SELECT ON ROOM TO "public"@'localhost';
GRANT SELECT ON public_currentAllocation TO "public"@'localhost';


-- drop user 'resident'@'localhost';
CREATE USER 'resident'@'localhost' IDENTIFIED BY 'Password@resident1234';

-- granting permissions to resident user
GRANT SELECT ON RESIDENT TO 'resident'@'localhost';
GRANT SELECT ON RESIDENT_PHONE TO 'resident'@'localhost';
GRANT SELECT ON ENROLLED_IN TO 'resident'@'localhost';
GRANT SELECT,UPDATE ON users TO 'resident'@'localhost';
GRANT SELECT ON ALLOCATION TO 'resident'@'localhost';
GRANT SELECT ON CURRENT_ALLOCATION TO 'resident'@'localhost';
GRANT SELECT ON HOSTEL TO 'resident'@'localhost';
GRANT SELECT ON CARETAKER TO 'resident'@'localhost';
GRANT SELECT ON ROOM TO 'resident'@'localhost';
GRANT SELECT ON CARETAKER_PHONE TO 'resident'@'localhost';
