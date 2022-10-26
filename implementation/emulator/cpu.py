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

    def read_image(self, img: str) -> None:
        """Reads a .bin file
        Args:
            img (str): path to the file
        """
        with open(img, "rb") as disk:
            while byte := disk.read(4):
                self.add_instruction(int.from_bytes(byte, "little"))

    def add_instruction(self, instruction: int, index: Optional[int] = None) -> None:
        """Adds a new instruction to the firmware
        Args:
            instruction (int): Instruction to be added
            index (Optional[int], optional): New struction's index(None to append). Defaults to None.
        """
        if not (idx := index):
            idx = self._last_inst_idx
            self._last_inst_idx += 1
        self.firmware[idx] = instruction

    def halt(self) -> None:
        """Halt instruction"""
        self.add_instruction(0b00000000000000000000000000000000, 255)

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
        while True:
            if self._step():
                ticks += 1
            else:
                break
        return ticks  # displays number of steps
