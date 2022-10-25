from array import array

from components import ULA, Bus, Registers


class CPU:
    def __init__(self) -> None:
        self._regs = Registers()
        self._ula = ULA()
        self._bus = Bus()
        self._control_store = array("L", [0]) * 512

    def read_registers(self, register_number: int) -> None:
        self._bus.BUS_A = self._regs.H
        self._bus.BUS_B = self._regs.get_reg(register_number)

    def write_registers(self, register_bits: int) -> None:
        self._regs.write_reg(register_bits, self._bus.BUS_C)

    def ula_operation(self, control_bits: int) -> None:
        self._bus.BUS_C = self._ula.operation(
            control_bits, self._bus.BUS_A, self._bus.BUS_B
        )

    def next_instruction(self, next_instruction: int, jam: int) -> None:
        if jam == 0b000:
            self._regs.MPC = next_instruction
            return
        if jam & 0b001:
            next_instruction |= self._ula.Z << 8
        if jam & 0b010:
            next_instruction |= self._ula.N << 8
        if jam & 0b100:
            next_instruction |= self._regs.MBR

        self._regs.MPC = next_instruction
