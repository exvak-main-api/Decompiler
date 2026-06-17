from analyzer import Analyzer
from controlflow import ControlFlowAnalyzer
from generator import Generator
from ast import *


class Decompiler:

    def __init__(self):

        self.analyzer = Analyzer()

        self.controlflow = ControlFlowAnalyzer()

        self.generator = Generator()

    def make_identifier(self, reg):

        return Identifier(f"v{reg}")

    def make_constant(self, value):

        return Constant(value)

    def build_ast(self, proto):

        root = Block()

        registers = {}

        for ins in proto.instructions:

            op = ins.opcode

            # LOADNIL
            if op == 2:

                registers[ins.a] = Constant(None)

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        Constant(None)
                    )
                )

            # LOADB
            elif op == 3:

                value = bool(ins.b)

                registers[ins.a] = Constant(value)

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        Constant(value)
                    )
                )

            # LOADN
            elif op == 4:

                registers[ins.a] = Constant(ins.c)

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        Constant(ins.c)
                    )
                )

            # LOADK
            elif op == 5:

                value = Constant(f"K{ins.c}")

                registers[ins.a] = value

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        value
                    )
                )

            # MOVE
            elif op == 6:

                value = registers.get(
                    ins.b,
                    Identifier(f"v{ins.b}")
                )

                registers[ins.a] = value

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        value
                    )
                )

            # ADD
            elif op == 20:

                expr = BinaryOp(
                    registers.get(
                        ins.b,
                        Identifier(f"v{ins.b}")
                    ),
                    "+",
                    registers.get(
                        ins.c,
                        Identifier(f"v{ins.c}")
                    )
                )

                registers[ins.a] = expr

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        expr
                    )
                )

            # SUB
            elif op == 21:

                expr = BinaryOp(
                    registers.get(
                        ins.b,
                        Identifier(f"v{ins.b}")
                    ),
                    "-",
                    registers.get(
                        ins.c,
                        Identifier(f"v{ins.c}")
                    )
                )

                registers[ins.a] = expr

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        expr
                    )
                )

            # MUL
            elif op == 22:

                expr = BinaryOp(
                    registers.get(
                        ins.b,
                        Identifier(f"v{ins.b}")
                    ),
                    "*",
                    registers.get(
                        ins.c,
                        Identifier(f"v{ins.c}")
                    )
                )

                registers[ins.a] = expr

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        expr
                    )
                )

            # DIV
            elif op == 23:

                expr = BinaryOp(
                    registers.get(
                        ins.b,
                        Identifier(f"v{ins.b}")
                    ),
                    "/",
                    registers.get(
                        ins.c,
                        Identifier(f"v{ins.c}")
                    )
                )

                registers[ins.a] = expr

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        expr
                    )
                )

            # MOD
            elif op == 24:

                expr = BinaryOp(
                    registers.get(
                        ins.b,
                        Identifier(f"v{ins.b}")
                    ),
                    "%",
                    registers.get(
                        ins.c,
                        Identifier(f"v{ins.c}")
                    )
                )

                registers[ins.a] = expr

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        expr
                    )
                )

            # POW
            elif op == 25:

                expr = BinaryOp(
                    registers.get(
                        ins.b,
                        Identifier(f"v{ins.b}")
                    ),
                    "^",
                    registers.get(
                        ins.c,
                        Identifier(f"v{ins.c}")
                    )
                )

                registers[ins.a] = expr

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        expr
                    )
                )

            # NOT
            elif op == 31:

                expr = UnaryOp(
                    "not ",
                    registers.get(
                        ins.b,
                        Identifier(f"v{ins.b}")
                    )
                )

                registers[ins.a] = expr

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        expr
                    )
                )

            # LEN
            elif op == 32:

                expr = UnaryOp(
                    "#",
                    registers.get(
                        ins.b,
                        Identifier(f"v{ins.b}")
                    )
                )

                registers[ins.a] = expr

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        expr
                    )
                )

            # CONCAT
            elif op == 33:

                expr = BinaryOp(
                    registers.get(
                        ins.b,
                        Identifier(f"v{ins.b}")
                    ),
                    "..",
                    registers.get(
                        ins.c,
                        Identifier(f"v{ins.c}")
                    )
                )

                registers[ins.a] = expr

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        expr
                    )
                )

            # NEWTABLE
            elif op == 17:

                tbl = Table()

                registers[ins.a] = tbl

                root.add(
                    Assignment(
                        Identifier(f"v{ins.a}"),
                        tbl
                    )
                )

            # CALL
            elif op == 46:

                root.add(
                    Call(
                        registers.get(
                            ins.a,
                            Identifier(f"v{ins.a}")
                        ),
                        []
                    )
                )

            # RETURN
            elif op == 48:

                root.add(
                    Return(
                        registers.get(
                            ins.a,
                            Identifier(f"v{ins.a}")
                        )
                    )
                )

        return root

    def decompile(self, proto):

        tree = self.build_ast(proto)

        return self.generator.generate(tree)

    def decompile_chunk(self, chunk):

        return self.decompile(
            chunk.main_proto
          )
