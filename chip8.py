import random


class Chip8:
    """The basic shape of chip8.
        Sacrificing moudularity since this is a pretty difficult project.
        Therefore the entire thing is going to be in one class."""

    def __init__(self,speed = 600):
        #The start of the program/data space of memory where the roms are loaded from
        self.START_ADDR = 0x200
        #Where fonts are loaded from
        self.FONT_ADDR = 0x50

        #Since the chip-8 isn't running at 60hz, we need to adjust for the timer values
        self.speed = speed
        #Calculate how many cycles should roughly equal a 60hz rate of decrease
        self.timerThreshhold = speed//60
        #Timer counter is incremented each cycle, and if it equals timerThreshold then the timers can decrease by 1
        self.timerCounter = 0


        #The chip-8 has 16 eight bit registers ranging from V0 to VF.
        self.V = [0] * 16

        self.memory = [0] * 4096
        self.index = None
        self.pc = self.START_ADDR
        self.stack = [0] * 16
        self.stackPointer = -1

        #Both these timers decrement at a rate of 60hz if not 0
        self.delayTimer = 0
        self.soundTimer = 0

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

    def getSoundTimer(self):
        return self.soundTimer


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
                if self.stackPointer < 0:
                    print('ERRORRRRRRRRRRRRRR')
                self.pc = self.stack[self.stackPointer]
                self.stackPointer -= 1

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

        elif self.identifier == 0x2:
            #2nnn: Call subroutine at nnn
            self.stackPointer += 1
            self.stack[self.stackPointer] = self.pc
            self.pc = self.NNN
            print('Executing 2nnn: ', hex(self.opcode))

        elif self.identifier == 0x3:
            #3xnn: Skip next instruction if Vx = nn
            if self.V[self.X] == self.NN:
                self.pc += 2
            print('Executing 3xnn: ', hex(self.opcode))

        elif self.identifier == 0x4:
            #4xnn: Skip next instruction if Vx != nn
            if self.V[self.X] != self.NN:
                self.pc += 2
            print('Executing 4xnn: ', hex(self.opcode))

        elif self.identifier == 0x5:
            #5xy0: Skip next instruction if Vx = Vy
            if self.V[self.X] == self.V[self.Y]:
                self.pc += 2
            print('Executing 5xnn: ', hex(self.opcode))

        elif self.identifier == 0x6:
            #6xnn: Set register VX to nn
            self.V[self.X] = self.NN
            print('Executing 6xnn: ', hex(self.opcode))

        elif self.identifier == 0x7:
            #7xnn: Set register VX to VX += nn

            #TEMP FIX!!!!!!
            self.V[self.X] = self.V[self.X] + self.NN
            print('Executing 7xnn: ', hex(self.opcode))

        elif self.identifier == 0x8:
            if self.N == 0x0:
                #8xy0: Stores the value of register Vy in register Vx
                self.V[self.X] = self.V[self.Y]
                print('Executing 8xy0: ', hex(self.opcode))

            elif self.N == 0x1:
                #8xy1: Set Vx = Vx OR Vy
                self.V[self.X] = self.V[self.X] | self.V[self.Y]
                print('Executing 8xy1: ', hex(self.opcode))
            
            elif self.N == 0x2:
                #8xy1: Set Vx = Vx AND Vy
                self.V[self.X] = self.V[self.X] & self.V[self.Y]
                print('Executing 8xy2: ', hex(self.opcode))

            elif self.N == 0x3:
                #8xy3: Set Vx = Vx XOR Vy
                self.V[self.X] = self.V[self.X] ^ self.V[self.Y]
                print('Executing 8xy3: ', hex(self.opcode))
            
            elif self.N == 0x4:
                #8xy4: Set Vx = Vx + Vy, set VF = carry
                self.VxADDVy = (self.V[self.X] + self.V[self.Y])
                if self.VxADDVy > 0xFF:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                self.V[self.X] = self.VxADDVy & 0xFF
                print('Executing 8xy4: ', hex(self.opcode))

            elif self.N == 0x5:
                #8xy5: Set Vx = Vx - Vy, set VF = NOT borrow
                if self.V[self.X] > self.V[self.Y]:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                
                self.V[self.X] = (self.V[self.X] - self.V[self.Y]) 
                print('Executing 8xy5: ', hex(self.opcode))

            elif self.N == 0x6:
                #8xy6: Set Vx = Vx SHR 1
                self.V[0xF] = self.V[self.X] & 0x1
                self.V[self.X] = self.V[self.Y] >> 1
                print('Executing 8xy6: ', hex(self.opcode))

            elif self.N == 0x7:
                #8xy7: Set Vx = Vy - Vx, set VF = NOT borrow
                if self.V[self.Y] > self.V[self.X]:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0

                self.V[self.X] = self.V[self.Y] - self.V[self.X]
                print('Executing 8xy7: ', hex(self.opcode))

            elif self.N == 0xE:
                #8xyE: Set Vx = Vx SHL 1
                if (self.V[self.X] & 0x80) != 0:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                
                self.V[self.X] = self.V[self.Y] << 1
                print('Executing 8xyE: ', hex(self.opcode))

        elif self.identifier == 0x9:
            #9xy0: Skip next instruction if Vx != Vy
            if self.V[self.X] != self.V[self.Y]:
                self.pc += 2

        elif self.identifier == 0xA:
            #Annn: Set index register index to nnn
            self.index = self.NNN
            print('Executing Annn: ', hex(self.opcode))

        elif self.identifier == 0xB:
            #Bnnn: Jump to location nnn + V[0]
            self.pc = self.NNN + self.V[0]
            #self.pc = self.NNN + self.V[self.X]

        elif self.identifier == 0xC:
            #Cxkk: Set Vx to random byte AND nn
            self.V[self.X] = random.randint(0,256) & self.NN

        elif self.identifier == 0xD:
            # Dxyn: Draw and display

            # Modulo to wrap around screen
            self.Xvalue = self.V[self.X] % 64
            self.Yvalue = self.V[self.Y] % 32
            self.V[0xF] = 0 #Collision flag

            for row in range(self.N):
                self.spriteByte = self.memory[self.index + row]
                
                for column in (range(8)):
                    if (self.Yvalue + row) < 32 and (self.Xvalue + column) < 64:
                        #Get value of bit
                        self.spritePixel = 0
                        if (self.spriteByte & (2**(7-column))) > 0:
                            self.spritePixel = 1  
                        self.screenPixel = self.video[(self.Yvalue + row)][(self.Xvalue + column)]
                        

                        self.spriteXorScreen = self.spritePixel ^ self.screenPixel
                        self.video[(self.Yvalue + row)][(self.Xvalue + column)] = self.spriteXorScreen
                        
                        #If screen pixel has been xor'ed, then set collision flag
                        if self.spritePixel and not self.spriteXorScreen:
                            self.V[0xF] = 1

            print('Executing Dxyn: ', hex(self.opcode))

            # Returning true so pygame redraws screen
            return True

        elif self.identifier == 0xE:
            if self.N == 0xE:
                #Ex9E: Skip next instruction if key with value of Vx pressed
                pass
            elif self.N == 0x1:
                #ExA1: Skip next instruction if key with the value of Vx not pressed
                pass
        elif self.identifier == 0xF:
            if self.NN == 0x07:
                #Fx07: Set Vx = delay timer value
                self.V[self.X] = self.delayTimer
            elif self.NN == 0x0A:
                #Fx0A: Block execution until key pressed, value stored in Vx
                pass
            elif self.NN == 0x15:
                #Fx15: Set Delay timer = Vx
                self.delayTimer = self.V[self.X]
            elif self.NN == 0x18:
                #Fx18: Set sound timer = Vx
                self.soundTimer = self.V[self.X]
            elif self.NN == 0x1E:
                #Fx1E: Index and Vx are added and stored in index
                self.index += self.V[self.X]
            elif self.NN == 0x29:
                #Fx29: Set Index to address of hexadecimal character in Vx
                self.char = self.V[self.X] & 0x0F
                self.addressOfChar = self.char * 5 + self.FONT_ADDR
                self.index = self.addressOfChar
            
            elif self.NN == 0x33:
                #Fx33: Store BCD representation of Vx in memory locations I, I+1 and I+2
                self.Vx = self.V[self.X]

                self.hundreds = self.Vx  // 100
                self.tens = (self.Vx // 10) % 10
                self.ones = (self.Vx) % 10

                self.BCD = [self.hundreds,self.tens,self.ones]

                for i in range(3):
                    self.memory[self.index + i] = self.BCD[i]
                print('Executing Fx33: ', hex(self.opcode))
            

            
            elif self.NN == 0x55:
                #Fx55: Store all register data till Vx(included) in memory starting at I
                for register in range(self.X+1):
                    self.memory[self.index + register] = self.V[register]
                    #self.index += 1 #the original implementation increased index
                print('Executing Fx55: ', hex(self.opcode))

            elif self.NN == 0x65:
                #Fx65: Read data from index into registers till Vx(included)
                for register in range(self.X+1):
                    self.V[register] = self.memory[self.index+register]
                    #self.index += 1 #the original implementation increased index
                print('Executing Fx65: ', hex(self.opcode))

            
        #This makes each register an unsigned 8 bit integer
        for i in range(len(self.V)):
            self.V[i] &= 0xFF
            

        

    def cycle(self):
        #The main fetch, decode execute cycle of the processor
        
        #fetch and construct the opcode from two bytes, the current pc and pc+1
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc+1]

        #increment pc by two as each instruction is 2 bytes
        self.pc += 2

        #Deal with timers
        if self.delayTimer > 0:
            self.delayTimer -= 1
        if self.soundTimer > 0:
            self.soundTimer -= 1
        
        '''self.timerCounter += 1
        if self.timerCounter % self.timerThreshhold == 0:
            if self.delayTimer > 0:
                print('delaytimer: ', self.delayTimer)
                self.delayTimer -= 1
            if self.soundTimer > 0:
                self.soundTimer -= 1
                print('soundtimer: ', self.soundTimer)'''

        
        #decode and execute instruction, as well as draw to screen if needed
        self.redrawFlag = self.executeOpcode()
        if self.redrawFlag:
            return True


