import os
import re
from os import listdir
import os.path
from os.path import join

# System
########

# Get network interfaces list
def interfaces():
    sys_path = '/sys/class/net'
    ifaces = [ f for f in listdir(sys_path) if join(sys_path, f) ]
    ifaces.remove('lo')
    return ifaces


# Get traffic values
def get_traf():
    ifaces = interfaces()
    traffic = {}

    # Parsing /proc/net/dev
    proc = '/proc/net/dev'
    f = open(proc, "r")
    for line in f.readlines():
        bytes = line.split()
        for i in ifaces:
            net = bytes[0]
            net = net[:-1]
            if i == net:
                traffic[i] = { 'in': bytes[1], 'out': bytes[9] }
    return traffic


# Get memory function
def get_mem():
    proc = '/proc/meminfo'
    mem = {}
    f = open(proc, "r")
    for line in f.readlines():
        memory = line.split()
        m = memory[0][:-1]
        if m == 'MemTotal':
            mem['total'] = memory[1]
        elif m == 'MemFree':
            mem['free'] = memory[1]
        elif m == 'Buffers':
            mem['buffers'] = memory[1]
        elif m == 'Cached':
            mem['cached'] = memory[1]
        elif m == 'SwapCached':
            mem['swap'] = memory[1]

    mem['used'] = (int( mem['total'] ) - int( mem['free'] )) - ( int(mem['cached']) - int(mem['buffers']) )
    return mem


# Get phisicals CPU
def cpus():
    proc = '/proc/cpuinfo'
    f = open(proc, "r")

    # Physical id counter
    phys = 1
    for line in f.readlines():
        l = line.split(':')
        name = l[0][:-1]
        if name == 'physical id':
            value = l[1]
            if int(value) >= phys:
                phys = phys + 1
    f.close()

    return phys


# Get CPU cores
def cpu_cores():
    proc = '/proc/cpuinfo'
    f = open(proc, 'r')

    # Cores counter
    cores = 1
    for line in f.readlines():
        l = line.split(':')
        name = re.split(r'(.+)\s\s+', l[0])
        # Exception
        try:
            if name[1] == 'core id':
                value = l[1]
                if int(value) >= cores:
                    cores = cores + 1
        except:
            continue
    f.close()

    return cores


# Get load average
def cpu_load():
    cpu_file = '/tmp/cpu_load'
    stat_cmd = 'mpstat -P ALL'
    
    # Write command output to file
    w = open(cpu_file, "w")
    w.write( get_cmd(stat_cmd) )
    w.close()

    # Vars
    sys_load = {}
    # Read file
    f = open(cpu_file, 'r')
    for line in f.readlines():
        l = line.split()
        
        # Exception
        c = 2
        while c < 12: 
            try:
                # I don't understand what is it. 2Iknups: Try to comment the code, pls :)
                # YOU_COMMENTS_HERE
                num = l[c].split(',')
                if l[c] != 'all':
                    l[c] = int(num[0]) 
                if l[2] == 'all':
                    sys_load['all'] = { 'usr': int(float(l[3])*100), 'nice': int(float(l[4])*100), 'sys': int(float(l[5])*100),
                    'iowait': int(float(l[6])*100), 'soft': int(float(l[7])*100), 'idle': int(float(l[11])*100)} 
                elif l[2] == 'CPU': 
                    continue 
                else: 
                    print(l[2])
                    sys_load[str(l[2])] = { 'usr': int(float(l[3])*100), 'nice': int(float(l[4])*100), 'sys': int(float(l[5])*100), 
                    'iowait': int(float(l[6])*100), 'soft': int(float(l[7])*100), 'idle': int(float(l[11])*100)} 
  
                c = c + 1 
            except: 
                c = c + 1 
 
    
    f.close()
    # Remove output file
    os.remove(cpu_file)
    print sys_load

    return sys_load


# Get system output. 
# !!! Will be removed later !!!
def get_cmd(cmd):
    return os.popen(cmd).read()

# End of system
###############
