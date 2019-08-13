import argparse
import subprocess
import random
from sqlalchemy.orm import sessionmaker
import ast
import time
from db_connect import get_conn

parser = argparse.ArgumentParser()
parser.add_argument('E', type = int, help = 'number of exchange transactions in a process')
parser.add_argument('P', type = int, help = 'number of processes')
parser.add_argument('I', help = 'isolation level')
args = parser.parse_args()

processes = []
for i in xrange(0, args.P):
    processes.append(subprocess.Popen(['python', 'c:/Users/User/OneDrive/NUS/course/CS5421/assigment/project5/run_exchanges.py', str(args.E), args.I], stdout=subprocess.PIPE)) ##MODIFIED

for process in processes:
    process.wait()

time = []
for process in processes:
    time.append(ast.literal_eval(process.communicate()[0]))

print float(sum(time)) / len(time)

