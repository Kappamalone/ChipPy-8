

class Chip8:

    """The basic shape of chip8"""
    def __init__():

        #The chip-8 has 16 eight bit registers ranging from V0 to VF.
        registers = [0] * 16

        memory = [0] * 4096
        index = None
        pc = None
        stack = [0] * 16
        stackPointer = None
        delayTimer = None
        soundTimer = None
        keypad = [0] * 16
        video = [[0]*64 for i in range(32)]
        opcode = None

    """loading a rom"""
    def loadRom(file):
        pass

if __name__ == "__main__":
    pass