# NOTE: I took some inspiration from Rev Downie @ GitHub to code the
# classes "MVHandler" and "MV32Handler", more specifically, how they handle
# immediate vs non-immediate instructions (MV vs MVI and MV32 vs MVI32).
# I didn't intend to read someone else's code initially, but I got to
# the point where I've already written several VMs and none of these
# were working with the actual payload (but did with the sample program)
# so I was getting a little bit frustrated. In the end, the problem was
# somewhere else (at the ASCII85 decoding process).

class ADDHandler:
    def load(self, memory):
        self.opcode = memory.read(1)
        self.opcode = int.from_bytes(self.opcode, "little")

    def execute(self, registers, memory, output):
        registers["a"] += registers["b"]
        registers["a"] %= 255

class APTRHandler:
    def load(self, memory):
        self.opcode = memory.read(1)
        self.opcode = int.from_bytes(self.opcode, "little")
        self.immediate = memory.read(1)
        self.immediate = int.from_bytes(self.immediate, "little")

    def execute(self, registers, memory, output):
        registers["ptr"] += self.immediate

class CMPHandler:
    def load(self, memory):
        self.opcode = memory.read(1)
        self.opcode = int.from_bytes(self.opcode, "little")

    def execute(self, registers, memory, output):
        if registers["a"] == registers["b"]:
            registers["f"] = 0x00
        else:
            registers["f"] = 0x01

class HALTHandler:
    def load(self, memory):
        self.opcode = memory.read(1)
        self.opcode = int.from_bytes(self.opcode, "little")

    def execute(self, registers, memory, output):
        pass

class JEZHandler:
    def load(self, memory):
        self.opcode = memory.read(1)
        self.opcode = int.from_bytes(self.opcode, "little")
        self.immediate = memory.read(4)
        self.immediate = int.from_bytes(self.immediate, "little")

    def execute(self, registers, memory, output):
        if registers["f"] == 0x00:
            registers["pc"] = self.immediate

class JNZHandler:
    def load(self, memory):
        self.opcode = memory.read(1)
        self.opcode = int.from_bytes(self.opcode, "little")
        self.immediate = memory.read(4)
        self.immediate = int.from_bytes(self.immediate, "little")

    def execute(self, registers, memory, output):
        if registers["f"] != 0x00:
            registers["pc"] = self.immediate

class MVHandler:
    def load(self, memory):
        self.opcode = memory.read(1)
        self.opcode = int.from_bytes(self.opcode, "little")

        # A zero "source" indicates a MVI instruction instead of
        # a MV one, so, we need to read the immediate payload.
        source = (self.opcode & 0b00000111)

        if source == 0:
            self.immediate = memory.read(1)
            self.immediate = int.from_bytes(self.immediate, "little")

    def execute(self, registers, memory, output):
        number_to_register = { 1: "a", 2: "b", 3: "c", 4: "d",
                               5: "e", 6: "f", 7: "ptr+c" }

        destination = (self.opcode & 0b00111000) >> 3

        source = (self.opcode & 0b00000111)
        source_value = None

        if source != 0:
            if source != 7:
                source_value = registers[number_to_register[source]]
            else:
                # "ptr+c" is a pseudo register that indicates a memory
                # location.
                offset = registers["ptr"] + registers["c"]
                source_value = memory.peek_from(offset, 1)
                source_value = int.from_bytes(source_value, "little")
        else:
            source_value = self.immediate

        if destination != 7:
            registers[number_to_register[destination]] = source_value
        else:
            # "ptr+c" is a pseudo register that indicates a memory
            # location.
            offset = registers["ptr"] + registers["c"]
            memory.write_at(offset, 1, source_value)

class MV32Handler:
    def load(self, memory):
        self.opcode = memory.read(1)
        self.opcode = int.from_bytes(self.opcode, "little")

        # A zero "source" indicates a MVI32 instruction instead of
        # a MV32 one, so, we need to read the immediate payload.
        source = (self.opcode & 0b00000111)

        if source == 0:
            self.immediate = memory.read(4)
            self.immediate = int.from_bytes(self.immediate, "little")

    def execute(self, registers, memory, output):
        number_to_register = { 1: "la", 2: "lb", 3: "lc", 4: "ld",
                               5: "ptr", 6: "pc" }

        destination = (self.opcode & 0b00111000) >> 3

        source = (self.opcode & 0b00000111)
        source_value = None

        if source != 0:
            source_value = registers[number_to_register[source]]
        else:
            source_value = self.immediate

        registers[number_to_register[destination]] = source_value

class OUTHandler:
    def load(self, memory):
        self.opcode = memory.read(1)
        self.opcode = int.from_bytes(self.opcode, "little")

    def execute(self, registers, memory, output):
        output.append(registers["a"])

class SUBHandler:
    def load(self, memory):
        self.opcode = memory.read(1)
        self.opcode = int.from_bytes(self.opcode, "little")

    def execute(self, registers, memory, output):
        registers["a"] -= registers["b"]

        if registers["a"] < 0:
            registers["a"] += 255

class XORHandler:
    def load(self, memory):
        self.opcode = memory.read(1)
        self.opcode = int.from_bytes(self.opcode, "little")

    def execute(self, registers, memory, output):
        registers["a"] ^= registers["b"]
