from assembler import Assembler
from emulator import CPU
from instructions import instructions

if __name__ == "__main__":
    assembler = Assembler("implementation\program.asm")
    assembler.execute()

    cpu = CPU()
    cpu.read_image("program.bin")
    instructions(cpu)

    print(cpu.execute())
