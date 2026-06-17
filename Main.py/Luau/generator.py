from ast import *


class Generator:

    def __init__(self):
        self.indent = "    "

    def pad(self, depth):
        return self.indent * depth

    def generate(self, node, depth=0):

        if node is None:
            return ""

        if isinstance(node, Block):

            lines = []

            for child in node.body:
                result = self.generate(child, depth)

                if result:
                    lines.append(result)

            return "\n".join(lines)

        if isinstance(node, Identifier):
            return node.name

        if isinstance(node, Constant):

            if node.value is None:
                return "nil"

            if isinstance(node.value, str):
                return repr(node.value)

            if isinstance(node.value, bool):
                return str(node.value).lower()

            return str(node.value)

        if isinstance(node, Vararg):
            return "..."

        if isinstance(node, Global):
            return node.name

        if isinstance(node, Upvalue):
            return node.name

        if isinstance(node, BinaryOp):
            return (
                f"({self.generate(node.left)} "
                f"{node.op} "
                f"{self.generate(node.right)})"
            )

        if isinstance(node, UnaryOp):
            return (
                f"({node.op}"
                f"{self.generate(node.value)})"
            )

        if isinstance(node, LogicalAnd):
            return (
                f"({self.generate(node.left)} "
                f"and "
                f"{self.generate(node.right)})"
            )

        if isinstance(node, LogicalOr):
            return (
                f"({self.generate(node.left)} "
                f"or "
                f"{self.generate(node.right)})"
            )

        if isinstance(node, Compare):
            return (
                f"({self.generate(node.left)} "
                f"{node.op} "
                f"{self.generate(node.right)})"
            )

        if isinstance(node, Index):
            return (
                f"{self.generate(node.table)}"
                f"[{self.generate(node.key)}]"
            )

        if isinstance(node, Field):
            return (
                f"{self.generate(node.table)}"
                f".{node.field}"
            )

        if isinstance(node, Assignment):

            return (
                self.pad(depth)
                + self.generate(node.target)
                + " = "
                + self.generate(node.value)
            )

        if isinstance(node, Return):

            return (
                self.pad(depth)
                + "return "
                + self.generate(node.value)
            )

        if isinstance(node, Call):

            args = ", ".join(
                self.generate(arg)
                for arg in node.args
            )

            return (
                self.pad(depth)
                + self.generate(node.func)
                + "("
                + args
                + ")"
            )

        if isinstance(node, MethodCall):

            args = ", ".join(
                self.generate(arg)
                for arg in node.args
            )

            return (
                self.pad(depth)
                + self.generate(node.obj)
                + ":"
                + node.method
                + "("
                + args
                + ")"
            )

        if isinstance(node, Table):

            values = []

            for entry in node.entries:
                values.append(
                    self.generate(entry)
                )

            return (
                "{"
                + ", ".join(values)
                + "}"
            )

        if isinstance(node, TableSet):

            return (
                self.pad(depth)
                + self.generate(node.table)
                + "["
                + self.generate(node.key)
                + "] = "
                + self.generate(node.value)
            )

        if isinstance(node, If):

            result = (
                self.pad(depth)
                + "if "
                + self.generate(node.condition)
                + " then\n"
            )

            result += self.generate(
                node.body,
                depth + 1
            )

            if node.else_body.body:

                result += (
                    "\n"
                    + self.pad(depth)
                    + "else\n"
                )

                result += self.generate(
                    node.else_body,
                    depth + 1
                )

            result += (
                "\n"
                + self.pad(depth)
                + "end"
            )

            return result

        if isinstance(node, While):

            result = (
                self.pad(depth)
                + "while "
                + self.generate(node.condition)
                + " do\n"
            )

            result += self.generate(
                node.body,
                depth + 1
            )

            result += (
                "\n"
                + self.pad(depth)
                + "end"
            )

            return result

        if isinstance(node, Repeat):

            result = (
                self.pad(depth)
                + "repeat\n"
            )

            result += self.generate(
                node.body,
                depth + 1
            )

            result += (
                "\n"
                + self.pad(depth)
                + "until "
                + self.generate(node.condition)
            )

            return result

        if isinstance(node, NumericFor):

            result = (
                self.pad(depth)
                + f"for {node.variable} = "
                + self.generate(node.start)
                + ", "
                + self.generate(node.finish)
                + ", "
                + self.generate(node.step)
                + " do\n"
            )

            result += self.generate(
                node.body,
                depth + 1
            )

            result += (
                "\n"
                + self.pad(depth)
                + "end"
            )

            return result

        if isinstance(node, GenericFor):

            result = (
                self.pad(depth)
                + "for "
                + ", ".join(node.variables)
                + " in "
                + self.generate(node.iterator)
                + " do\n"
            )

            result += self.generate(
                node.body,
                depth + 1
            )

            result += (
                "\n"
                + self.pad(depth)
                + "end"
            )

            return result

        if isinstance(node, Function):

            result = (
                self.pad(depth)
                + "function "
                + node.name
                + "("
                + ", ".join(node.args)
                + ")\n"
            )

            result += self.generate(
                node.body,
                depth + 1
            )

            result += (
                "\n"
                + self.pad(depth)
                + "end"
            )

            return result

        if isinstance(node, Closure):

            result = (
                "function("
                + ", ".join(node.args)
                + ")\n"
            )

            result += self.generate(
                node.body,
                depth + 1
            )

            result += "\nend"

            return result

        if isinstance(node, Break):
            return self.pad(depth) + "break"

        if isinstance(node, Continue):
            return self.pad(depth) + "continue"

        if isinstance(node, Label):
            return self.pad(depth) + f"::{node.name}::"

        if isinstance(node, Goto):
            return self.pad(depth) + f"goto {node.label}"

        if isinstance(node, Import):
            return node.path

        return f"-- unsupported node {type(node).__name__}"
