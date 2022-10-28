from emulator import CPU


def instructions(cpu: CPU) -> None:
    # C => MAR, MDR, PC, X, Y, H
    # B => 000 = MDR, 001 = PC, 010 = MBR, 011 = x, 100 = Y
    # main: PC <- PC + 1; MBR <- read_byte(PC); GOTO MBR
    cpu.add_instruction(0b000000000_100_00_110101_001000_001_001)

    cpu._last_inst_idx = 2
    # X = X + mem[address]
    ##2: PC <- PC + 1; MBR <- read_byte(PC); GOTO 3
    cpu.add_instruction(0b000000011_000_00_110101_001000_001_001)
    ##3: MAR <- MBR; read_word; GOTO 4
    cpu.add_instruction(0b000000100_000_00_010100_100000_010_010)
    ##4: H <- MDR; GOTO 5
    cpu.add_instruction(0b000000101_000_00_010100_000001_000_000)
    ##5: X <- H + X; GOTO 0
    cpu.add_instruction(0b000000000_000_00_111100_000100_000_011)

    # X = X - mem[address]
    ##6: PC <- PC + 1; fetch; goto 7
    cpu.add_instruction(0b000000111_000_00_110101_001000_001_001)
    ##7: MAR <- MBR; read; goto 8
    cpu.add_instruction(0b000001000_000_00_010100_100000_010_010)
    ##8: H <- MDR; goto 9
    cpu.add_instruction(0b000001001_000_00_010100_000001_000_000)
    ##9: X <- X - H; goto 0
    cpu.add_instruction(0b000000000_000_00_111111_000100_000_011)

    # mem[address] = X
    ##10: PC <- PC + 1; fetch; GOTO 11
    cpu.add_instruction(0b000001011_000_00_110101_001000_001_001)
    ##11: MAR <- MBR; GOTO 12
    cpu.add_instruction(0b000001100_000_00_010100_100000_000_010)
    ##12: MDR <- X; write; GOTO 0
    cpu.add_instruction(0b000000000_000_00_010100_010000_100_011)

    # goto address
    ##13: PC <- PC + 1; fetch; GOTO 14
    cpu.add_instruction(0b000001110_000_00_110101_001000_001_001)
    ##14: PC <- MBR; fetch; GOTO MBR
    cpu.add_instruction(0b000000000_100_00_010100_001000_001_010)

    # if X = 0 then goto address
    ## 15: X <- X; IF ALU = 0 GOTO 272(100010000) ELSE GOTO 16(000010000)
    cpu.add_instruction(0b000010000_001_00_010100_000100_000_011)
    ## 16: PC <- PC + 1; GOTO 0
    cpu.add_instruction(0b000000000_000_00_110101_001000_000_001)
    ## 272: GOTO 13
    cpu.add_instruction(0b000001101_000_00_000000_000000_000_000, 272)

    # halt:
    cpu.halt()

    # cpu.firmware[0] = 0b00000000100000000000000000010000  # MDR = MEMORY[0]; GOTO 1
    # cpu.firmware[1] = 0b00000001000000010100000001000000  # H = MDR; GOTO 2
    # cpu.firmware[2] = 0b00000001100000110001100100000000  # MAR = X = 1; GOTO 3
    # cpu.firmware[3] = 0b00000010000000000000000000010000  # MDR = MEMORY[MAR]; GOTO 4
    # cpu.firmware[4] = 0b00000010100000111100010000000000  # MDR = H + MDR; GOTO 5
    # cpu.firmware[5] = 0b00000011000000110101000100000011  # X = X + 1; GOTO 6
    # cpu.firmware[6] = 0b00000011100000110101100000000011  # MAR = X + 1; GOTO 7
    # cpu.firmware[7] = 0b00000100000000000000000000100000  # MEMORY[MAR] = MDR; GOTO 8
