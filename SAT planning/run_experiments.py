#https://linuxhandbook.com/execute-shell-command-python/

import os
cmd1=''
execsem=''
pgcons=''
pg=''
benchmarks=['miconic','pipesworld','rovers']
for benchm in benchmarks:
    for j in range(2):
        # FOR parallel and no fluent or reachable
        if j==int(0):
            execsem='serial'
        elif j==int(1):
            execsem='parallel'
        for k in range(4):
            # FOR constraints. NONE, fmutec,reachable,both
            if k==int(0):
                pgcons='-p false'
            elif k==int(1):
                pgcons="-l fmutex -p true"
                pg='fmutex'
            elif k == int(2):
                pgcons = "-l reachable -p true"
                pg = 'reachable'
            elif k == int(3):
                pgcons = "-l both -p true"
                pg='both'
            for i in range(1,11):
                if i<int(10):

                    cmd1="timeout 300 python3 -u planner.py benchmarks/{}/domain.pddl benchmarks/{}/problem0{}.pddl {}_temp{}{} 1:30:1 -x {}  {} -q ramp | tee -a {}-1-10.log".format(benchm,benchm,i,benchm,execsem,pg,execsem,pgcons,benchm)
                    os.system(cmd1)
                else:
                    cmd1 = "timeout 300 python3 -u planner.py benchmarks/{}/domain.pddl benchmarks/{}/problem{}.pddl {}_temp{}{} 1:30:1 -x {}  {} -q ramp | tee -a {}-1-10.log".format(benchm,benchm,i,benchm,execsem,pg,execsem,pgcons,benchm)
                    os.system(cmd1)

# using -a option of tee commmand to append all the entries of a problem otherwise it was just adding the latest ones.