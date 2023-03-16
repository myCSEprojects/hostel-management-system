# Using the hostel management database
use hostelmng;

DROP table users;
# creating the users database
CREATE TABLE users (id NUMERIC(8) NOT NULL, key_ BINARY(64) NOT NULL, PRIMARY KEY (id));

INSERT INTO users (id, key_) VALUES (20000000, "c10be01f09b75742b3a230fdd3c9cbfde2b2f08ec6427132804cd6375e1e4021b778e0e794635178ab3f4dabc72118f22563c24f4abe72587e10b52671c9dad2");