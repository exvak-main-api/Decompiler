# analyzer.py

class Analyzer:

    def __init__(self):
        self.registers = {}
        self.output = []

    def reg(self, index):
        return self.registers.get(index, f"v{index}")

    def setreg(self, index, value):
        self.registers[index] = value

    def emit(self, line):
        self.output.append(line)

    def analyze(self, proto):

        for ins in proto.instructions:

            op = ins.opcode

            # LOADNIL
            if op == 2:
                self.setreg(ins.a, "nil")
                self.emit(
                    f"local v{ins.a} = nil"
                )

            # LOADB
            elif op == 3:
                value = "true" if ins.b else "false"
                self.setreg(ins.a, value)
                self.emit(
                    f"local v{ins.a} = {value}"
                )

            # LOADN
            elif op == 4:
                self.setreg(ins.a, str(ins.c))
                self.emit(
                    f"local v{ins.a} = {ins.c}"
                )

            # LOADK
            elif op == 5:
                value = f"K{ins.c}"
                self.setreg(ins.a, value)
                self.emit(
                    f"local v{ins.a} = {value}"
                )

            # MOVE
            elif op == 6:
                value = self.reg(ins.b)
                self.setreg(ins.a, value)
                self.emit(
                    f"local v{ins.a} = {value}"
                )

            # GETGLOBAL
            elif op == 7:
                value = f"GLOBAL_{ins.c}"
                self.setreg(ins.a, value)
                self.emit(
                    f"local v{ins.a} = {value}"
                )

            # GETUPVAL
            elif op == 9:
                value = f"UPVALUE_{ins.b}"
                self.setreg(ins.a, value)
                self.emit(
                    f"local v{ins.a} = {value}"
                )

            # NEWTABLE
            elif op == 17:
                self.setreg(ins.a, "{}")
                self.emit(
                    f"local v{ins.a} = {{}}"
                )

            # ADD
            elif op == 20:
                expr = f"{self.reg(ins.b)} + {self.reg(ins.c)}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # SUB
            elif op == 21:
                expr = f"{self.reg(ins.b)} - {self.reg(ins.c)}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # MUL
            elif op == 22:
                expr = f"{self.reg(ins.b)} * {self.reg(ins.c)}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # DIV
            elif op == 23:
                expr = f"{self.reg(ins.b)} / {self.reg(ins.c)}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # MOD
            elif op == 24:
                expr = f"{self.reg(ins.b)} % {self.reg(ins.c)}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # POW
            elif op == 25:
                expr = f"{self.reg(ins.b)} ^ {self.reg(ins.c)}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # ADDK
            elif op == 26:
                expr = f"{self.reg(ins.b)} + K{ins.c}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # SUBK
            elif op == 27:
                expr = f"{self.reg(ins.b)} - K{ins.c}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # MULK
            elif op == 28:
                expr = f"{self.reg(ins.b)} * K{ins.c}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # DIVK
            elif op == 29:
                expr = f"{self.reg(ins.b)} / K{ins.c}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # UNM
            elif op == 30:
                expr = f"-{self.reg(ins.b)}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # NOT
            elif op == 31:
                expr = f"not {self.reg(ins.b)}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # LEN
            elif op == 32:
                expr = f"#{self.reg(ins.b)}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # CONCAT
            elif op == 33:
                expr = f"{self.reg(ins.b)} .. {self.reg(ins.c)}"
                self.setreg(ins.a, expr)
                self.emit(
                    f"local v{ins.a} = {expr}"
                )

            # EQ
            elif op == 41:
                self.emit(
                    f"-- if {self.reg(ins.b)} == {self.reg(ins.c)}"
                )

            # LT
            elif op == 42:
                self.emit(
                    f"-- if {self.reg(ins.b)} < {self.reg(ins.c)}"
                )

            # LE
            elif op == 43:
                self.emit(
                    f"-- if {self.reg(ins.b)} <= {self.reg(ins.c)}"
                )

            # CALL
            elif op == 46:
                func = self.reg(ins.a)

                self.emit(
                    f"{func}()"
                )

            # NAMECALL
            elif op == 47:
                self.emit(
                    f"-- method call on v{ins.a}"
                )

            # RETURN
            elif op == 48:
                self.emit(
                    f"return {self.reg(ins.a)}"
                )

            # FORNPREP
            elif op == 49:
                self.emit(
                    "-- numeric for start"
                )

            # FORNLOOP
            elif op == 50:
                self.emit(
                    "-- numeric for end"
                )

            # FORGPREP
            elif op == 51:
                self.emit(
                    "-- generic for start"
                )

            # FORGLOOP
            elif op == 52:
                self.emit(
                    "-- generic for end"
                )

            # NEWCLOSURE
            elif op == 55:
                self.setreg(
                    ins.a,
                    "function() end"
                )

                self.emit(
                    f"local v{ins.a} = function() end"
                )

            # DUPCLOSURE
            elif op == 56:
                self.emit(
                    f"-- duplicate closure {ins.a}"
                )

            # VARARG
            elif op == 58:
                self.setreg(ins.a, "...")
                self.emit(
                    f"local v{ins.a} = ..."
                )

            # GETIMPORT
            elif op == 64:
                value = f"IMPORT_{ins.c}"
                self.setreg(ins.a, value)
                self.emit(
                    f"local v{ins.a} = {value}"
                )

            else:
                self.emit(
                    f"-- unhandled opcode {op}"
                )

        return "\n".join(self.output)
