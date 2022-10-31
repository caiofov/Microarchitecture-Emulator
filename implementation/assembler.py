from io import IOBase


class Assembler:
    def __init__(self, source: str, output: str = "program.bin") -> None:
        self.source_file = source
        self.output_file = output
        self.lines = []
        self.lines_bin = []
        self.names = []

        self.instruction_set = {
            "add": 0x02,
            "sub": 0x06,
            "goto": 0x0D,
            "mov": 0x0A,
            "jz": 0x0F,
            "add1": 0x11,
            "halt": 0xFF,
        }
        self.instructions = list(self.instruction_set.keys()) + ["wb", "ww"]

    def _is_instruction(self, token: str) -> bool:
        return token in self.instructions

    def _is_name(self, token: str) -> bool:
        name = False
        for n in self.names:
            if name := (n[0] == token):
                break
        return name

    def _encode_2ops(self, inst: str, ops: list[str]) -> list[int]:
        if len(ops) > 1 and ops[0] == "x":
            if self._is_name(ops[1]):
                return [self.instruction_set[inst], ops[1]]
        raise ValueError("Invalid input ", ops)

    def _encode_goto(self, ops: list[str]) -> list[int]:
        if len(ops) > 0 and self._is_name(ops[0]):
            return [self.instruction_set["goto"], ops[0]]
        else:
            raise ValueError("Invalid input ", ops)

    def _encode_wb(self, ops: list[str]) -> list[int]:
        if len(ops) > 0 and ops[0].isnumeric() and int(ops[0]) < 256:
            return [int(ops[0])]
        else:
            raise ValueError("Invalid input ", ops)

    def _encode_ww(self, ops: list[str]) -> list[int]:
        if len(ops) > 0 and ops[0].isnumeric():
            line_bin = []
            val = int(ops[0])

            if val < pow(2, 32):
                line_bin.append(val & 0xFF)
                line_bin.append((val & 0xFF00) >> 8)
                line_bin.append((val & 0xFF0000) >> 16)
                line_bin.append((val & 0xFF000000) >> 24)
                return line_bin
            else:
                raise ValueError("Number exceeded max value of 2^32")

        else:
            raise ValueError("Invalid input ", ops)

    def _encode_instruction(self, instruction: str, ops: list[str]) -> list[int]:
        if instruction in ("add", "sub", "mov", "jz", "ms"):
            return self._encode_2ops(instruction, ops)
        elif instruction == "goto":
            return self._encode_goto(ops)
        elif instruction in ("halt", "add1"):
            return [self.instruction_set[instruction]]
        elif instruction == "wb":
            return self._encode_wb(ops)
        elif instruction == "ww":
            return self._encode_ww(ops)
        else:
            return []

    def _line_to_bin_step1(self, line) -> list[int]:
        return (
            self._encode_instruction(line[0], line[1:])
            if self._is_instruction(line[0])
            else self._encode_instruction(line[1], line[2:])
        )

    def _lines_to_bin_step1(self) -> bool:
        for line in self.lines:
            if not (line_bin := self._line_to_bin_step1(line)):
                raise SyntaxError("Line ", self.lines.index(line))
            self.lines_bin.append(line_bin)
        return True

    def _find_names(self) -> None:
        for k in range(len(self.lines)):
            is_label = True
            for i in self.instructions:
                if self.lines[k][0] == i:
                    is_label = False
                    break
            if is_label:
                self.names.append((self.lines[k][0], k))

    def _count_bytes(self, line_number: int) -> int:
        line = 0
        byte = 1
        while line < line_number:
            byte += len(self.lines_bin[line])
            line += 1
        return byte

    def _get_name_byte(self, str) -> int:
        for name in self.names:
            if name[0] == str:
                return name[1]

    def _resolve_names(self) -> None:
        for i in range(len(self.names)):
            self.names[i] = (self.names[i][0], self._count_bytes(self.names[i][1]))

        for line in self.lines_bin:
            for i in range(len(line)):
                if self._is_name(line[i]):
                    line[i] = self._get_name_byte(line[i]) // (
                        4
                        if line[i - 1]
                        in (self.instruction_set[op] for op in ["add", "sub", "mov"])
                        else 1
                    )

    def _load_tokens(self, file: IOBase) -> None:
        """Normalizes all tokens and deletes empty strings
        Args:
            file (IOBase): opened source file
        """
        for l in file:
            tokens = [
                t
                for t in l.replace("\n", "").replace(",", "").lower().split(" ")
                if t and t[0] != "#"
            ]
            if tokens:
                self.lines.append(tokens)

    def execute(self) -> None:
        """Executes the assembler"""

        with open(self.source_file, "r") as fsrc:
            self._load_tokens(fsrc)
            self._find_names()

            if self._lines_to_bin_step1():
                self._resolve_names()
                byte_arr = [0]

                for line in self.lines_bin:
                    for byte in line:
                        byte_arr.append(byte)

                with open(self.output_file, "wb") as fdst:
                    fdst.write(bytearray(byte_arr))
