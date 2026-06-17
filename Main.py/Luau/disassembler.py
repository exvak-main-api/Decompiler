from opcodes import get_opcode


class Disassembler:

    def __init__(self):
        pass

    def disassemble_instruction(self, ins):

        op = get_opcode(ins.opcode)

        return (
            f"{ins.pc:04X} "
            f"{op.name:<16} "
            f"A={ins.a:<3} "
            f"B={ins.b:<3} "
            f"C={ins.c:<3}"
        )

    def disassemble_proto(self, proto):

        lines = []

        for ins in proto.instructions:
            lines.append(
                self.disassemble_instruction(ins)
            )

        return "\n".join(lines)
