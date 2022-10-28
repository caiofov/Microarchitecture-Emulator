from array import array


class Memory:
    """Emulates a memory (1Mb storage and 32 bits each word)"""

    def __init__(self) -> None:
        self._memory = array("L", [0]) * (1024 * 1024 // 4)  # 1Mb | 262.144 words
        # 1 word = 32 bits (4 bytes)

    @staticmethod
    def _normalize_pos(pos: int, add_num: int = 0, add_bits: int = 0) -> int:
        return pos & ((0b1111111111111111111 << add_num) | add_bits)

    def read_word(self, memory_address: int) -> int:
        """Reads the words located at the given memory address
        Args:
            memory_address (int): word's address
        Returns:
            int: word
        """
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

    def _get_complete_word_by_byte(self, byte: int) -> tuple[int, int, int]:
        pos = self._normalize_pos(byte, 2, 3)
        addr_word = pos >> 2  # divides 'pos' by 4 (32 bits - 4 bytes - word's size)
        word_stored = self._memory[addr_word]
        end_byte = (pos & 0b11) << 3  # remainder of the division converted to bytes

        return word_stored, end_byte, addr_word

    def read_byte(self, byte: int) -> int:
        """Reads a byte from the memory
        Args:
            byte (int): byte to read
        Returns:
            int: value stored in that byte
        """
        word_stored, end_byte, _ = self._get_complete_word_by_byte(byte)
        val_byte = word_stored >> end_byte  # removes all bits before the expected byte

        return val_byte & 0xFF  # turns all unexpected bits into 0

    def write_byte(self, byte: int, value: int) -> None:
        """Writes a value into a byte from the memory
        Args:
            byte (int): byte to which the value will be written
            value (int): value to write
        """
        value &= 0xFF  # prepares the value
        word_stored, end_byte, addr_word = self._get_complete_word_by_byte(byte)

        # mask: turns into 0 all positions to be changed
        mask = ~(0xFF << end_byte)
        word_stored &= mask  # applies the mask

        # produces and stores the new value
        self._memory[addr_word] = word_stored | (value << end_byte)

    def __str__(self) -> str:
        output = {}
        idx = 0
        for data in self._memory:
            if data:
                output[str(idx)] = data
            idx += 1

        return str(output)
