--1
CREATE or REPLACE FUNCTION test(Q TEXT, N INTEGER) RETURNs FLOAT AS 
$$
DECLARE
time_single FLOAT :=0.0;
time_total FLOAT :=0.0;
i INTEGER :=0;
plan_json JSON;
BEGIN
	FOR i IN 1..N
	LOOP
		EXECUTE 'EXPLAIN(ANALYZE TRUE, TIMING, FORMAT JSON)' || Q INTO plan_json;
		SELECT plan_json -> 0 ->'Execution Time' INTO time_single;
		--SELECT 1 INTO time_single;
		time_total := time_total + time_single;
	END LOOP;
	RETURN time_total/N;
END;
$$ LANGUAGE plpgsql;

--2.1
SELECT e.empid, e.lname
FROM employee e FULL JOIN payroll p
ON e.empid = p.empid
WHERE p.salary = 199170 
AND e.lname IS NOT NULL;

--2.2
SELECT e.empid, e.lname
FROM employee e
WHERE EXISTS (
	SELECT *
	FROM payroll p
	WHERE e.empid = p.empid
	AND p.salary = 199170);
	
--2.3
SELECT e.empid, e.lname
FROM employee e
WHERE e.empid IN (
	SELECT p.empid
	FROM payroll p
	WHERE p.salary = 199170);
	
--2.4
SELECT e.empid, e.lname
FROM employee e, (
					SELECT empid
					FROM payroll p
					WHERE p.salary = 199170
				) temp
WHERE  e.empid = temp.empid;

--2.5
SELECT e.empid, e.lname
FROM employee e
WHERE NOT EXISTS (
	SELECT *
	FROM payroll p
	WHERE e.empid = p.empid
	AND p.salary <> 199170);
	
--3
SELECT e.empid, e.lname
FROM employee e
WHERE  e.empid NOT IN(
						SELECT empid
						FROM payroll p
						WHERE p.salary <> 199170
					);