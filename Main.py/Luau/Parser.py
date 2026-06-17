# luau/parser.py

from dataclasses import dataclass, field
from typing import List, Any
import struct


class ParseError(Exception):
    pass


class Reader:
    def __init__(self, data: bytes):
        self.data = memoryview(data)
        self.pos = 0
        self.size = len(data)

    def eof(self):
        return self.pos >= self.size

    def tell(self):
        return self.pos

    def remaining(self):
        return self.size - self.pos

    def seek(self, offset: int):
        if offset < 0 or offset > self.size:
            raise ParseError(f"Invalid seek: {offset}")
        self.pos = offset

    def skip(self, amount: int):
        self.seek(self.pos + amount)

    def require(self, size: int):
        if self.pos + size > self.size:
            raise ParseError(
                f"Unexpected EOF at 0x{self.pos:X}"
            )

    def u8(self):
        self.require(1)
        value = self.data[self.pos]
        self.pos += 1
        return value

    def i8(self):
        self.require(1)
        value = struct.unpack_from("<b", self.data, self.pos)[0]
        self.pos += 1
        return value

    def u16(self):
        self.require(2)
        value = struct.unpack_from("<H", self.data, self.pos)[0]
        self.pos += 2
        return value

    def i16(self):
        self.require(2)
        value = struct.unpack_from("<h", self.data, self.pos)[0]
        self.pos += 2
        return value

    def u32(self):
        self.require(4)
        value = struct.unpack_from("<I", self.data, self.pos)[0]
        self.pos += 4
        return value

    def i32(self):
        self.require(4)
        value = struct.unpack_from("<i", self.data, self.pos)[0]
        self.pos += 4
        return value

    def u64(self):
        self.require(8)
        value = struct.unpack_from("<Q", self.data, self.pos)[0]
        self.pos += 8
        return value

    def i64(self):
        self.require(8)
        value = struct.unpack_from("<q", self.data, self.pos)[0]
        self.pos += 8
        return value

    def f32(self):
        self.require(4)
        value = struct.unpack_from("<f", self.data, self.pos)[0]
        self.pos += 4
        return value

    def f64(self):
        self.require(8)
        value = struct.unpack_from("<d", self.data, self.pos)[0]
        self.pos += 8
        return value

    def bytes(self, size: int):
        self.require(size)
        value = self.data[self.pos:self.pos + size].tobytes()
        self.pos += size
        return value

    def string(self):
        length = self.varint()

        if length == 0:
            return ""

        return self.bytes(length).decode(
            "utf-8",
            errors="replace"
        )

    def peek_u8(self):
        self.require(1)
        return self.data[self.pos]

    def varint(self):
        result = 0
        shift = 0

        while True:
            byte = self.u8()

            result |= (byte & 0x7F) << shift

            if not (byte & 0x80):
                break

            shift += 7

            if shift > 63:
                raise ParseError("Invalid VarInt")

        return result


@dataclass
class Constant:
    type: int
    value: Any


@dataclass
class Instruction:
    pc: int
    raw: int
    opcode: int
    a: int
    b: int
    c: int

    def __repr__(self):
        return (
            f"[{self.pc:04X}] "
            f"OP={self.opcode} "
            f"A={self.a} "
            f"B={self.b} "
            f"C={self.c}"
        )


@dataclass
class Proto:
    max_stack: int = 0
    params: int = 0
    upvalues: int = 0
    vararg: bool = False

    instructions: List[Instruction] = field(
        default_factory=list
    )

    constants: List[Constant] = field(
        default_factory=list
    )

    protos: List["Proto"] = field(
        default_factory=list
    )


@dataclass
class Chunk:
    version: int
    strings: List[str]
    main_proto: Proto


class ChunkParser:

    def __init__(self, data: bytes):
        self.r = Reader(data)

    def parse(self):
        version = self.r.u8()

        strings = self.read_strings()

        main_proto = self.read_proto()

        return Chunk(
            version=version,
            strings=strings,
            main_proto=main_proto
        )

    def read_strings(self):
        count = self.r.varint()

        strings = []

        for _ in range(count):
            strings.append(
                self.r.string()
            )

        return strings

    def read_proto(self):
        proto = Proto()

        proto.max_stack = self.r.u8()
        proto.params = self.r.u8()
        proto.upvalues = self.r.u8()
        proto.vararg = bool(self.r.u8())

        instruction_count = self.r.varint()

        for pc in range(instruction_count):

            raw = self.r.u32()

            opcode = raw & 0xFF
            a = (raw >> 8) & 0xFF
            b = (raw >> 16) & 0xFF
            c = (raw >> 24) & 0xFF

            proto.instructions.append(
                Instruction(
                    pc=pc,
                    raw=raw,
                    opcode=opcode,
                    a=a,
                    b=b,
                    c=c
                )
            )

        constant_count = self.r.varint()

        for _ in range(constant_count):

            ctype = self.r.u8()

            if ctype == 0:
                value = None

            elif ctype == 1:
                value = False

            elif ctype == 2:
                value = True

            elif ctype == 3:
                value = self.r.f64()

            elif ctype == 4:
                value = self.r.string()

            else:
                value = None

            proto.constants.append(
                Constant(
                    type=ctype,
                    value=value
                )
            )

        child_count = self.r.varint()

        for _ in range(child_count):
            proto.protos.append(
                self.read_proto()
            )

        return proto


def load_file(path: str):
    with open(path, "rb") as f:
        return f.read()


if __name__ == "__main__":

    data = load_file("sample.luau")

    parser = ChunkParser(data)

    chunk = parser.parse()

    print("Version:", chunk.version)

    print("Strings:", len(chunk.strings))

    print(
        "Instructions:",
        len(chunk.main_proto.instructions)
    )

    for ins in chunk.main_proto.instructions:
        print(ins)
