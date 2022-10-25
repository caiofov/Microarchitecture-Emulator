class Registers:
    def __init__(self) -> None:
        self.MPC = 0
        self.MIR = 0
        self.MAR = 0
        self.MDR = 0
        self.PC = 0
        self.MBR = 0
        self.X = 0
        self.Y = 0
        self.H = 0

    def get_reg(self, reg_num: int) -> int:
        return (
            [self.MDR, self.PC, self.MBR, self.X, self.Y][reg_num]
            if reg_num in range(5)
            else 0
        )

    def write_reg(self, reg_bits: int, value: int) -> None:
        if reg_bits & 0b100000:
            self.MAR = value
        elif reg_bits & 0b010000:
            self.MDR = value
        elif reg_bits & 0b001000:
            self.PC = value
        elif reg_bits & 0b000100:
            self.X = value
        elif reg_bits & 0b000010:
            self.Y = value
        elif reg_bits & 0b000001:
            self.H = value
        else:
            raise ValueError("Invalid register number ", reg_bits)


class ULA:
    def __init__(self) -> None:
        self.N = 0
        self.Z = 1


class Bus:
    def __init__(self) -> None:
        self.BUS_A = 0
        self.BUS_B = 0
        self.BUS_C = 0
