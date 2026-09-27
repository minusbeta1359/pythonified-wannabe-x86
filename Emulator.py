
data = "MOV DTX 5 ; MOV RAM 7 DTX ;"
xolo = data.split()

RAM = [0] * 64
FLOPPY = [0] * 1440
DTX = 0


def interpret(xolo):
    global DTX, RAM, FLOPPY #the entire language is interpreted in bits
    inter_main = 0
    cmd = 0 #1 is mov
    payload = 0 #1 is dtx and 2 is ram
    slot = 0 #slot considers ram to be 64 Bit while hard drivers or floppies may be 1.44 KiB
    for i in xolo:
        if i == "MOV" and inter_main == 0:
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
        if inter_main == 2 and cmd == 1 and payload == 1: #DTX
            DTX = int(i)
            print(i)
            inter_main = 0
            continue
        if inter_main == 2 and cmd == 1 and payload == 2: #RAM
            print(i)
            slot = int(i)
            inter_main = 3
            cmd = 330 # reserved for ram
            continue
        if inter_main == 3 and cmd == 330:
            if i == DTX:
                RAM[slot] = DTX
                print("DTX to RAM")
            else:
                RAM[slot] = i
                print("Int to RAM")

            print("RAM")
            inter_main = 0
            continue
        if i == ";":
            slot = 0
            payload = 0
            inter_main = 0
            cmd = 0

interpret(xolo)
