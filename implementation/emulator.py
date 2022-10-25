from array import array


class MemoryEmulator:
    def __init__(self) -> None:
        self._memory = array("L", [0]) * (1024 * 1024 // 4)  # 1Mb | 262.144 words
        # 1 word = 32 bits (4 bytes)

    @staticmethod
    def _get_pos(end: int) -> int:
        return end & 0b111111111111111111

    def read_word(self, end: int) -> int:
        # reads 32 bits
        pos = self._get_pos(end)
        return self._memory[pos]

    def write_word(self, end: int, val: int) -> None:
        # writes 32 bits
        pos = self._get_pos(end)
        val = val & 0xFFFFFFFF
        self._memory[pos] = val

    def read_byte(self, end: int) -> int:
        pos = self._get_pos(end)
        end_word = pos >> 2
        val_word = self._memory[end_word]

        end_byte = pos & 0b11
        val_byte = val_word >> (end_byte << 3)
        val_byte = val_byte & 0xFF
        return val_byte

    def write_byte(self, end: int, val: int) -> None:
        pos = self._get_pos(end)
        val = val & 0xFF
        end_word = pos >> 2
        val_word = self._memory[end_word]
        end_byte = pos & 0b11
        mask = ~(0xFF << (end_byte << 3))
        val_word = val_word & mask
        val = val << (end_byte << 3)
        val_word = val_word | val
        self._memory[end_word] = val_word
