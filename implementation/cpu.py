from array import array

from components import ALU, Bus, Registers
from memory_emulator import MemoryEmulator


class CPU:
    def __init__(self) -> None:
        self._regs = Registers()
        self._alu = ALU()
        self._bus = Bus()
        self._firmware = array("L", [0]) * 512
        self._memory = MemoryEmulator()

    def read_registers(self, register_number: int) -> None:
        self._bus.BUS_A = self._regs.H
        self._bus.BUS_B = self._regs.get_reg(register_number)

    def write_registers(self, register_bits: int) -> None:
        self._regs.write_reg(register_bits, self._bus.BUS_C)

    def alu_operation(self, control_bits: int) -> None:
        self._bus.BUS_C = self._alu.operation(
            control_bits, self._bus.BUS_A, self._bus.BUS_B
        )

    def next_instruction(self, next_instruction: int, jam: int) -> None:
        if jam == 0b000:
            self._regs.MPC = next_instruction
            return
        if jam & 0b001:
            next_instruction |= self._alu.Z << 8
        if jam & 0b010:
            next_instruction |= self._alu.N << 8
        if jam & 0b100:
            next_instruction |= self._regs.MBR

        self._regs.MPC = next_instruction

    def memory_io(self, mem_bits: int) -> None:
        if mem_bits & 0b001:
            self._regs.MBR = self._memory.read_byte(self._regs.PC)
        if mem_bits & 0b010:
            self._regs.MDR = self._memory.read_word(self._regs.MAR)
        if mem_bits & 0b100:
            self._memory.write_word(self._regs.MAR, self._regs.MDR)
