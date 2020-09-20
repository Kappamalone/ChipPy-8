

class Chip8:

    """The basic shape of chip8"""
    def __init__(self):

        #The chip-8 has 16 eight bit registers ranging from V0 to VF.
        self.registers = [0] * 16

        self.memory = [0] * 4096
        self.index = None
        self.pc = None
        self.stack = [0] * 16
        self.stackPointer = None
        self.delayTimer = None
        self.soundTimer = None
        self.keypad = [0] * 16
        self.video = [[0]*64 for i in range(32)]
        self.opcode = None


    def loadRom(self,file):
        """loading a specified rom"""

        self.START_ADDR = 0x200

        #Load rom into memory of chip8, starting from 0x200
        with open(file,'rb') as file:
            while True:
                byte = file.read(1)
                print('READING BYTE: ',byte,end = '\t')
                if not byte:
                    break
                self.memory[self.START_ADDR] = byte
                print(self.START_ADDR)
                self.START_ADDR += 1
    
            #print(self.memory[0x200:])



if __name__ == "__main__":
    emulator = Chip8()
    emulator.loadRom('BC_test.ch8')