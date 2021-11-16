import numpy as np
import json
import logging


####### init logging style

#create a logger
logger = logging.getLogger('mylogger')
#set logger level
logger.setLevel(logging.INFO)
#or you can set the following level
#logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('app.log')
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)






####### defs
def cstep(n):
    if n % 2 == 0:
        return n/2
    else:
        return 3*n+1
    
    
def c_checker(n):
    # pastvals=[cstep(maxTest+2**16-3)] a possible test
    pastvals = []
    i=0
    while n > 2: #could just check if ==2**x but thats probably harder
        # idea: log_2 % 1 ==0 as 1.5%1=0.5..
        n = cstep(n)
        if n in pastvals:
            return True, n
        pastvals.append(n)
        i = i+1 
        if i>1e6:
            #print("might be diverging")
            return True, n 
    return False, i


def c_checker_arr(x, intrvl):
    i=0
    while (c_checker(x[i])[0]==False) & (i<intrvl-1):
        i = i+1
    if i==intrvl-1:
        print("done from ", x[0], " to ", x[-1])
        return 1, 1 #return second 1 as default
    else:
        print("YO number is:", x[i], "and loop at: ", c_checker(x[i])[1])
        return 0, x[i]
    

def progress_save(currento, foundno, interval=2**16):
    if foundno == 1:
        logger.info("done from "+ str(currento)+ " to "+ str(currento + interval))
    else:
        logger.critical("motherfucking loop or divergence at " + str(foundno))
        
    dict = {'Start' : 2**120, 'Interval' : interval, 'Current' : currento + interval, "Found_no" : foundno}

    jsondat = json.dumps(dict)

    f = open("progress.json","w") # w for write, r for read

    f.write(jsondat)
    f.close()

      
        
###### Routine
while(1):
    # load data

    f = open("progress.json","r")
    dat = json.loads(f.read())
    current_no = dat["Current"]
    intrvl = dat["Interval"]
    foundno = dat["Found_no"]
    if foundno != 1:
        print("Already found Collatz breaking number in: ", foundno)
        break
    f.close()

    # execute  collatz test

    x_arr = np.arange(current_no, current_no+intrvl+1) #+1 b/c np.arange[1,2]=[1]

    run = c_checker_arr(x_arr, intrvl)
    
    if run[0] == 0:
        progress_save(current_no, run[1], intrvl)
        break
    elif run[0] == 1:
        progress_save(current_no, run[1], intrvl)




