from array import array


class MemoryEmulator:
    def __init__(self) -> None:
        self._memory = array("L", [0]) * (1024 * 1024 // 4)  # 1Mb | 262.144 words
        # 1 word = 32 bits (4 bytes)

    @staticmethod
    def _get_pos(pos: int) -> int:
        return pos & 0b111111111111111111

    def read_word(self, memory_address: int) -> int:
        # reads the value storage at 'memory_address'
        pos = self._get_pos(memory_address)
        return self._memory[pos]

    def write_word(self, memory_address: int, value: int) -> None:
        # writes a value (value) at 'memory_address'
        pos = self._get_pos(memory_address)
        value = value & 0xFFFFFFFF
        self._memory[pos] = value

    def read_byte(self, memory_address: int) -> int:
        # reads
        pos = self._get_pos(memory_address)
        addr_word = pos >> 2
        word_stored = self._memory[addr_word]

        end_byte = pos & 0b11
        val_byte = word_stored >> (end_byte << 3)
        val_byte = val_byte & 0xFF

        return val_byte

    def write_byte(self, memory_address: int, value: int) -> None:
        # writes
        value &= 0xFF

        pos = self._get_pos(memory_address)
        addr_word = pos >> 2
        word_stored = self._memory[addr_word]

        end_byte = pos & 0b11
        mask = ~(0xFF << (end_byte << 3))
        word_stored &= mask
        value = value << (end_byte << 3)
        word_stored |= value

        self._memory[addr_word] = word_stored
