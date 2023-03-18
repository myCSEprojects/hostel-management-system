
-- Create a trigger that updates a record in "orders" table when a record is deleted from "customers" table
delimiter //
CREATE TRIGGER update_occupancy
AFTER DELETE ON CURRENT_ALLOCATION
FOR EACH ROW
Begin
  UPDATE ROOM SET occupied = occupied-1 WHERE room_no = OLD.room_no AND hostel_name = OLD.hostel_name ;
end //
delimiter;

delimiter //
CREATE TRIGGER on_entry
AFTER INSERT ON  CURRENT_ALLOCATION
FOR EACH ROW
BEGIN
  UPDATE ROOM
  SET occupied = occupied +1  
  WHERE ROOM.room_no = NEW.room_no and ROOM.hostel_name = NEW.hostel_name;
END //
delimiter;

delimiter //
CREATE TRIGGER deallocation
AFTER DELETE ON CURRENT_ALLOCATION
FOR EACH ROW
Begin
	DECLARE exit_date DATE;
	set exit_date = NULL;
	INSERT INTO ALLOCATION  (semester, year, resident_id, room_no, hostel_name, entry_date, exit_date, payment_status, due_amount, due_status, payment_amount)
	values(old.semester, old.year, old.resident_id, old.room_no, old.hostel_name, old.entry_date, exit_date, old.payment_status, old.due_amount, old.due_status, old.payment_amount);
end//
delimiter;

drop procedure DEALLOCATE;
DELIMITER //

CREATE procedure DEALLOCATE(IN resident_id numeric(8), IN exit_date DATE)
Begin
	DELETE FROM CURRENT_ALLOCATION WHERE CURRENT_ALLOCATION.resident_id = resident_id;
    UPDATE ALLOCATION
    SET ALLOCATION.exit_date = exit_date
	WHERE ALLOCATION.resident_id = resident_id and ALLOCATION.exit_date is NULL;
end//

DELIMITER ;

