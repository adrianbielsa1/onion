# To obtain the key, I knew that the first 15 bytes of the actual data would be:
#
#   "==[ Layer 4/6: "
#
# (without the quotation marks). Thus, with the following operation:
#
#   cyphered_data xor actual_data
#
# I was able to obtain the first 15 bytes of the key. Given that the first line of the payload
# is always 60 bytes long, I was able to skip bytes 15...32 (which I did not have the key yet)
# and decode bytes 33...47. Since all of these where "=" signs, I knew that the bytes following
# them would be equal signs too. So I applied the same previous operation, changing the actual
# data to:
#
#   "============="
#
# (without the quotation marks). Doing this, I got the key's bytes in range 15...28. So now
# I was sitting at 28 of the 32 bytes of the key. I decided to go ahead and decode the data,
# writing 4 spaces instead of decoding bytes that I did not have the key for. I ended up
# with an almost readable text, with some words cut. Something like this:
#
#   packets    tain extra data like the des    tion address (where the pack    hould be sent to)
#
# Next, I completed the easiest of these 32-bytes-long blocks, which was the first one. I simply
# had to deduce the missing 4 bytes.
#
#   "==[ Layer 4/6: Network Traff    ============================"
#   "==[ Layer 4/6: Network Traffic ]============================"
#
# and then all that was left was applying the same operation used to get the first 28 bytes
# to the key, now to obtain all of it.
key = bytes([108, 36, 132, 142, 66, 25, 168, 225, 197, 219, 87,
             101, 185, 198, 20, 158, 165, 25, 53, 150, 59, 57,
             127, 165, 101, 209, 254, 1, 133, 125, 217, 76])
