from vm_handlers import *
from vm_memory import *

class VM:
    def __init__(self, memory_data: bytes):
        self.registers = {
            # 8-bit registers.
            "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0,

            # 32-bit registers.
            "la": 0, "lb": 0, "lc": 0, "ld": 0, "ptr": 0, "pc": 0,
        }

        self.memory = VMMemory(self.registers, memory_data)

        # Maps an opcode to the corresponding handler class, which
        # will load the instruction and execute it. Instructions
        # that are less-than-a-byte long, such as MV or MV32, are
        # not included here since they require a little more special
        # handling.
        self.opcode_to_handler = {
            0xC2: ADDHandler, 0xE1: APTRHandler, 0xC1: CMPHandler,
            0x21: JEZHandler, 0x22: JNZHandler, 0x02: OUTHandler,
            0xC3: SUBHandler, 0xC4: XORHandler,
        }

    def run(self):
        output = bytearray()

        while self.next(output):
            pass

        return output

    def next(self, output: bytearray):
        # Get the instruction code, which is one byte long or less.
        opcode = self.memory.peek(1)
        opcode = int.from_bytes(opcode, "little")

        # Object associated with the instruction which can load and
        # execute it.
        handler = None

        # HALT instruction. It is kinda murky to analyze the opcode
        # here since I'm effectively ignoring the HALTHandler class,
        # but oh well.
        if opcode == 0x01:
            return False

        if opcode in self.opcode_to_handler.keys():
            handler = self.opcode_to_handler[opcode]()
        else:
            # Transform the opcode into its binary representation and
            # remove the leading "0b" part.
            binary_opcode = bin(opcode)[2 : ]

            # Make the binary representation 8 bits long (each bit
            # represented by a character).
            while len(binary_opcode) < 8:
                binary_opcode = "0" + binary_opcode

            # Get the first two bits which indicate if the operation
            # is either a MV or MV32 instruction. MVI and MVI32
            # instructions are just derivatives of them.
            binary_opcode = binary_opcode[0 : 2]

            if binary_opcode == "01":
                handler = MVHandler()
            elif binary_opcode == "10":
                handler = MV32Handler()
            else:
                # TODO: Throw error.
                pass

        # Load the instruction from memory and execute it.
        handler.load(self.memory)
        handler.execute(self.registers, self.memory, output)

        # Keep processing instructions.
        return True
