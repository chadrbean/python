from plumbum import local
import psutil
ls = local["ls"]
grep = local["grep"]
cat = local["cat"]
wc = local["wc"]
top = local["top"]
tail = local["tail"]


def getproc(psname):
    piddic = {}
    piddic.update({psname: []})
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if psname in proc.info["name"]:
            piddic[psname].append(proc.info["pid"])
    if len(piddic[psname]) < 1:
        piddic.pop(psname)
    return piddic

def main():
    pslist = ["brave", "vlc"]
    for i in pslist:
        print(i)
        # chain = top ["-p","{}".format(i), "-b", "-1", "-n", "1"] | tail ["-1"]
        # print(chain())
       

main()