import numpy as np
import json


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
            print("might be diverging")
            return True, n 
    return False, i



def c_checker_arr(x, intrvl):
    i=0
    while (c_checker(x[i])[0]==False) & (i<intrvl-1):
        i = i+1
    if i==intrvl-1:
        print("done from ", x[0], " to ", x[-1])
    else:
        print("YO number is:", x[i], "and loop at: ", c_checker(x[i])[1])
        return 0, x[i]

        
###Routine
while(1):
    # load data

    f = open("progress.json","r")
    dat = json.loads(f.read())
    current_no = dat["Current"]
    intrvl = dat["Interval"]
    f.close()

    # execute  collatz test

    x_arr = np.arange(current_no, current_no+intrvl)

    run = c_checker_arr(x_arr, intrvl)
    
    if run[0] == 0:
        f = open("status.txt", "w")
        f.write("motherfucking loop or divergence at " + str(x[i]))
        break

    current_new = current_no+intrvl-1


    # save data


    dict = {'Start' : 2**120, 'Interval' : 2**16, 'Current' : current_new}

    jsondat = json.dumps(dict)

    f = open("progress.json","w") # w for write, r for read

    f.write(jsondat)

    f.close()
