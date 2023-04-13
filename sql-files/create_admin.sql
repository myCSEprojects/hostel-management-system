use hostelmng;
drop USER 'admin'@'localhost';
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'Password@1234';
GRANT all privileges on hostelmng.* TO 'admin'@'localhost';
