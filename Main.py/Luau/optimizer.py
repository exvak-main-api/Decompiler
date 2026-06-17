from ast import *


class Optimizer:

    def optimize(self, node):

        if isinstance(node, Block):

            new_body = []

            for child in node.body:

                optimized = self.optimize(child)

                if optimized:
                    new_body.append(optimized)

            node.body = new_body
            return node

        if isinstance(node, Assignment):

            if isinstance(node.value, Identifier):

                if node.target.name == node.value.name:
                    return None

            return node

        if isinstance(node, BinaryOp):

            left = self.optimize(node.left)
            right = self.optimize(node.right)

            node.left = left
            node.right = right

            if isinstance(left, Constant) and isinstance(right, Constant):

                try:
                    if node.op == "+":
                        return Constant(left.value + right.value)

                    if node.op == "-":
                        return Constant(left.value - right.value)

                    if node.op == "*":
                        return Constant(left.value * right.value)

                    if node.op == "/":
                        return Constant(left.value / right.value)

                    if node.op == "%":
                        return Constant(left.value % right.value)

                    if node.op == "^":
                        return Constant(left.value ** right.value)
                except:
                    pass

            return node

        if isinstance(node, UnaryOp):

            value = self.optimize(node.value)

            node.value = value

            if isinstance(value, Constant):

                try:
                    if node.op.strip() == "not":
                        return Constant(not value.value)

                    if node.op == "#":
                        return Constant(len(value.value))

                except:
                    pass

            return node

        if isinstance(node, If):

            node.condition = self.optimize(node.condition)
            node.body = self.optimize(node.body)
            node.else_body = self.optimize(node.else_body)

            return node

        if isinstance(node, While):

            node.condition = self.optimize(node.condition)
            node.body = self.optimize(node.body)

            return node

        if isinstance(node, NumericFor):

            node.start = self.optimize(node.start)
            node.finish = self.optimize(node.finish)
            node.step = self.optimize(node.step)
            node.body = self.optimize(node.body)

            return node

        if isinstance(node, Return):

            node.value = self.optimize(node.value)

            return node

        if isinstance(node, Call):

            node.func = self.optimize(node.func)
            node.args = [self.optimize(a) for a in node.args]

            return node

        return node
