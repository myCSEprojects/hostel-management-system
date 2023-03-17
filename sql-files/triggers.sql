DELETE FROM CARETAKER WHERE CARETAKER_ID = 10000002;
SELECT * FROM CARETAKER_PHONE;


-- Create a trigger that updates a record in "orders" table when a record is deleted from "customers" table
delimiter //
CREATE TRIGGER update_occupancy
AFTER DELETE ON CURRENT_ALLOCATION
FOR EACH ROW
Begin
  UPDATE ROOM SET occupied = occupied-1 WHERE room_no = OLD.room_no AND hostel_name = OLD.hostel_name ;
end; 

delimiter //
CREATE TRIGGER on_entry
AFTER INSERT ON  current_allocation
FOR EACH ROW
BEGIN
  UPDATE room
  SET occupied = occupied +1  
  WHERE room.room_no = NEW.room_no and room.hostel_name = NEW.hostel_name;
END;


delimiter //

CREATE TRIGGER deallocation
AFTER DELETE ON CURRENT_ALLOCATION
FOR EACH ROW
Begin
  DECLARE exit_date DATE;
  set exit_date = date(NOW());
 INSERT INTO ALLOCATION  (semester, year, resident_id, room_no, hostel_name, entry_date, exit_date, payment_status, due_amount, due_status, payment_amount)
 values(old.semester, old.year, old.resident_id, old.room_no, old.hostel_name, old.entry_date, exit_date, old.payment_status, old.due_amount, old.due_status, old.payment_amount);
end; 


