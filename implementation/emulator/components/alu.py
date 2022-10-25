class ALU:
    def __init__(self) -> None:
        self.N = 0
        self.Z = 1

    def operation(self, control_bits: int, a: int, b: int) -> int:
        shift_bits = (control_bits & 0b11000000) >> 6
        control_bits = control_bits & 0b00111111

        if control_bits == 0b011000:
            o = a
        elif control_bits == 0b010100:
            o = b
        elif control_bits == 0b011010:
            o = ~a
        elif control_bits == 0b101100:
            o = ~b
        elif control_bits == 0b111100:
            o = a + b
        elif control_bits == 0b111101:
            o = a + b + 1
        elif control_bits == 0b111001:
            o = a + 1
        elif control_bits == 0b110101:
            o = b + 1
        elif control_bits == 0b111111:
            o = b - a
        elif control_bits == 0b110110:
            o = b - 1
        elif control_bits == 0b111011:
            o = -a
        elif control_bits == 0b001100:
            o = a & b
        elif control_bits == 0b011100:
            o = a | b
        elif control_bits == 0b010000:
            o = 0
        elif control_bits == 0b110001:
            o = 1
        elif control_bits == 0b110010:
            o = -1
        else:
            ValueError("Invalid ALU input ", control_bits)

        # update N and Z
        self.N = o
        self.Z = int(not o)

        if shift_bits == 0b01:
            o = o << 1
        elif shift_bits == 0b10:
            o = o >> 1
        elif shift_bits == 0b11:
            o = o << 8

        return o
