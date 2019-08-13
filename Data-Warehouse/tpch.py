##### 
## This section imports the necessary classes and methods from the SQLAlchemy library
####
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

######## IMPORTANT! Change this to your metric number for grading
student_no = 'XXXX' 
#########################

#####
## This section creates an engine for the PostgreSQL
## and creates a database session s.
#####
# username = 'postgres'
# password = '1'
# dbname = 'TPCH'
# engine = create_engine('postgres://%s:%s@localhost:5432/%s' % (username, password, dbname))

username = 'postgres'
password = '1'
dbname = 'TPCH'
engine = create_engine('postgres://%s:%s@localhost:5432/%s' % (username, password, dbname))

Session = sessionmaker(bind=engine)
s = Session()

#####
## Query 
#####
query1 = """SELECT LINEITEM.L_ORDERKEY, PART.P_NAME, SUPPLIER.S_NAME, ORDERS.O_ORDERDATE, LINEITEM.L_EXTENDEDPRICE
FROM LINEITEM, ORDERS, CUSTOMER, SUPPLIER, PART
WHERE CUSTOMER.C_NAME = 'Customer#000000001'
AND CUSTOMER.C_CUSTKEY = ORDERS.O_CUSTKEY
AND ORDERS.O_ORDERKEY = LINEITEM.L_ORDERKEY
AND LINEITEM.L_SUPPKEY = SUPPLIER.S_SUPPKEY
AND LINEITEM.L_PARTKEY = PART.P_PARTKEY;"""

s.execute(query1)

query2 = """SELECT SUM(LINEITEM.L_EXTENDEDPRICE) AS SUM_EXPRICE
FROM LINEITEM, ORDERS, CUSTOMER, PART, REGION, NATION
WHERE CUSTOMER.C_CUSTKEY = ORDERS.O_CUSTKEY
AND LINEITEM.L_ORDERKEY = ORDERS.O_ORDERKEY
AND LINEITEM.L_PARTKEY = PART.P_PARTKEY
AND REGION.R_REGIONKEY = NATION.N_REGIONKEY
AND NATION.N_NATIONKEY = CUSTOMER.C_NATIONKEY
AND PART.P_BRAND = 'Brand#13'
GROUP BY CUBE(REGION.R_NAME, CUSTOMER.C_NATIONKEY, CUSTOMER.C_MKTSEGMENT)
ORDER BY SUM_EXPRICE;"""

s.execute(query2)

query3 = """SELECT COUNT(*) AS TOTAL_NUM_LINEORDER,
SUM(LINEITEM.L_EXTENDEDPRICE) AS SUM_EXTENDEDPRICE,
SUM(LINEITEM.L_EXTENDEDPRICE*(1-LINEITEM.L_DISCOUNT)) AS SUM_DISCOUNT_PRICE,
SUM(LINEITEM.L_EXTENDEDPRICE*(1-LINEITEM.L_DISCOUNT)*(1+LINEITEM.L_TAX)) AS sum_DISCOUNT_PRICE_TAX,
AVG(LINEITEM.L_QUANTITY) AS AVG_QUANTITY,
AVG(LINEITEM.L_EXTENDEDPRICE) AS AVG_EXTENDEDPRICE,
AVG(LINEITEM.L_DISCOUNT) AS AVG_DISCOUNT
FROM LINEITEM, ORDERS
WHERE LINEITEM.L_ORDERKEY = ORDERS.O_ORDERKEY
GROUP BY ROLLUP(EXTRACT(YEAR FROM ORDERS.O_ORDERDATE),EXTRACT(MONTH FROM ORDERS.O_ORDERDATE))
ORDER BY EXTRACT(YEAR FROM ORDERS.O_ORDERDATE),EXTRACT(MONTH FROM ORDERS.O_ORDERDATE) ASC;"""

s.execute(query3)


query4 = """SELECT ORDERS.O_ORDERPRIORITY, COUNT(*) AS ORDER_COUNT 
FROM ORDERS WHERE EXISTS 
(SELECT * FROM LINEITEM WHERE LINEITEM.L_ORDERKEY = ORDERS.O_ORDERKEY AND LINEITEM.L_COMMITDATE < LINEITEM.L_RECEIPTDATE)
GROUP BY ORDERS.O_ORDERPRIORITY ORDER BY ORDERS.O_ORDERPRIORITY ASC;"""

s.execute(query4)


s.commit()





