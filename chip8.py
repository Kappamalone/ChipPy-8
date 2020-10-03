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

        #Two dimensional matrix for representation of graphics
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
        print()

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

    def getVideo(self):
        return self.video

    def executeOpcode(self):
        #Decode a given opcode and extract the required
        #values from the opcode which are X, Y and N

        self.identifier = (self.opcode & 0xF000) >> 12 #First Nibble: Used to differentiate most opcodes apart
        self.X = (self.opcode & 0x0F00) >> 8 # Second Nibble: 
        self.Y = (self.opcode & 0x00F0) >> 4 # Third Nibble:
        self.N = (self.opcode & 0x000F) # Fourth Nibble: 
        self.NN = self.opcode & 0x00FF # Third and Fourth Nibble: 
        self.NNN = self.opcode & 0x0FFF # Second, Third and Fourth Nibble:  
        #print(self.identifier, self.X, self.Y, self.N, self.NN, self.NNN)

        if self.identifier == 0x0:
            if self.NN == 0xEE:
                #00EE: Return from subroutine
                pass
            elif self.Y == 0xE:
                #00E0: Clear Screen
                self.video = [[0]*64 for i in range(32)]
                print('Executing 00E0: Clear Screen ' + hex(self.opcode))

                #returning true so pygame redraws screen
                return True

        elif self.identifier == 0x1:
            #1nnn: Jump to location nnn
            self.pc = self.NNN
            print('Executing 1nnn: ', hex(self.opcode))


        elif self.identifier == 0x6:
            #6xnn: Set register VX to nn
            self.V[self.X] = self.NN
            print('Executing 6xnn: ', hex(self.opcode))

        elif self.identifier == 0x7:
            #7xnn: Set register VX to VX += nn
            self.V[self.X] += self.NN
            print('Executing 7xnn: ', hex(self.opcode))

        elif self.identifier == 0xA:
            #Annn: Set index register index to nnn
            self.index = self.NNN
            print('Executing Annn: ', hex(self.opcode))

        elif self.identifier == 0xD:
            # Dxyn: Draw and display

            # Modulo to wrap around screen
            self.Xvalue = self.V[self.X] % 64
            self.Yvalue = self.V[self.Y] % 32
            self.V[0xF] = 0 #Collision flag

            for row in range(self.N):
                self.spriteByte = self.memory[self.index + row]
                
                for column in range(8):
                    #Get value of bit
                    self.spritePixel = 0
                    if (self.spriteByte & (0x80 >> column)) > 0:
                        self.spritePixel = 1 

                    self.screenPixel = self.video[self.Yvalue + row][self.Xvalue + column]
                    

                    self.spriteXorScreen = self.spritePixel ^ self.screenPixel
                    self.video[self.Yvalue + row][self.Xvalue + column] = self.spriteXorScreen
                    
                    #If screen pixel has been xor'ed, then set collision flag
                    if self.spritePixel and not self.spriteXorScreen:
                        self.V[0xF] = 1


            print('Executing Dxyn: ', hex(self.opcode))

            # Returning true so pygame redraws screen
            return True
            

        

    def cycle(self):
        #The main fetch, decode execute cycle of the processor
        
        #fetch and construct the opcode from two bytes, the current pc and pc+1
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc+1]

        #increment pc by two as each instruction is 2 bytes
        self.pc += 2

        #print(hex(self.opcode), end = '\t')

        #decode and execute instruction, as well as draw to screen if needed
        self.redrawFlag = self.executeOpcode()
        if self.redrawFlag:
            return True

