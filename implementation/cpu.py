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
