data = "MOV DSK.FLOPPY 1 3 ; MOV DTX DSK.FLOPPY 1 3 ; "
xolo = data.split()

#DOCUMENTATION
#MOV LOAD NUM
#ADD LOAD NUM
#SUB LOAD NUM
#MOV SLOTLOAD SLOT LOAD
#MOV LOAD SLOTLOAD SLOT
#STDOUT SLOTLOAD SLOT
#STDOUT LOAD
#ONLY CPU REG CAN SUB AND ADD
#SEMICOLONS ARE OBLIGATORY

RAM = [0] * 64
FLOPPY = [0] * 1440
DTX = 0


def interpret(xolo):
    try:
        global DTX, RAM, FLOPPY #the entire language is interpreted in int
        inter_main = 0
        numberator = 0
        cmd = 0 #1 is mov 2 is stdout 3 is add 4 is sub
        payload = 0 #1 is dtx and 2 is ram
        slot = 0 #slot considers ram to be 64 Bit while hard drivers or floppies may be 1.44 KiB
        for i in xolo:
            if i == "MOV" and inter_main == 0: # mov command
                print("move")
                inter_main = 1
                cmd = 1
                continue
            if i == "ADD" and inter_main == 0:# add cmd
                print("add")
                inter_main = 1
                cmd = 3
                continue
            if i == "SUB" and inter_main == 0:# sub cmd
                print("sub")
                inter_main = 1
                cmd = 4
                continue
            if i == "STDOUT" and inter_main == 0: #stdout command
                print("stdout")
                inter_main = 1
                cmd = 2
                continue
            if i == "DTX" and inter_main == 1: #dtx preamble
                print("to dtx")
                inter_main = 2
                payload = 1
                continue
            if i == "DSK.FLOPPY" and inter_main == 1: #floppy preamble
                print("to l floppy")
                inter_main = 2
                payload = 3
                continue
            if i == "RAM" and inter_main == 1: #ram preamble
                print("to l ram")
                inter_main = 2
                payload = 2
                continue
            if inter_main == 2 and payload == 1 and cmd == 2:
                print("---------- stdout confirm")
                print(f"dtx value: {DTX}")
                inter_main = 0
                continue
            if inter_main == 2 and payload == 3 and cmd == 2:
                print("STDOUT READING DISK")
                print(FLOPPY)

            if inter_main == 2 and payload == 1 and cmd == 3:
                numberator = int(i)
                print("dtx add")
                DTX = int(DTX) + numberator
                inter_main = 0
                print(DTX)
            if inter_main == 2 and payload == 1 and cmd == 4:
                numberator = int(i)
                print("dtx sub")
                DTX = int(DTX) - numberator
                inter_main = 0
                print(DTX)
            if inter_main == 2 and cmd == 1 and payload == 1: #DTX alloc
                if i != "RAM" and i != "DSK.FLOPPY":
                    DTX = int(i)
                    print(i)
                    inter_main = 0
                elif i == "RAM":
                    print("RAM FLAG")
                    inter_main = 3
                else:
                    print("FLOP FLAG")
                    inter_main = 4
                continue
            if inter_main == 3 and cmd == 1 and payload == 1:
                print("dtx take ram")
                located = RAM[int(i)]
                DTX = int(located)
                inter_main = 0
                continue
            if inter_main == 4 and cmd == 1 and payload == 1:
                print("dtx take floppy")
                located = FLOPPY[int(i)]
                DTX = int(located)
                inter_main = 0
                continue
            if inter_main == 2 and cmd == 1 and payload == 2: #RAM slot alloc
                print(i)
                slot = int(i)
                inter_main = 3
                cmd = 330 # reserved for ram
                continue
            if inter_main == 2 and cmd == 1 and payload == 3: #Floppy slot alloc
                print(i)
                slot = int(i)
                inter_main = 3
                cmd = 331 #reserved for floppy
                continue
            if inter_main == 2 and cmd == 2 and payload == 2: #stdout slot alloc
                print(i)
                print("--------------- stdout confirm")
                slot = int(i)
                inter_main = 3
                print(f"------------- slot: {slot}")
                print(f"------------- ram val: {RAM[slot]}")
                inter_main = 0
                continue
            if inter_main == 3 and cmd == 330: #RAM alloc
                if i == "DTX":
                    RAM[slot] = int(DTX)
                    print("DTX to RAM")
                else:
                    RAM[slot] = int(i)
                    print("Int to RAM")
                continue
            if inter_main == 3 and cmd == 331: #FLOPPY alloc
                if i == "DTX":
                    FLOPPY[slot] = int(DTX)
                    print("DTX to FLOPPY")
                else:
                    FLOPPY[slot] = int(i)
                    print("Int to FLOPPY")
                inter_main = 0
                continue
            if i == ";": #command restarter
                slot = 0
                payload = 0
                inter_main = 0
                cmd = 0
    except IndexError:
        print("errno 0x0001: Index Err either at FLOPPY or RAM")

interpret(xolo)
input("Press enter to exit")

