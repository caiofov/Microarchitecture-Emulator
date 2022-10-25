from array import array


class MemoryEmulator:
    def __init__(self) -> None:
        self._memory = array("L", [0]) * (1024 * 1024 // 4)  # 1Mb | 262.144 words
        # 1 word = 32 bits (4 bytes)

    def read_word(self, end: int) -> int:
        # reads 32 bits
        pos = end & 0b111111111111111111
        return self._memory[pos]

    def write_word(self, end: int, val: int) -> None:
        # writes
        pos = end & 0b111111111111111111
        val = val & 0xFFFFFFFF
        self._memory[pos] = val

    def read_byte(self, end: int) -> int:
        pass

    def write_byte(self, end: int, val: int) -> None:
        pass
