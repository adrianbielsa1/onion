from copy import deepcopy

class IPv4Header:
    @classmethod
    def from_bytes(cls, byte_header: bytes):
        # Create instance.
        self = cls()

        self.version = byte_header[0] & 0b11110000 # First 4 bits.
        self.ihl = byte_header[0] & 0b00001111 # Last 4 bits.
        self.dscp = byte_header[1] & 0b11111100 # First 6 bits.
        self.ecn = byte_header[1] & 0b00000011 # Last 2 bits.
        self.total_length = int.from_bytes(byte_header[2 : 4], "big")
        self.identification = int.from_bytes(byte_header[4 : 6], "big")
        self.flags = byte_header[6] & 0b11100000 # First 3 bits.
        self.fragment_offset = int.from_bytes(byte_header[6 : 8], "big")
        self.fragment_offset &= 0b0001111111111111 # Last 13 bits.
        self.ttl = byte_header[8]
        self.protocol = byte_header[9]
        self.checksum = int.from_bytes(byte_header[10 : 12], "big")
        self.source_address = int.from_bytes(byte_header[12 : 16], "big")
        self.destination_address = int.from_bytes(byte_header[16 : 20], "big")

        # NOTE: There's an additional field, "options", but this layer's
        # specification did not make any use of it (i.e. it will always
        # be non-existant in this case) so I chose not to include it here.

        # Copy.
        self.original_byte_data = deepcopy(byte_header)

        return self

class UDPHeader:
    @classmethod
    def from_bytes(cls, byte_header: bytes):
        # Create instance.
        self = cls()

        self.source_port = int.from_bytes(byte_header[0 : 2], "big")
        self.destination_port = int.from_bytes(byte_header[2 : 4], "big")
        self.length = int.from_bytes(byte_header[4 : 6], "big")
        self.checksum = int.from_bytes(byte_header[6 : 8], "big")

        # Copy.
        self.original_byte_data = deepcopy(byte_header)

        return self

# NOTE: "byte_data" argument's length must be a multiple of 2 bytes.
def verify_checksum(byte_data: bytes):
    checksum = 0

    for i in range(0, len(byte_data), 2):
        # Convert the big-endian 16-bit value into an "int" object represented
        # in the OS endianness. This does not affect the final result.
        word = int.from_bytes(byte_data[i : i + 2], "big")

        # Add 16-bit value.
        checksum += word

    # Add carry bit. This is analogous to adding 1 if the carry bit is set,
    # and 0 otherwise.
    # NOTE: I did not come up with this idea. I found it on the Internet,
    # but I don't remember where.
    checksum += (checksum >> 16)

    # Discard excess bits, keeping only the first 16.
    checksum = (checksum & 0b1111111111111111)

    # Flip all bits.
    checksum = (checksum ^ 0b1111111111111111)

    return (checksum == 0)

# Returns an UDP packet (header + data) preceeded by a "pseudo" IPv4 header.
def build_pseudo_udp_packet(ipv4_header: IPv4Header, udp_header: UDPHeader, udp_data: bytes):
    byte_result = bytearray()

    # -- IPV4 PSEUDO HEADER
    byte_result += ipv4_header.source_address.to_bytes(4, "big")
    byte_result += ipv4_header.destination_address.to_bytes(4, "big")

    byte_result += ipv4_header.protocol.to_bytes(2, "big")
    byte_result += udp_header.length.to_bytes(2, "big")

    # -- UDP HEADER
    byte_result += udp_header.source_port.to_bytes(2, "big")
    byte_result += udp_header.destination_port.to_bytes(2, "big")
    byte_result += udp_header.length.to_bytes(2, "big")
    byte_result += udp_header.checksum.to_bytes(2, "big")

    # -- UDP DATA
    byte_result += udp_data

    # Pad result to 2-bytes.
    while (len(byte_result) % 2) != 0:
        byte_result.append(0)

    return byte_result

def ipv4_checksum_is_ok(ipv4_header: IPv4Header):
    return verify_checksum(ipv4_header.original_byte_data)

def udp_checksum_is_ok(ipv4_header: IPv4Header, udp_header: UDPHeader, udp_data: bytes):
    # Reconstruct the packet using the pseudo IPv4 information as noted
    # in Wikipedia.
    pseudo_packet = build_pseudo_udp_packet(ipv4_header, udp_header, udp_data)

    return verify_checksum(pseudo_packet)

def packet_is_ok(ipv4_header: IPv4Header, udp_header: UDPHeader, udp_data: bytes):
    if not ipv4_checksum_is_ok(ipv4_header):
        return False

    if not udp_checksum_is_ok(ipv4_header, udp_header, udp_data):
        return False

    expected_source_address = bytes([10, 1, 1, 10]) # 10.1.1.10
    expected_destination_address = bytes([10, 1, 1, 200]) # 10.1.1.200
    expected_destination_port = 42069

    source_address = ipv4_header.source_address.to_bytes(4, "big")
    destination_address = ipv4_header.destination_address.to_bytes(4, "big")
    destination_port = udp_header.destination_port

    if source_address != expected_source_address:
        return False

    if destination_address != expected_destination_address:
        return False

    if destination_port != expected_destination_port:
        return False

    return True

# NOTE: Since Python passes parameters by object reference, and since "bytes" is
# an immutable object, no copy is needed because the original data is never
# modified.
def decode(byte_data: bytes):
    byte_result = bytearray()

    while len(byte_data) > 0:
        # NOTE: I know that the IPv4 header may have a different width in real
        # situations; however, the instructions said that in this case, it is
        # ALWAYS 20 bytes long.
        ipv4_header = IPv4Header.from_bytes(byte_data[0 : 20])
        udp_header = UDPHeader.from_bytes(byte_data[20 : 28])

        # NOTE: We subtract 8 since that's the length of the UDP header.
        udp_data = byte_data[28 : 28 + (udp_header.length - 8)]

        # Move on. The IPv4 header's total length field contains the size of
        # the IPv4 header + UDP header + Payload.
        byte_data = byte_data[ipv4_header.total_length : len(byte_data)]

        if packet_is_ok(ipv4_header, udp_header, udp_data):
            byte_result += udp_data

    return byte_result
