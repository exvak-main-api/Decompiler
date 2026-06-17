from parser import ChunkParser
from disassembler import Disassembler

with open("sample.luau", "rb") as f:
    data = f.read()

chunk = ChunkParser(data).parse()

dis = Disassembler()

print(
    dis.disassemble_proto(
        chunk.main_proto
    )
)
