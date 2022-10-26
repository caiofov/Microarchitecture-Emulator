import sys

fsrc = open(str(sys.argv[1]), "r")


class Assembler:
    def __init__(self, source: str, output: str = "program.bin") -> None:
        self.source_file = source
        self.output_file = output
        self.lines = []
        self.lines_bin = []
        self.names = []

        self.instructions = ["add", "sub", "goto", "mov", "jz", "halt", "wb", "ww"]
        self.instruction_set = {
            "add": 0x02,
            "sub": 0x06,
            "goto": 0x0D,
            "mov": 0x0A,
            "jz": 0x0F,
            "halt": 0xFF,
        }

    def is_instruction(self, str) -> bool:
        inst = False
        for i in self.instructions:
            if i == str:
                inst = True
                break
        return inst

    def is_name(self, str):
        name = False
        for n in self.names:
            if n[0] == str:
                name = True
                break
        return name

    def encode_2ops(self, inst, ops):
        line_bin = []
        if len(ops) > 1:
            if ops[0] == "x":
                if is_name(ops[1]):
                    line_bin.append(instruction_set[inst])
                    line_bin.append(ops[1])
        return line_bin

    def encode_goto(self, ops):
        line_bin = []
        if len(ops) > 0:
            if is_name(ops[0]):
                line_bin.append(instruction_set["goto"])
                line_bin.append(ops[0])
        return line_bin

    def encode_halt(
        self,
    ):
        line_bin = []
        line_bin.append(instruction_set["halt"])
        return line_bin

    def encode_wb(self, ops):
        line_bin = []
        if len(ops) > 0:
            if ops[0].isnumeric():
                if int(ops[0]) < 256:
                    line_bin.append(int(ops[0]))
        return line_bin

    def encode_ww(self, ops):
        line_bin = []
        if len(ops) > 0:
            if ops[0].isnumeric():
                val = int(ops[0])
                if val < pow(2, 32):
                    line_bin.append(val & 0xFF)
                    line_bin.append((val & 0xFF00) >> 8)
                    line_bin.append((val & 0xFF0000) >> 16)
                    line_bin.append((val & 0xFF000000) >> 24)
        return line_bin

    def encode_instruction(self, inst, ops):
        if inst == "add" or inst == "sub" or inst == "mov" or inst == "jz":
            return encode_2ops(inst, ops)
        elif inst == "goto":
            return encode_goto(ops)
        elif inst == "halt":
            return encode_halt()
        elif inst == "wb":
            return encode_wb(ops)
        elif inst == "ww":
            return encode_ww(ops)
        else:
            return []

    def line_to_bin_step1(self, line):
        line_bin = []
        if is_instruction(line[0]):
            line_bin = encode_instruction(line[0], line[1:])
        else:
            line_bin = encode_instruction(line[1], line[2:])
        return line_bin

    def lines_to_bin_step1(self):
        for line in self.lines:
            line_bin = line_to_bin_step1(line)
            if line_bin == []:
                print("Erro de sintaxe na linha ", self.lines.index(line))
                return False
            self.lines_bin.append(line_bin)
        return True

    def find_names(self):
        for k in range(0, len(self.lines)):
            is_label = True
            for i in self.instructions:
                if self.lines[k][0] == i:
                    is_label = False
                    break
            if is_label:
                names.append((self.lines[k][0], k))

    def count_bytes(self, line_number: int) -> int:
        line = 0
        byte = 1
        while line < line_number:
            byte += len(self.lines_bin[line])
            line += 1
        return byte

    def get_name_byte(self, str):
        for name in self.names:
            if name[0] == str:
                return name[1]

    def resolve_names(self) -> None:
        for i in range(0, len(names)):
            names[i] = (names[i][0], count_bytes(names[i][1]))
        for line in self.lines_bin:
            for i in range(0, len(line)):
                if is_name(line[i]):
                    if (
                        line[i - 1] == instruction_set["add"]
                        or line[i - 1] == instruction_set["sub"]
                        or line[i - 1] == instruction_set["mov"]
                    ):
                        line[i] = get_name_byte(line[i]) // 4
                    else:
                        line[i] = get_name_byte(line[i])

    def execute(self) -> None:
        with open(self.source_file, "r") as fsrc:
            for line in fsrc:
                tokens = line.replace("\n", "").replace(",", "").lower().split(" ")
                i = 0
                while i < len(tokens):
                    if tokens[i] == "":
                        tokens.pop(i)
                        i -= 1
                    i += 1
                if len(tokens) > 0:
                    self.lines.append(tokens)

            self.find_names()
            if self.lines_to_bin_step1():
                self.resolve_names()
                byte_arr = [0]
                for line in self.lines_bin:
                    for byte in line:
                        byte_arr.append(byte)
                with open(self.output_file, "wb") as fdst:
                    fdst.write(bytearray(byte_arr))
