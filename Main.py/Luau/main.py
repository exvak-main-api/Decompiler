from parser import ChunkParser
from decompiler import Decompiler
from optimizer import Optimizer


def load_file(path):
    with open(path, "rb") as f:
        return f.read()


def main():

    data = load_file("sample.luau")

    chunk = ChunkParser(data).parse()

    decompiler = Decompiler()
    optimizer = Optimizer()

    ast_tree = decompiler.build_ast(chunk.main_proto)

    optimized = optimizer.optimize(ast_tree)

    if optimized is None:
        print("-- empty output")
        return

    output = decompiler.generator.generate(optimized)

    print(output)


if __name__ == "__main__":
    main()
