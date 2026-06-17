from parser import ChunkParser
from analyzer import Analyzer

with open("sample.luau", "rb") as f:
    data = f.read()

chunk = ChunkParser(data).parse()

lua_code = Analyzer().analyze(
    chunk.main_proto
)

print(lua_code)
