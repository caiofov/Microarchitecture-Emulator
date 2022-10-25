from array import array

from components import ULA, Bus, Registers


class CPU:
    def __init__(self) -> None:
        self._regs = Registers()
        self._ula = ULA()
        self._bus = Bus()
        self._control_store = array("L", [0]) * 512
