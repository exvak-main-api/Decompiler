# function_rebuilder.py

from ast import *


class FunctionRebuilder:

    def rebuild(self, node):

        if isinstance(node, Block):

            new_body = []
            i = 0

            while i < len(node.body):

                ins = node.body[i]

                # detect function start pattern (very simplified)
                if (
                    isinstance(ins, Assignment)
                    and isinstance(ins.value, Constant)
                    and str(ins.value.value).startswith("function")
                ):

                    func_name = ins.target.name

                    func = Function(
                        name=func_name,
                        args=[],
                        body=Block()
                    )

                    i += 1

                    while i < len(node.body):

                        inner = node.body[i]

                        # crude end detection
                        if isinstance(inner, Return):
                            func.body.add(inner)
                            i += 1
                            break

                        func.body.add(inner)
                        i += 1

                    new_body.append(func)
                    continue

                new_body.append(self.rebuild(ins))
                i += 1

            node.body = new_body
            return node

        if isinstance(node, If):
            node.condition = self.rebuild(node.condition)
            node.body = self.rebuild(node.body)
            node.else_body = self.rebuild(node.else_body)
            return node

        if isinstance(node, While):
            node.condition = self.rebuild(node.condition)
            node.body = self.rebuild(node.body)
            return node

        if isinstance(node, Assignment):
            node.value = self.rebuild(node.value)
            return node

        if isinstance(node, Return):
            node.value = self.rebuild(node.value)
            return node

        if isinstance(node, Call):
            node.func = self.rebuild(node.func)
            node.args = [self.rebuild(a) for a in node.args]
            return node

        return node
