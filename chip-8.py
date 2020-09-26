class Chip8:
    """The basic shape of chip8.
        Sacrificing moudularity since this is a pretty difficult project.
        Therefore the entire thing is going to be in one class."""

    def __init__(self):

        #The start of the program/data space of memory where the roms are loaded from
        self.START_ADDR = 0x200
        #Where fonts are loaded from
        self.FONT_ADDR = 0x50

        #The chip-8 has 16 eight bit registers ranging from V0 to VF.
        self.V = [0] * 16

        self.memory = [0] * 4096
        self.index = None
        self.pc = self.START_ADDR
        self.stack = [0] * 16
        self.stackPointer = None

        #Both these timers decrement at a rate of 60hz if not 0
        self.delayTimer = None
        self.soundTimer = None

        #The keypad has the hexadecimal characters for input
        self.keypad = [0] * 16

        self.video = [[0]*64 for i in range(32)]
        self.opcode = None

    def loadRom(self,file):
        """loading a specified rom"""

        #Load rom into memory of chip8, starting from 0x200
        with open(file,'rb') as file:
            self.counter = self.START_ADDR
            while True:
                byte = file.read(1)
                print('READING BYTE: ',byte,int.from_bytes(byte, byteorder = 'big'),end = '\t')
                if not byte:
                    break
                self.memory[self.counter] = int.from_bytes(byte, byteorder = 'big')
                print(self.counter)
                self.counter += 1

            #print(self.memory[80:])

    def loadFontSet(self):
        """load the fontset of the chip-8 into memory"""

        #load hexadecimal representation of fonts starting from 0x50
        self.fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]

        self.counter = self.FONT_ADDR
        for font in self.fontset:
            self.memory[self.counter] = font
            self.counter += 1

    def executeOpcode(self):
        #Get the required x, y and n values to be used in each opcode
        #Determine which opcode to execute with large if statement
        firstNibble = (self.opcode & 0xF000) >> 12
        X = (self.opcode & 0x0F00) >> 8
        Y = (self.opcode & 0x00F0) >> 4
        N = (self.opcode & 0x000F)

        print(firstNibble,X,Y,N)

    def cycle(self):
        #The main fetch, decode execute cycle of the processor
        print()

        for i in range(100):
            #construct the opcode from two bytes
            self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc+1]
            print(hex(self.opcode), end = '\t')
            self.executeOpcode()

            #increment pc by two as each instruction is 2 bytes
            self.pc += 2





if __name__ == "__main__":
    emulator = Chip8()
    emulator.loadFontSet()
    emulator.loadRom('IBM Logo.ch8')
    emulator.cycle()