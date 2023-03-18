SELECT * FROM hostelmng.current_allocation;

select * from current_allocation where room_no%25 = 0 ;

select sum(occupied) from room where occupied > 1  and room_type = "triple";

DELETE FROM CARETAKER WHERE CARETAKER_ID = 10000002;
SELECT * FROM CARETAKER_PHONE;


delete from room where occupied > 1  and room_type = "triple";

select sum(occupied) from room ;

SELECT COUNT(*) FROM ALLOCATION ;
delete from current_allocation where room_no >= 200 ;
SELECT COUNT(*) FROM ALLOCATION;

SELECT * from
(SELECT resident_id, CONCAT(first_name, " ", last_name) as full_name
FROM CURRENT_ALLOCATION NATURAL JOIN RESIDENT) as display
NATURAL JOIN
(SELECT *
FROM CURRENT_ALLOCATION NATURAL JOIN RESIDENT) as form;

Select DATE('2023-12-12');
CALL DEALLOCATE(20000002, STR_TO_DATE('2023-12-12', '%Y-%m-%d'));

SELECT * FROM ALLOCATION WHERE resident_id = 20000002;
SELECT * FROM CURRENT_ALLOCATION WHERE resident_id = 20000002;
