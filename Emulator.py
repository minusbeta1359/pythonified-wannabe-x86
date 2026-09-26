
data = "mov DTX 3 ; mov RAM 5 ; mov DTX 45 ; mov RAM 99"
xolo = data.split()

RAM = 0
DTX = 0

def interpret(xolo):
    global DTX, RAM
    inter_main = 0
    cmd = 0 #1 is mov
    payload = 0 #1 is dtx and 2 is ram
    for i in xolo:
        if i == "mov" and inter_main == 0:
            print("move")
            inter_main = 1
            cmd = 1
            continue
        if i == "DTX" and inter_main == 1:
            print("to dtx")
            inter_main = 2
            payload = 1
            continue
        if i == "RAM" and inter_main == 1:
            print("to l ram")
            inter_main = 2
            payload = 2
            continue
        if inter_main == 2 and cmd == 1 and payload == 1:
            DTX = int(i)
            print(i)
            inter_main = 0
            continue
        if inter_main == 2 and cmd == 1 and payload == 2:
            RAM = int(i)
            print(i)
            inter_main = 0
            continue
        if i == ";":
            payload = 0
            inter_main = 0
            cmd = 0

interpret(xolo)