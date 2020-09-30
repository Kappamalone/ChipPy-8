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
        self.emulator.loadRom('IBM Logo.ch8')

        #Setting up pygame variables
        self.width = 64 * 16
        self.height = 32 * 16
        self.screen = pygame.display.set_mode((self.width, self.height))

    def main(self):
        for i in range(100):
            print(self.emulator.cycle())




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