from plumbum import local
import psutil
import time
ls = local["ls"]
grep = local["grep"]
cat = local["cat"]
wc = local["wc"]
top = local["top"]
tail = local["tail"]
awk = local["awk"]


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

def main():
    pslist = ["brave", "vlc", "code", "joplin"]
    while True:
        for i in pslist:
            getpid = getproc(i)
            time.sleep(1)
            try:
                for pid in getpid[i]:
                    chain = top ["-p","{}".format(pid), "-b", "-1", "-n", "1"] | tail ["-1"] | awk ['{print $9}']
                    runcmd = chain()
                    if float(runcmd) > 30:
                        print(i, pid, runcmd)
            except:
                pass

main()