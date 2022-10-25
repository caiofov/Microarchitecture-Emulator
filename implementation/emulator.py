from array import array


class MemoryEmulator:
    pass


memory = array("L", [0]) * (1024 * 1024 // 4)  # 1Mb | 262.144 words
# 1 word = 32 bits (4 bytes)


def read_word(end):
    # reads 32 bits
    end = end & 0b111111111111111111
    return memory[end]


def write_word(end, val):
    # writes
    end = end & 0b111111111111111111
    val = val & 0xFFFFFFFF
    memory[end] = val


def read_bytes(end):
    pass
