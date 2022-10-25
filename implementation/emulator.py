from array import array


class MemoryEmulator:
    def __init__(self) -> None:
        self._memory = array("L", [0]) * (1024 * 1024 // 4)  # 1Mb | 262.144 words
        # 1 word = 32 bits (4 bytes)

    @staticmethod
    def _get_pos(pos: int) -> int:
        return pos & 0b111111111111111111

    def read_word(self, memory_address: int) -> int:
        # reads 32 bits
        pos = self._get_pos(memory_address)
        return self._memory[pos]

    def write_word(self, memory_address: int, value: int) -> None:
        # writes 32 bits
        pos = self._get_pos(memory_address)
        value = value & 0xFFFFFFFF
        self._memory[pos] = value

    def read_byte(self, memory_address: int) -> int:
        pos = self._get_pos(memory_address)
        end_word = pos >> 2
        val_word = self._memory[end_word]

        end_byte = pos & 0b11
        val_byte = val_word >> (end_byte << 3)
        val_byte = val_byte & 0xFF
        return val_byte

    def write_byte(self, memory_address: int, value: int) -> None:
        pos = self._get_pos(memory_address)
        value = value & 0xFF
        end_word = pos >> 2
        val_word = self._memory[end_word]
        end_byte = pos & 0b11
        mask = ~(0xFF << (end_byte << 3))
        val_word = val_word & mask
        value = value << (end_byte << 3)
        val_word = val_word | value
        self._memory[end_word] = val_word
