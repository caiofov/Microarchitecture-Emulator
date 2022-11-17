class ALU:
    def __init__(self) -> None:
        self.N = 0
        self.Z = 1

    @staticmethod
    def _parse_operation(operation: int) -> tuple[int, int, int, int, int, int]:
        return (
            (operation & 0b11000000) >> 6,
            (operation & 0b00110000) >> 4,  # f0,f1
            (operation & 0b00001000) >> 3,  # enA
            (operation & 0b00000100) >> 2,  # enB
            (operation & 0b00000010) >> 1,  # invA
            operation & 0b00000001,  # inc
        )

    def operation(self, control_bits: int, a: int, b: int) -> int:
        """Instruction for ALU operation
        Args:
            control_bits (int): according to the microarchiteture (sll8, sra1, f0, f1, enA, enB, invA, inc)
            a (int): value A
            b (int): value B
        Returns:
            int: operation's result
        """
        shift_bits, op, en_a, en_b, inv_a, inc = self._parse_operation(control_bits)

        if op == 0b01:
            res = ((-a if inv_a else a) if en_a else 0) | (b if en_b else 0)
        elif op == 0b11:  # sum
            res = (
                ((-a if inv_a else a) if en_a else 0)
                + (b if en_b else 0)
                + (-inc if inv_a and not en_a else (0 if inv_a and en_a else inc))
            )
        elif en_a and en_b:
            res = a & b if op == 0b00 else ~b
        else:
            raise ValueError("Invalid ALU input ", control_bits)

        if control_bits == 0b110010:
            res = -1

        # update N and Z
        self.N = int(bool(res))
        self.Z = int(not res)

        if shift_bits == 0b11:
            res = res << 8
        elif shift_bits:
            res = res << 1 if shift_bits == 0b01 else res >> 1

        return res
