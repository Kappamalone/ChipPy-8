import pygame
from chip8 import Chip8

pygame.init()
pygame.display.set_caption('ChipPy-8')

class window:
    '''Class to handle Chip-8 timing and pygame shenanigans'''

    def __init__(self):

        #Setup the chip-8 emulator by loading fontset and rom into memory
        self.emulator = Chip8()
        self.emulator.loadFontSet()
        self.rom = input('1: IBM, 2: BC, 3: Test: ')
        if self.rom == '1':
            self.emulator.loadRom('IBM Logo.ch8')
        elif self.rom == '2':
            self.emulator.loadRom('BC_test.ch8')
        elif self.rom == '3':
            self.emulator.loadRom('test_opcode.ch8')

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
        self.drawGrid()
        pygame.display.update()
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            self.drawFlag = self.emulator.cycle()
            #self.command = input('Enter command: ')
            if self.drawFlag:
                self.drawGrid()
                pygame.display.update()




if __name__ == "__main__":
    ''''
    emulator = Chip8()
    emulator.loadFontSet()
    emulator.loadRom('IBM Logo.ch8')
    emulator.cycle()'''
    pygame.init()
    pygame.display.set_caption('ChipPy-8')

    window = window()
    window.main()