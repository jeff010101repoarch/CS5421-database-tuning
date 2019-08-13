import argparse
from sqlalchemy.orm import sessionmaker
import subprocess
import ast
from db_connect import get_conn

## Argument parser to take the parameters from the command line
## Example on how to run: python run_experiments.py 100 100 100 READ_COMMITTED
# parser = argparse.ArgumentParser()
# parser.add_argument('S', type = int, help = 'number of sums')
# parser.add_argument('E', type = int, help = 'number of exchange transactions in a process')
# parser.add_argument('P', type = int, help = 'number of process')
# parser.add_argument('I', help = 'isolation level')
# args = parser.parse_args()
S = 100
I = ["SERIALIZABLE"]#["READ_UNCOMMITTED","READ_COMMITTED","REPEATABLE_READ","SERIALIZABLE"]
cro = []
time_r = []

for P in xrange(10,110,10):
    E = int(2000/P)
    cro_sub = []
    time_r_sub = []
    for j in I:
        
        cro_sub2 = []
        time_r_sub2 = []
        for i in xrange(0,20):
            print j, E, P, i
            ## Create engine
            engine = get_conn()
            Session = sessionmaker(bind=engine.execution_options(isolation_level=j, autocommit=True))
            sess = Session() 

            ## Calculate the correct sum before applying the function
            p0 = subprocess.Popen(['python', 'c:/Users/User/OneDrive/NUS/course/CS5421/assigment/project5/run_sums.py', str(1), j], stdout=subprocess.PIPE)
            correct_sum = ast.literal_eval(p0.communicate()[0])[0]
            ## Create subprocess to run the transactions paralelly
            p1 = subprocess.Popen(['python', 'c:/Users/User/OneDrive/NUS/course/CS5421/assigment/project5/run_sums.py', str(S), j], stdout=subprocess.PIPE)

            p2 = subprocess.Popen(['python', 'c:/Users/User/OneDrive/NUS/course/CS5421/assigment/project5/run_all_exchanges.py', str(E), str(P), j], stdout=subprocess.PIPE)

            p1.wait()

            p2.wait()

            ## Check the new sums and calculate correctness
            sums = ast.literal_eval(p1.communicate()[0])
            time = ast.literal_eval(p2.communicate()[0])
            good = [x for x in sums if abs(x - correct_sum) < 0.01]
            Correctness = float(len(good)) / S
            print 'Correctness:', float(len(good)) / S
            print 'Time:', time 
            cro_sub2.append(Correctness)
            time_r_sub2.append(time)
        print j,cro_sub2, time_r_sub2
        cro_sub.append(cro_sub2)
        time_r_sub.append(time_r_sub2)
    print cro_sub, time_r_sub
    cro.append(cro_sub)
    time_r.append(time_r_sub)
        

print cro
print time_r
