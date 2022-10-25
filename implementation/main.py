from memory_emulator import MemoryEmulator

mem = MemoryEmulator()
mem.write_word(3, 5)
print(mem.read_word(3))

mem.write_byte(80, 200)
print(mem.read_byte(80))

mem.write_word(4, 0xAAFFEEC1)
print(mem.read_byte(18))
