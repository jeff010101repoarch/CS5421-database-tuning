DROP TABLE IF EXISTS PART CASCADE;
CREATE TABLE PART (

	P_PARTKEY		SERIAL PRIMARY KEY,
	P_NAME			VARCHAR(55),
	P_MFGR			CHAR(25),
	P_BRAND			CHAR(10),
	P_TYPE			VARCHAR(25),
	P_SIZE			INTEGER,
	P_CONTAINER		CHAR(10),
	P_RETAILPRICE	DECIMAL,
	P_COMMENT		VARCHAR(23)
);

DROP TABLE IF EXISTS SUPPLIER CASCADE;
CREATE TABLE SUPPLIER (
	S_SUPPKEY		SERIAL PRIMARY KEY,
	S_NAME			CHAR(25),
	S_ADDRESS		VARCHAR(40),
	S_NATIONKEY		BIGINT NOT NULL, -- references N_NATIONKEY
	S_PHONE			CHAR(15),
	S_ACCTBAL		DECIMAL,
	S_COMMENT		VARCHAR(101)
);

DROP TABLE IF EXISTS PARTSUPP CASCADE;
CREATE TABLE PARTSUPP (
	PS_PARTKEY		BIGINT NOT NULL, -- references P_PARTKEY
	PS_SUPPKEY		BIGINT NOT NULL, -- references S_SUPPKEY
	PS_AVAILQTY		INTEGER,
	PS_SUPPLYCOST	DECIMAL,
	PS_COMMENT		VARCHAR(199),
	PRIMARY KEY (PS_PARTKEY, PS_SUPPKEY)
);

DROP TABLE IF EXISTS CUSTOMER CASCADE;
CREATE TABLE CUSTOMER (
	C_CUSTKEY		SERIAL PRIMARY KEY,
	C_NAME			VARCHAR(25),
	C_ADDRESS		VARCHAR(40),
	C_NATIONKEY		BIGINT NOT NULL, -- references N_NATIONKEY
	C_PHONE			CHAR(15),
	C_ACCTBAL		DECIMAL,
	C_MKTSEGMENT	CHAR(10),
	C_COMMENT		VARCHAR(117)
);

DROP TABLE IF EXISTS ORDERS CASCADE;
CREATE TABLE ORDERS (
	O_ORDERKEY		SERIAL PRIMARY KEY,
	O_CUSTKEY		BIGINT NOT NULL, -- references C_CUSTKEY
	O_ORDERSTATUS	CHAR(1),
	O_TOTALPRICE	DECIMAL,
	O_ORDERDATE		DATE,
	O_ORDERPRIORITY	CHAR(15),
	O_CLERK			CHAR(15),
	O_SHIPPRIORITY	INTEGER,
	O_COMMENT		VARCHAR(79)
);

DROP TABLE IF EXISTS LINEITEM CASCADE;
CREATE TABLE LINEITEM (
	L_ORDERKEY		BIGINT NOT NULL, -- references O_ORDERKEY
	L_PARTKEY		BIGINT NOT NULL, -- references P_PARTKEY (compound fk to PARTSUPP)
	L_SUPPKEY		BIGINT NOT NULL, -- references S_SUPPKEY (compound fk to PARTSUPP)
	L_LINENUMBER	INTEGER,
	L_QUANTITY		DECIMAL,
	L_EXTENDEDPRICE	DECIMAL,
	L_DISCOUNT		DECIMAL,
	L_TAX			DECIMAL,
	L_RETURNFLAG	CHAR(1),
	L_LINESTATUS	CHAR(1),
	L_SHIPDATE		DATE,
	L_COMMITDATE	DATE,
	L_RECEIPTDATE	DATE,
	L_SHIPINSTRUCT	CHAR(25),
	L_SHIPMODE		CHAR(10),
	L_COMMENT		VARCHAR(44),
	PRIMARY KEY (L_ORDERKEY, L_LINENUMBER)
);

DROP TABLE IF EXISTS NATION CASCADE;
CREATE TABLE NATION (
	N_NATIONKEY		SERIAL PRIMARY KEY,
	N_NAME			CHAR(25),
	N_REGIONKEY		BIGINT NOT NULL,  -- references R_REGIONKEY
	N_COMMENT		VARCHAR(152)
);

DROP TABLE IF EXISTS REGION CASCADE;
CREATE TABLE REGION (
	R_REGIONKEY	SERIAL PRIMARY KEY,
	R_NAME		CHAR(25),
	R_COMMENT	VARCHAR(152)
);


----- Copy the tbl file to /tmp/
COPY customer FROM 'C:\Users\User\OneDrive\NUS\course\CS5421\assigment\project4\TPCH Project\TPCH Project\table\table\customer.tbl' WITH DELIMITER '|';
COPY lineitem FROM 'C:\Users\User\OneDrive\NUS\course\CS5421\assigment\project4\TPCH Project\TPCH Project\table\table\lineitem.tbl' WITH DELIMITER '|';
COPY nation FROM 'C:\Users\User\OneDrive\NUS\course\CS5421\assigment\project4\TPCH Project\TPCH Project\table\table\nation.tbl' WITH DELIMITER '|';
COPY orders FROM 'C:\Users\User\OneDrive\NUS\course\CS5421\assigment\project4\TPCH Project\TPCH Project\table\table\orders.tbl' WITH DELIMITER '|';
COPY part FROM 'C:\Users\User\OneDrive\NUS\course\CS5421\assigment\project4\TPCH Project\TPCH Project\table\table\part.tbl' WITH DELIMITER '|';
COPY partsupp FROM 'C:\Users\User\OneDrive\NUS\course\CS5421\assigment\project4\TPCH Project\TPCH Project\table\table\partsupp.tbl' WITH DELIMITER '|';
COPY region FROM 'C:\Users\User\OneDrive\NUS\course\CS5421\assigment\project4\TPCH Project\TPCH Project\table\table\region.tbl' WITH DELIMITER '|';
COPY supplier FROM 'C:\Users\User\OneDrive\NUS\course\CS5421\assigment\project4\TPCH Project\TPCH Project\table\table\supplier.tbl' WITH DELIMITER '|';




----- CREATE CUSTOMER
DROP TABLE IF EXISTS DIM_CUSTOMER CASCADE;
CREATE TABLE DIM_CUSTOMER (
	C_CUSTKEY		SERIAL PRIMARY KEY,
	C_NAME			VARCHAR(25),
	C_ADDRESS		VARCHAR(40),
	C_NATION		CHAR(25),
	C_REGION		CHAR(25),
	C_PHONE			CHAR(15),
	C_MKTSEGMENT	CHAR(10)
);

INSERT INTO DIM_CUSTOMER 
SELECT cu.c_custkey, cu.c_name, cu.c_address, n.n_name, r.r_name, cu.c_phone, cu.c_mktsegment
FROM CUSTOMER cu, NATION n, REGION r 
WHERE cu.c_nationkey = n.n_nationkey AND n.n_regionkey = r.r_regionkey;

----- CREATE SUPPLIER
DROP TABLE IF EXISTS DIM_SUPPLIER CASCADE;
CREATE TABLE DIM_SUPPLIER (
	S_SUPPKEY		SERIAL PRIMARY KEY,
	S_NAME			CHAR(25),
	S_ADDRESS		VARCHAR(40),
	S_NATION		CHAR(25),
	S_REGION		CHAR(25),
	S_PHONE			CHAR(15)
);

INSERT INTO DIM_SUPPLIER 
SELECT s.s_suppkey, s.s_name, s.s_address, n.n_name, r.r_name, s.s_phone
FROM SUPPLIER s, NATION n, REGION r 
WHERE s.s_nationkey = n.n_nationkey AND n.n_regionkey = r.r_regionkey;

----- CREATE PART
DROP TABLE IF EXISTS DIM_PART CASCADE;
CREATE TABLE DIM_PART (

	P_PARTKEY		SERIAL PRIMARY KEY,
	P_NAME			VARCHAR(55),
	P_MFGR			CHAR(25),
	P_BRAND			CHAR(10),
	P_TYPE			VARCHAR(25),
	P_SIZE			INTEGER,
	P_CONTAINER		CHAR(10)
);

INSERT INTO DIM_PART
SELECT p_partkey, p_name, p_mfgr, p_brand, p_type, p_size, p_container
FROM PART;

----- CREATE PART
DROP TABLE IF EXISTS DIM_DATE CASCADE;
CREATE TABLE DIM_DATE (

	P_PARTKEY		SERIAL PRIMARY KEY,
	P_NAME			VARCHAR(55),
	P_MFGR			CHAR(25),
	P_BRAND			CHAR(10),
	P_TYPE			VARCHAR(25),
	P_SIZE			INTEGER,
	P_CONTAINER		CHAR(10)
);

---- CREATE FACT LINEORDER
DROP TABLE IF EXISTS FACT_LINEORDER CASCADE;
CREATE TABLE FACT_LINEORDER (
	LO_ORDERKEY		BIGINT NOT NULL, -- references O_ORDERKEY
	LO_LINENUMBER	INTEGER,	
	LO_CUSTKEY		BIGINT NOT NULL, -- references C_CUSTKEY
	LO_PARTKEY		BIGINT NOT NULL, -- references P_PARTKEY (compound fk to PARTSUPP)
	LO_SUPPKEY		BIGINT NOT NULL, -- references S_SUPPKEY (compound fk to PARTSUPP)
	LO_ORDERDATE		DATE,
	LO_ORDERPRIORITY	CHAR(15),
	LO_SHIPPRIORITY	INTEGER,
	LO_QUANTITY		DECIMAL,
	LO_EXTENDEDPRICE	DECIMAL,
	LO_ORDTOTALPRICE	DECIMAL,
	LO_DISCOUNT		DECIMAL,
	LO_REVENUE		DECIMAL,
	LO_SUPPLYCOST	DECIMAL,
	LO_TAX			DECIMAL,
	LO_SHIPDATE 	DATE,
	LO_COMMITDATE	DATE,
	LO_RECEIPTDATE	DATE,
	LO_SHIPMODE		CHAR(10),
	PRIMARY KEY (LO_ORDERKEY, LO_LINENUMBER)
);
 
INSERT INTO FACT_LINEORDER 
SELECT l.l_orderkey, l.l_linenumber, c.c_custkey, l.l_partkey, l.l_suppkey, o.o_orderdate, o.o_orderpriority, o.o_shippriority, l.l_quantity, l.l_extendedprice, 
       o.o_totalprice, l.l_discount, (l.l_extendedprice * (100 - l.l_discount)) / 100, ps.ps_supplycost, l.l_tax, l.l_shipdate, l.l_commitdate, l.l_receiptdate, l.l_shipmode
FROM LINEITEM l, ORDERS o, CUSTOMER c, PART p, SUPPLIER s, PARTSUPP ps
WHERE o.o_orderkey = l.l_orderkey and o.o_custkey = c.c_custkey and l.l_partkey = p.p_partkey and l.l_suppkey = s.s_suppkey and l.l_partkey = ps.ps_partkey and l.l_suppkey = ps.ps_suppkey;



---- CREATE DIM DATE
DROP TABLE if exists DIM_DATE;

CREATE TABLE DIM_DATE
(
  d_date_dim_id              INT NOT NULL PRIMARY KEY,
  d_date_actual              DATE NOT NULL,
  d_epoch                    BIGINT NOT NULL,
  d_day_suffix               VARCHAR(4) NOT NULL,
  d_day_name                 VARCHAR(9) NOT NULL,
  d_day_of_week              INT NOT NULL,
  d_day_of_month             INT NOT NULL,
  d_day_of_quarter           INT NOT NULL,
  d_day_of_year              INT NOT NULL,
  d_week_of_month            INT NOT NULL,
  d_week_of_year             INT NOT NULL,
  d_week_of_year_iso         CHAR(10) NOT NULL,
  d_month_actual             INT NOT NULL,
  d_month_name               VARCHAR(9) NOT NULL,
  d_month_name_abbreviated   CHAR(3) NOT NULL,
  d_quarter_actual           INT NOT NULL,
  d_quarter_name             VARCHAR(9) NOT NULL,
  d_year_actual              INT NOT NULL,
  d_first_day_of_week        DATE NOT NULL,
  d_last_day_of_week         DATE NOT NULL,
  d_first_day_of_month       DATE NOT NULL,
  d_last_day_of_month        DATE NOT NULL,
  d_first_day_of_quarter     DATE NOT NULL,
  d_last_day_of_quarter      DATE NOT NULL,
  d_first_day_of_year        DATE NOT NULL,
  d_last_day_of_year         DATE NOT NULL,
  d_mmyyyy                   CHAR(6) NOT NULL,
  d_mmddyyyy                 CHAR(10) NOT NULL,
  d_weekend_indr             BOOLEAN NOT NULL
);

CREATE INDEX d_date_date_actual_idx
  ON dim_date(d_date_actual);
  
INSERT INTO dim_date
SELECT TO_CHAR(datum,'yyyymmdd')::INT AS d_date_dim_id,
       datum AS d_date_actual,
       EXTRACT(epoch FROM datum) AS d_epoch,
       TO_CHAR(datum,'fmDDth') AS d_day_suffix,
       TO_CHAR(datum,'Day') AS d_day_name,
       EXTRACT(isodow FROM datum) AS d_day_of_week,
       EXTRACT(DAY FROM datum) AS d_day_of_month,
       datum - DATE_TRUNC('quarter',datum)::DATE +1 AS d_day_of_quarter,
       EXTRACT(doy FROM datum) AS d_day_of_year,
       TO_CHAR(datum,'W')::INT AS d_week_of_month,
       EXTRACT(week FROM datum) AS d_week_of_year,
       TO_CHAR(datum,'YYYY"-W"IW-') || EXTRACT(isodow FROM datum) AS d_week_of_year_iso,
       EXTRACT(MONTH FROM datum) AS d_month_actual,
       TO_CHAR(datum,'Month') AS d_month_name,
       TO_CHAR(datum,'Mon') AS d_month_name_abbreviated,
       EXTRACT(quarter FROM datum) AS d_quarter_actual,
       CASE
         WHEN EXTRACT(quarter FROM datum) = 1 THEN 'First'
         WHEN EXTRACT(quarter FROM datum) = 2 THEN 'Second'
         WHEN EXTRACT(quarter FROM datum) = 3 THEN 'Third'
         WHEN EXTRACT(quarter FROM datum) = 4 THEN 'Fourth'
       END AS d_quarter_name,
       EXTRACT(isoyear FROM datum) AS d_year_actual,
       datum +(1 -EXTRACT(isodow FROM datum))::INT AS d_first_day_of_week,
       datum +(7 -EXTRACT(isodow FROM datum))::INT AS d_last_day_of_week,
       datum +(1 -EXTRACT(DAY FROM datum))::INT AS d_first_day_of_month,
       (DATE_TRUNC('MONTH',datum) +INTERVAL '1 MONTH - 1 day')::DATE AS d_last_day_of_month,
       DATE_TRUNC('quarter',datum)::DATE AS d_first_day_of_quarter,
       (DATE_TRUNC('quarter',datum) +INTERVAL '3 MONTH - 1 day')::DATE AS d_last_day_of_quarter,
       TO_DATE(EXTRACT(isoyear FROM datum) || '-01-01','YYYY-MM-DD') AS d_first_day_of_year,
       TO_DATE(EXTRACT(isoyear FROM datum) || '-12-31','YYYY-MM-DD') AS d_last_day_of_year,
       TO_CHAR(datum,'mmyyyy') AS d_mmyyyy,
       TO_CHAR(datum,'mmddyyyy') AS d_mmddyyyy,
       CASE
         WHEN EXTRACT(isodow FROM datum) IN (6,7) THEN TRUE
         ELSE FALSE
       END AS d_weekend_indr
FROM (SELECT '1970-01-01'::DATE+ SEQUENCE.DAY AS datum
      FROM GENERATE_SERIES (0,29219) AS SEQUENCE (DAY)
      GROUP BY SEQUENCE.DAY) DQ
ORDER BY 1;


