from array import array
from typing import Optional

from .components import ALU, Bus, Registers
from .memory import Memory


class CPU:
    """Emulates a CPU"""

    def __init__(self) -> None:
        self._regs = Registers()
        self._alu = ALU()
        self._bus = Bus()
        self.firmware = array("L", [0]) * 512
        self._memory = Memory()
        self._last_inst_idx = 0
        self._control()

    def read_image(self, img: str) -> None:
        """Reads a .bin file
        Args:
            img (str): path to the file
        """
        byte_address = 0
        with open(img, "rb") as disk:
            while byte := disk.read(1):
                self._memory.write_byte(byte_address, int.from_bytes(byte, "little"))
                byte_address += 1

    def halt(self) -> None:
        """Halt instruction"""
        self.firmware[255] = 0b00000000000000000000000000000000

    def _read_registers(self, register_number: int) -> None:
        self._bus.BUS_A = self._regs.H
        self._bus.BUS_B = self._regs.get_reg(register_number)

    def _write_registers(self, register_bits: int) -> None:
        self._regs.write_reg(register_bits, self._bus.BUS_C)

    def _alu_operation(self, control_bits: int) -> None:
        if not control_bits:
            return
        self._bus.BUS_C = self._alu.operation(
            control_bits, self._bus.BUS_A, self._bus.BUS_B
        )

    def _next_instruction(self, next_instruction: int, jam: int) -> None:
        if jam == 0b000:
            self._regs.MPC = next_instruction
            return

        if jam & 0b001:
            next_instruction |= self._alu.Z << 8
        elif jam & 0b010:
            next_instruction |= self._alu.N << 8
        elif jam & 0b100:
            next_instruction |= self._regs.MBR

        self._regs.MPC = next_instruction

    def _memory_io(self, mem_bits: int) -> None:
        if mem_bits & 0b001:
            self._regs.MBR = self._memory.read_byte(self._regs.PC)
        elif mem_bits & 0b010:
            self._regs.MDR = self._memory.read_word(self._regs.MAR)
        elif mem_bits & 0b100:
            self._memory.write_word(self._regs.MAR, self._regs.MDR)

    def _step(self) -> bool:
        self._regs.MIR = self.firmware[self._regs.MPC]

        if self._regs.MIR == 0:
            return False

        r_regs, alu, w_regs, mem, nxt, jam = self._parse_instruction(self._regs.MIR)

        self._read_registers(r_regs)
        self._alu_operation(alu)
        self._write_registers(w_regs)
        self._memory_io(mem)
        self._next_instruction(nxt, jam)

        return True

    @staticmethod
    def _parse_instruction(instruction: int) -> tuple[int, int, int, int, int, int]:
        return (
            instruction & 0b00000000000000000000000000000111,
            (instruction & 0b00000000000011111111000000000000) >> 12,
            (instruction & 0b00000000000000000000111111000000) >> 6,
            (instruction & 0b00000000000000000000000000111000) >> 3,
            (instruction & 0b11111111100000000000000000000000) >> 23,
            (instruction & 0b00000000011100000000000000000000) >> 20,
        )

    def execute(self) -> int:
        """
        Executes all intructions stored at the firmware
        Returns:
            int: Number of steps
        """
        ticks = 0
        while self._step():
            ticks += 1
        return ticks  # displays number of steps

    def __str__(self) -> str:
        output = {}
        idx = 0
        for data in self.firmware:
            if data:
                output[str(idx)] = data
            idx += 1

        return str(output)

    def _main_op(self) -> None:
        # main: PC <- PC + 1; MBR <- read_byte(PC); GOTO MBR
        self.firmware[0] = 0b000000000_100_00_110101_001000_001_001

    def _add_op(self) -> None:
        # X = X + mem[address]
        ##2: PC <- PC + 1; MBR <- read_byte(PC); GOTO 3
        self.firmware[2] = 0b000000011_000_00_110101_001000_001_001
        ##3: MAR <- MBR; read_word; GOTO 4
        self.firmware[3] = 0b000000100_000_00_010100_100000_010_010
        ##4: H <- MDR; GOTO 5
        self.firmware[4] = 0b000000101_000_00_010100_000001_000_000
        ##5: X <- H + X; GOTO 0
        self.firmware[5] = 0b000000000_000_00_111100_000100_000_011

    def _sub_op(self) -> None:
        # X = X - mem[address]
        ##6: PC <- PC + 1; fetch; goto 7
        self.firmware[6] = 0b000000111_000_00_110101_001000_001_001
        ##7: MAR <- MBR; read; goto 8
        self.firmware[7] = 0b000001000_000_00_010100_100000_010_010
        ##8: H <- MDR; goto 9
        self.firmware[8] = 0b000001001_000_00_010100_000001_000_000
        ##9: X <- X - H; goto 0
        self.firmware[9] = 0b000000000_000_00_111111_000100_000_011

    def _mov_op(self) -> None:
        # mem[address] = X
        ##10: PC <- PC + 1; fetch; GOTO 11
        self.firmware[10] = 0b000001011_000_00_110101_001000_001_001
        ##11: MAR <- MBR; GOTO 12
        self.firmware[11] = 0b000001100_000_00_010100_100000_000_010
        ##12: MDR <- X; write; GOTO 0
        self.firmware[12] = 0b000000000_000_00_010100_010000_100_011

    def _goto_op(self) -> None:
        # goto address
        ##13: PC <- PC + 1; fetch; GOTO 14
        self.firmware[13] = 0b000001110_000_00_110101_001000_001_001
        ##14: PC <- MBR; fetch; GOTO MBR
        self.firmware[14] = 0b000000000_100_00_010100_001000_001_010

    def _jz_op(self) -> None:
        # if X = 0 then goto address
        ## 15: X <- X; IF ALU = 0 GOTO 272(100010000) ELSE GOTO 16(000010000)
        self.firmware[15] = 0b000010000_001_00_010100_000100_000_011
        ## 16: PC <- PC + 1; GOTO 0
        self.firmware[16] = 0b000000000_000_00_110101_001000_000_001
        ## 272: GOTO 13
        self.firmware[17] = 0b000001101_000_00_000000_000000_000_000

    def _control(self) -> None:
        # C => MAR, MDR, PC, X, Y, H
        # B => 000 = MDR, 001 = PC, 010 = MBR, 011 = x, 100 = Y
        self._main_op()

        self._add_op()  # X = X + mem[address]
        self._sub_op()  # X = X - mem[address]
        self._mov_op()  # mem[address] = X
        self._goto_op()  # goto address
        self._jz_op()  # if X = 0 then goto address

        self.halt()
