from assembler import Assembler
from emulator import CPU

if __name__ == "__main__":
    assembler = Assembler("implementation\program.asm")
    assembler.execute()

    cpu = CPU()
    cpu.read_image("program.bin")

    print(cpu.execute())
    print(cpu._memory)
