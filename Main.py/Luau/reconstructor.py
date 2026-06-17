from ast import *


class Reconstructor:

    def reconstruct(self, node):

        if isinstance(node, Block):

            new_body = []
            i = 0

            while i < len(node.body):

                current = node.body[i]

                # detect simple IF pattern
                if (
                    isinstance(current, Compare)
                    and i + 1 < len(node.body)
                ):

                    next_node = node.body[i + 1]

                    if isinstance(next_node, Block):

                        new_body.append(
                            If(
                                condition=current,
                                body=self.reconstruct(next_node),
                                else_body=Block()
                            )
                        )

                        i += 2
                        continue

                new_body.append(self.reconstruct(current))
                i += 1

            node.body = new_body
            return node

        if isinstance(node, If):
            node.condition = self.reconstruct(node.condition)
            node.body = self.reconstruct(node.body)
            node.else_body = self.reconstruct(node.else_body)
            return node

        if isinstance(node, While):
            node.condition = self.reconstruct(node.condition)
            node.body = self.reconstruct(node.body)
            return node

        if isinstance(node, NumericFor):
            node.start = self.reconstruct(node.start)
            node.finish = self.reconstruct(node.finish)
            node.step = self.reconstruct(node.step)
            node.body = self.reconstruct(node.body)
            return node

        if isinstance(node, GenericFor):
            node.iterator = self.reconstruct(node.iterator)
            node.body = self.reconstruct(node.body)
            return node

        if isinstance(node, BinaryOp):
            node.left = self.reconstruct(node.left)
            node.right = self.reconstruct(node.right)
            return node

        if isinstance(node, UnaryOp):
            node.value = self.reconstruct(node.value)
            return node

        if isinstance(node, Return):
            node.value = self.reconstruct(node.value)
            return node

        if isinstance(node, Assignment):
            node.value = self.reconstruct(node.value)
            return node

        if isinstance(node, Call):
            node.func = self.reconstruct(node.func)
            node.args = [self.reconstruct(a) for a in node.args]
            return node

        return node
