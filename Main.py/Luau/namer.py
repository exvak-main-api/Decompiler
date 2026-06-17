from ast import *


class Namer:

    def __init__(self):
        self.names = {}
        self.counter = 0

    def fresh(self, hint="v"):
        name = f"{hint}{self.counter}"
        self.counter += 1
        return name

    def name_register(self, reg):
        if reg not in self.names:
            self.names[reg] = self.fresh("v")
        return self.names[reg]

    def rename(self, node):

        if isinstance(node, Block):
            node.body = [self.rename(n) for n in node.body]
            return node

        if isinstance(node, Assignment):

            if isinstance(node.target, Identifier) and node.target.name.startswith("v"):

                node.target.name = self.name_register(node.target.name)

            node.value = self.rename(node.value)
            return node

        if isinstance(node, Return):
            node.value = self.rename(node.value)
            return node

        if isinstance(node, BinaryOp):
            node.left = self.rename(node.left)
            node.right = self.rename(node.right)
            return node

        if isinstance(node, UnaryOp):
            node.value = self.rename(node.value)
            return node

        if isinstance(node, Call):
            node.func = self.rename(node.func)
            node.args = [self.rename(a) for a in node.args]
            return node

        if isinstance(node, If):
            node.condition = self.rename(node.condition)
            node.body = self.rename(node.body)
            node.else_body = self.rename(node.else_body)
            return node

        if isinstance(node, While):
            node.condition = self.rename(node.condition)
            node.body = self.rename(node.body)
            return node

        if isinstance(node, NumericFor):
            node.start = self.rename(node.start)
            node.finish = self.rename(node.finish)
            node.step = self.rename(node.step)
            node.body = self.rename(node.body)
            return node

        if isinstance(node, GenericFor):
            node.iterator = self.rename(node.iterator)
            node.body = self.rename(node.body)
            return node

        return node
