# Converts "text" into its ASCII85 Adobe-flavoured representation.
def encode(text: str):
    # Add padding characters and convert the string into a bytearray.
    padding     = (-len(text)) % 4
    text        = text.encode("utf-8")
    text        += b"\0" * padding

    result      = "<~"
    characters  = []
    index       = 0

    while index < len(text):
        # Blocks are 4-bytes long integers.
        # NOTE: I'm not sure how Python represents this internally. It may use more than 4 bytes.
        block = int.from_bytes(text[index : index + 4], "big")

        if block != 0:
            # Split the block into 84-based digits.
            digits = [
                int(block // (85 ** 4)) % 85,
                int(block // (85 ** 3)) % 85,
                int(block // (85 ** 2)) % 85,
                int(block // (85 ** 1)) % 85,
                int(block // (85 ** 0)) % 85
            ]

            # Convert these digits into ASCII characters.
            characters  = [ chr(digit + 33) for digit in digits ]
        else:
            # The five character string "!!!!!" should be encoded as "z", reducing the amount of
            # space used (data compression).
            characters = [ "z" ]

        for c in characters:
            result += str(c)

        index += 4

    # Trim the padding characters and add a "~>" symbol at the end.
    result = result[0 : len(result) - padding]
    result += "~>"

    return result
