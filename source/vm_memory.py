class VMMemory:
    def __init__(self, registers, data):
        self.registers = registers
        self.data = data

    # Returns a byte stream read from the current program
    # counter position, without advancing it.
    def peek(self, size: int):
        result = self.data[self.registers["pc"] : self.registers["pc"] + size]

        return result

    # Reads a byte stream from the specified offset, but
    # does not modify the program counter in any way.
    def peek_from(self, offset: int, size: int):
        result = self.data[offset : offset + size]

        return result

    # Replaces one or more bytes at the specified offset,
    # without affecting the program counter.
    def write_at(self, offset: int, size: int, value):
        if size == 1:
            self.data[offset] = value
        else:
            for i in range(0, size, 1):
                self.data[offset + i] = value[i]

    # Returns one or more bytes starting from the program
    # counter, and then increases the program counter by
    # the amount of bytes read.
    def read(self, size: int):
        result = self.data[self.registers["pc"] : self.registers["pc"] + size]
        self.registers["pc"] += size

        return result
