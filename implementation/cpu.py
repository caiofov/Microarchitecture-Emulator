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

    def _read_registers(self, register_number: int) -> None:
        self._bus.BUS_A = self._regs.H
        self._bus.BUS_B = self._regs.get_reg(register_number)

    def _write_registers(self, register_bits: int) -> None:
        self._regs.write_reg(register_bits, self._bus.BUS_C)

    def _alu_operation(self, control_bits: int) -> None:
        self._bus.BUS_C = self._alu.operation(
            control_bits, self._bus.BUS_A, self._bus.BUS_B
        )

    def _next_instruction(self, next_instruction: int, jam: int) -> None:
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

    def _memory_io(self, mem_bits: int) -> None:
        if mem_bits & 0b001:
            self._regs.MBR = self._memory.read_byte(self._regs.PC)
        if mem_bits & 0b010:
            self._regs.MDR = self._memory.read_word(self._regs.MAR)
        if mem_bits & 0b100:
            self._memory.write_word(self._regs.MAR, self._regs.MDR)

    def add_instruction(self, instruction: int) -> None:
        self._firmware.append(instruction)

    def step(self) -> bool:
        self._regs.MIR = self._firmware[self._regs.MPC]

        if self._regs.MIR == 0:
            return False

        self._read_registers(self._regs.MIR & 0b00000000000000000000000000000111)

        self._alu_operation((self._regs.MIR & 0b00000000000011111111000000000000) >> 12)

        self._write_registers(
            (self._regs.MIR & 0b00000000000000000000111111000000) >> 6
        )

        self._memory_io((self._regs.MIR & 0b00000000000000000000000000111000) >> 3)

        self._next_instruction(
            (self._regs.MIR & 0b11111111100000000000000000000000) >> 23,
            (self._regs.MIR & 0b00000000011100000000000000000000) >> 20,
        )

        return True
