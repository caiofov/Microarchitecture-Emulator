from array import array


class Memory:
    """Emulates a memory (1Mb storage and 32 bits each word"""

    def __init__(self) -> None:
        self._memory = array("L", [0]) * (1024 * 1024 // 4)  # 1Mb | 262.144 words
        # 1 word = 32 bits (4 bytes)

    @staticmethod
    def _normalize_pos(pos: int) -> int:
        return pos & 0b1111111111111111111

    def read_word(self, memory_address: int) -> int:
        """Reads the words located at the given memory address
        Args:
            memory_address (int): word's address
        Returns:
            int: word
        """
        # reads the value storage at 'memory_address'
        pos = self._normalize_pos(memory_address)
        return self._memory[pos]

    def write_word(self, memory_address: int, value: int) -> None:
        """Writes the given word to the given memory address
        Args:
            memory_address (int): address to which the word will be written
            value (int): value to write
        """
        # writes a value (value) at 'memory_address'
        pos = self._normalize_pos(memory_address)
        value = value & 0xFFFFFFFF
        self._memory[pos] = value

    def read_byte(self, byte: int) -> int:
        """Reads a byte from the memory
        Args:
            byte (int): byte to read
        Returns:
            int: value stored in that byte
        """
        pos = self._normalize_pos(byte)
        addr_word = pos >> 2  # divides 'pos' by 4 (32 bits - 4 bytes - word's size)
        word_stored = self._memory[addr_word]

        end_byte = (pos & 0b11) << 3  # remainder of the division converted to bytes
        val_byte = word_stored >> end_byte

        return val_byte & 0xFF

    def write_byte(self, byte: int, value: int) -> None:
        """Writes a value into a byte from the memory
        Args:
            byte (int): byte to which the value will be written
            value (int): value to write
        """
        value &= 0xFF

        pos = self._normalize_pos(byte)
        addr_word = pos >> 2
        word_stored = self._memory[addr_word]

        end_byte = pos & 0b11
        mask = ~(0xFF << (end_byte << 3))
        word_stored &= mask
        value = value << (end_byte << 3)
        word_stored |= value

        self._memory[addr_word] = word_stored
