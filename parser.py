#!/usr/bin/python3.8
import sys

header_file = "blockchain_headers"
byteorder = sys.byteorder
with open(header_file, "rb") as f:
    block_num = 1
    print("%7s %32s %32s" % ("num", "block time", "block difficulty"))
    while True:
        version = f.read(4)
        if version == "":
            break
        prev_header_hash = f.read(32)
        merkle_root = f.read(32)
        block_time_str = f.read(4)
        difficulty_str = f.read(4)
        nonce = f.read(4)

        version_num = int.from_bytes(version, byteorder)
        block_time = int.from_bytes(block_time_str, byteorder)
        block_difficulty = int.from_bytes(difficulty_str, byteorder)

        print(block_num, ": ", block_time, " ", block_difficulty)

        block_num = block_num + 1
