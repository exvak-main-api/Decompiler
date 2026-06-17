from parser import ChunkParser
from decompiler import Decompiler
from optimizer import Optimizer
from namer import Namer
from reconstructor import Reconstructor
from function_rebuilder import FunctionRebuilder


def load_file(path):
    with open(path, "rb") as f:
        return f.read()


def main():

    data = load_file("sample.luau")
    chunk = ChunkParser(data).parse()

    decompiler = Decompiler()
    optimizer = Optimizer()
    namer = Namer()
    reconstructor = Reconstructor()
    function_rebuilder = FunctionRebuilder()

    ast_tree = decompiler.build_ast(chunk.main_proto)

    ast_tree = optimizer.optimize(ast_tree)
    ast_tree = namer.rename(ast_tree)
    ast_tree = reconstructor.reconstruct(ast_tree)
    ast_tree = function_rebuilder.rebuild(ast_tree)

    output = decompiler.generator.generate(ast_tree)

    print(output)


if __name__ == "__main__":
    main()
