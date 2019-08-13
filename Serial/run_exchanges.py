import argparse
from sqlalchemy.orm import sessionmaker
import time
from db_connect import get_conn
import random

## Argument parser to take the parameters from the command line
## Example on how to run: python run_sums.py 10 READ_COMMITTED
parser = argparse.ArgumentParser()
parser.add_argument('E', type = int, help = 'number of swap')
parser.add_argument('I', help = 'isolation level')
args = parser.parse_args()
#print args.S, args.I

## Execute a sum query and return the results
def exchange(sess):
    ## 1. Get the balance of two random ids
    A_1 = random.randint(1,100000)
    A_2 = random.randint(1,100000)

    V_1 = sess.execute("SELECT ACCOUNT.BALANCE FROM ACCOUNT WHERE ACCOUNT.ID =:A_1",{"A_1":A_1}).scalar()
    V_2 = sess.execute("SELECT ACCOUNT.BALANCE FROM ACCOUNT WHERE ACCOUNT.ID =:A_2",{"A_2":A_2}).scalar()
    ## 2. Swap the value
    sess.execute("UPDATE ACCOUNT SET BALANCE =:V_2 WHERE ACCOUNT.ID =:A_1",{"V_2":V_2,"A_1":A_1})
    sess.execute("UPDATE ACCOUNT SET BALANCE =:V_1 WHERE ACCOUNT.ID =:A_2",{"V_1":V_1,"A_2":A_2})

    sess.commit()

    return 1

## Create S sums operations
def S_sums(sess, E):
    # sums = []
    start = time.time()

    for i in xrange(0, E):
        # while True:
        try:
            exchange(sess)
        except Exception as e:
            # print e
            continue
        # break

    stop = time.time()
    return stop-start

## Create the engine and run the sums
engine = get_conn()
Session = sessionmaker(bind=engine.execution_options(isolation_level=args.I, autocommit=True))
sess = Session()
time = S_sums(sess, args.E)
print time