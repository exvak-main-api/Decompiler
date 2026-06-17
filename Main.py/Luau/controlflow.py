from ast import *


class ControlFlowAnalyzer:

    def __init__(self):
        self.instructions = []
        self.length = 0

    def analyze(self, proto):

        self.instructions = proto.instructions
        self.length = len(self.instructions)

        root = Block()

        pc = 0

        while pc < self.length:

            ins = self.instructions[pc]

            op = ins.opcode

            # JMP
            if op in (34, 35):

                root.add(
                    Jump(
                        getattr(ins, "d", ins.c)
                    )
                )

            # JMPIF
            elif op == 36:

                root.add(
                    JumpIf(
                        Identifier(f"v{ins.a}"),
                        getattr(ins, "d", ins.c)
                    )
                )

            # JMPIFNOT
            elif op == 37:

                root.add(
                    JumpIfNot(
                        Identifier(f"v{ins.a}"),
                        getattr(ins, "d", ins.c)
                    )
                )

            # JMPIFEQ
            elif op == 38:

                root.add(
                    If(
                        Compare(
                            Identifier(f"v{ins.a}"),
                            "==",
                            Identifier(f"v{ins.b}")
                        )
                    )
                )

            # JMPIFLE
            elif op == 39:

                root.add(
                    If(
                        Compare(
                            Identifier(f"v{ins.a}"),
                            "<=",
                            Identifier(f"v{ins.b}")
                        )
                    )
                )

            # JMPIFLT
            elif op == 40:

                root.add(
                    If(
                        Compare(
                            Identifier(f"v{ins.a}"),
                            "<",
                            Identifier(f"v{ins.b}")
                        )
                    )
                )

            # EQ
            elif op == 41:

                root.add(
                    Compare(
                        Identifier(f"v{ins.b}"),
                        "==",
                        Identifier(f"v{ins.c}")
                    )
                )

            # LT
            elif op == 42:

                root.add(
                    Compare(
                        Identifier(f"v{ins.b}"),
                        "<",
                        Identifier(f"v{ins.c}")
                    )
                )

            # LE
            elif op == 43:

                root.add(
                    Compare(
                        Identifier(f"v{ins.b}"),
                        "<=",
                        Identifier(f"v{ins.c}")
                    )
                )

            # FORNPREP
            elif op == 49:

                node = NumericFor(
                    variable=f"i{ins.a}",
                    start=Identifier(f"v{ins.a}"),
                    finish=Identifier(f"v{ins.a+1}"),
                    step=Identifier(f"v{ins.a+2}")
                )

                root.add(node)

            # FORNLOOP
            elif op == 50:

                root.add(
                    Continue()
                )

            # FORGPREP
            elif op == 51:

                node = GenericFor(
                    variables=[
                        f"v{ins.a}",
                        f"v{ins.a+1}"
                    ],
                    iterator=Identifier(
                        f"v{ins.a+2}"
                    )
                )

                root.add(node)

            # FORGLOOP
            elif op == 52:

                root.add(
                    Continue()
                )

            # RETURN
            elif op == 48:

                root.add(
                    Return(
                        Identifier(
                            f"v{ins.a}"
                        )
                    )
                )

            pc += 1

        return root


class BasicBlock:

    def __init__(self, start):

        self.start = start
        self.end = start

        self.instructions = []

        self.successors = []

        self.predecessors = []

    def add(self, ins):

        self.instructions.append(ins)

        self.end = ins.pc


class CFG:

    def __init__(self):

        self.blocks = []

    def add_block(self, block):

        self.blocks.append(block)

    def get_block(self, pc):

        for block in self.blocks:

            if block.start == pc:
                return block

        return None


class CFGBuilder:

    JUMP_OPS = {
        34,
        35,
        36,
        37,
        38,
        39,
        40
    }

    def build(self, proto):

        cfg = CFG()

        current = BasicBlock(0)

        for ins in proto.instructions:

            current.add(ins)

            if ins.opcode in self.JUMP_OPS:

                cfg.add_block(current)

                current = BasicBlock(
                    ins.pc + 1
                )

            elif ins.opcode == 48:

                cfg.add_block(current)

                current = BasicBlock(
                    ins.pc + 1
                )

        if current.instructions:
            cfg.add_block(current)

        return cfg
