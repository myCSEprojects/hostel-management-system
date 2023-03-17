SELECT * FROM hostelmng.current_allocation;

select * from current_allocation where room_no%25 = 0 ;

select sum(occupied) from room where occupied > 1  and room_type = "triple";



delete from room where occupied > 1  and room_type = "triple";

select sum(occupied) from room ;

SELECT COUNT(*) FROM ALLOCATION ;
delete from current_allocation where room_no >= 200 ;
SELECT COUNT(*) FROM ALLOCATION;


