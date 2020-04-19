#Program uses bluetoothctl to monitor, connect and disconnect devices
#It Does two Things: 
# 1. Auto connects bluetooth if during day hours and you turn on device
# 2. Auto disconnects during night hours
# 3. Auto disconnects if you are not are not using certain programs

from plumbum import local
# Requires yum install python3-devel, i also install using pip3 install psutil --user
import psutil
import time
from datetime import datetime

# Global Variables 
pslist = ["brave", "vlc", "joplin"]
bluetoothdevs = ["70:26:05:61:E7:B2"]
shuthours = [21,22,23,24,1,2,3,4,5]
# Auto connection relies on device being turned on
auto_connect_hours = [8,9,10,11,12,13,14,15,16,17,18,19,20]

# The library didnt work by importing each tool from the import statement above,
#   It did work by importing each bash binary on their own
# Binary Imports
ls = local["ls"]
grep = local["grep"]
cat = local["cat"]
wc = local["wc"]
top = local["top"]
tail = local["tail"]
awk = local["awk"]
sed = local["sed"]
blutoothctl = local["bluetoothctl"]

# Get process info for each service in pslist
def getproc(psname):
    piddic = {}
    piddic.update({psname: []})
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if psname in proc.info["name"]:
            piddic[psname].append(proc.info["pid"])
    if len(piddic[psname]) < 1:
        piddic.pop(psname)
    if len(piddic) != 0:
        return piddic

# Shutdown Blutooth
def blueshut():
    for i in bluetoothdevs:
        # Get connection Status (Not Needed Really but might use more later)
        chain_btinfo = blutoothctl ["info", i] | sed ["-n", "/Connected/p"] | awk ["{print $2}"]
        if "yes" in chain_btinfo():
            chain_btdiscon = blutoothctl ["disconnect", i]
            chain_btdiscon()
            time.sleep(5)

# Auto Connect bluetooth
def blueautoconnect():
    for i in bluetoothdevs:
        chain_btconn = blutoothctl ["connect", i]
        chain_btconn()
        time.sleep(5)

# Check to see if bluetooth device should shut because of time
def checktime():
    n = datetime.now()
    t = n.timetuple()
    cur_hour = t[3]
    if cur_hour in shuthours:
        blueshut()
    if cur_hour in auto_connect_hours:
        blueautoconnect()
        

# func main
def main():
    dev_loop_count = 0
    pid_true_count = 0
    while True:
        checktime()
        for i in pslist:
            time.sleep(5)
            getpid = getproc(i)
            try:
                for pid in getpid[i]:
                    chain = top ["-p","{}".format(pid), "-b", "-1", "-n", "1"] | tail ["-1"] | awk ['{print $9}']
                    runcmd = float(chain())
                    if runcmd < 20:
                        blue_pid_bool = False
                    else:
                        blue_pid_bool = True
                        print(i, runcmd)
            except:
                pass
        dev_loop_count += 1
        print("Printing Dev Count", dev_loop_count)
        if blue_pid_bool == False:
            pid_true_count += 1
            print("Printing True Count", pid_true_count)
        if pid_true_count == 3:
            print("Shutting Down Bluetooth Devices")
            blueshut()
        # Reset Dev Loop Count after so many itterations, using sleep but should change to using time
        if dev_loop_count == 5:
            print("Resetting Loop Count")
            dev_loop_count = 0
            pid_true_count = 0
 
main()