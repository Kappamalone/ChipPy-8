import pygame
from chip8 import Chip8
from timeit import default_timer as timer
import sys

class window:
    '''Class to handle Chip-8 timing and pygame shenanigans'''

    def __init__(self,speed = 600):

        #Setting up timer stuff
        self.start = timer()
        self.end = None
        self.speed = int(sys.argv[2])
        self.hertz = 1/speed

        #Setup the chip-8 emulator by loading fontset and rom into memory
        self.emulator = Chip8(self.speed)
        self.emulator.loadFontSet()
        self.rom = self.emulator.loadRom(sys.argv[1])

        #Setting up pygame variables
        self.width = 64 * 16
        self.height = 32 * 16
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.isRunning = True

    def drawGrid(self):
        self.blockSizeX = self.width/ 64  #Set the Xsize of the grid block
        self.blockSizeY = self.height/ 32 #Set the Ysize of the grid block
        for x in range(64):
            for y in range(32):
                self.rect = pygame.Rect(x*self.blockSizeX, y*self.blockSizeY,
                                self.blockSizeX, self.blockSizeY)
                                
                if self.emulator.getVideo()[y][x] == 1:
                    pygame.draw.rect(self.screen,(255, 255, 255),self.rect, 0)
                else:
                    pygame.draw.rect(self.screen,(0, 0, 0),self.rect, 0)

                    
    def main(self):
        #Setup the grid of values
        self.drawGrid()
        pygame.display.update()

        self.key = None

        while self.isRunning:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.isRunning = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.key = 0x1
                        elif event.key == pygame.K_2:
                            self.key = 0x2
                        elif event.key == pygame.K_3:
                            self.key = 0x3
                        elif event.key == pygame.K_4:
                            self.key = 0xC
                        elif event.key == pygame.K_q:
                            self.key = 0x4
                        elif event.key == pygame.K_w:
                            self.key = 0x5
                        elif event.key == pygame.K_e:
                            self.key = 0x6
                        elif event.key == pygame.K_r:
                            self.key = 0xD
                        elif event.key == pygame.K_a:
                            self.key = 0x7
                        elif event.key == pygame.K_s:
                            self.key = 0x8
                        elif event.key == pygame.K_d:
                            self.key = 0x9
                        elif event.key == pygame.K_f:
                            self.key = 0xE
                        elif event.key == pygame.K_z:
                            self.key = 0xA
                        elif event.key == pygame.K_x:
                            self.key = 0x0
                        elif event.key == pygame.K_c:
                            self.key = 0xB
                        elif event.key == pygame.K_v:
                            self.key = 0xF
                    elif event.type == pygame.KEYUP:
                        self.key = None

            #Executes instructin at speed hz
            self.end = timer()
            if (self.end - self.start) > self.hertz:
                self.drawFlag = self.emulator.cycle(self.key)
                #self.command = input('Enter command: ')
                #if self.command == 'reg':
                #    print(self.emulator.V)

                #if draw flag reached, redraw screen
                if self.drawFlag:
                    self.drawGrid()
                    pygame.display.update()
                self.start = self.end

                if self.emulator.getSoundTimer() > 0:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                    





if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('ChipPy-8')
    pygame.mixer.init()
    pygame.mixer.music.load("beep.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()

    window = window()
    window.main()
