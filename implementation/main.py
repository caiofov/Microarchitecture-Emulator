from cpu import CPU

if __name__ == "__main__":
    cpu = CPU()

    cpu.add_instruction(0b00000000100000000000000000010000)  # MDR = MEMORY[0]; GOTO 1
    cpu.add_instruction(0b00000001000000010100000001000000)  # H = MDR; GOTO 2
    cpu.add_instruction(0b00000001100000110001100100000000)  # MAR = X = 1; GOTO 3
    cpu.add_instruction(0b00000010000000000000000000010000)  # MDR = MEMORY[MAR]; GOTO 4
    cpu.add_instruction(0b00000010100000111100010000000000)  # MDR = H + MDR; GOTO 5
    cpu.add_instruction(0b00000011000000110101000100000011)  # X = X + 1; GOTO 6
    cpu.add_instruction(0b00000011100000110101100000000011)  # MAR = X + 1; GOTO 7
    cpu.add_instruction(0b00000100000000000000000000100000)  # MEMORY[MAR] = MDR; GOTO 8

    print(cpu.execute())
