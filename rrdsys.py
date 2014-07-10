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
        try:
            if l[1] == 'all':
                sys_load[l[1]] = { 'usr': l[2], 'nice': l[3], 'sys': l[4],
                'iowait': l[5], 'soft': l[7], 'idle': l[11] }
            elif l[1] == 'CPU':
                continue
            else:
                sys_load[l[1]] = { 'usr': l[2], 'nice': l[3], 'sys': l[4],
                'iowait': l[5], 'soft': l[7], 'idle': l[11] }
        except:
            continue
    f.close()
    os.remove(cpu_file)

    return sys_load

# Get system output. 
# !!! Will be removed later !!!
def get_cmd(cmd):
    return os.popen(cmd).read()

# End of system
###############