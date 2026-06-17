from dataclasses import dataclass, field
from typing import List, Any


class Node:
    pass


@dataclass
class Block(Node):
    body: List[Node] = field(default_factory=list)

    def add(self, node):
        self.body.append(node)


@dataclass
class Identifier(Node):
    name: str


@dataclass
class Constant(Node):
    value: Any


@dataclass
class Assignment(Node):
    target: Any
    value: Any


@dataclass
class Return(Node):
    value: Any


@dataclass
class Call(Node):
    func: Any
    args: List[Any] = field(default_factory=list)


@dataclass
class MethodCall(Node):
    obj: Any
    method: str
    args: List[Any] = field(default_factory=list)


@dataclass
class BinaryOp(Node):
    left: Any
    op: str
    right: Any


@dataclass
class UnaryOp(Node):
    op: str
    value: Any


@dataclass
class Index(Node):
    table: Any
    key: Any


@dataclass
class Field(Node):
    table: Any
    field: str


@dataclass
class Table(Node):
    entries: List[Any] = field(default_factory=list)


@dataclass
class TableSet(Node):
    table: Any
    key: Any
    value: Any


@dataclass
class If(Node):
    condition: Any
    body: Block = field(default_factory=Block)
    else_body: Block = field(default_factory=Block)


@dataclass
class While(Node):
    condition: Any
    body: Block = field(default_factory=Block)


@dataclass
class Repeat(Node):
    condition: Any
    body: Block = field(default_factory=Block)


@dataclass
class NumericFor(Node):
    variable: str
    start: Any
    finish: Any
    step: Any
    body: Block = field(default_factory=Block)


@dataclass
class GenericFor(Node):
    variables: List[str]
    iterator: Any
    body: Block = field(default_factory=Block)


@dataclass
class Function(Node):
    name: str
    args: List[str] = field(default_factory=list)
    body: Block = field(default_factory=Block)


@dataclass
class Closure(Node):
    args: List[str] = field(default_factory=list)
    body: Block = field(default_factory=Block)


@dataclass
class Break(Node):
    pass


@dataclass
class Continue(Node):
    pass


@dataclass
class Goto(Node):
    label: str


@dataclass
class Label(Node):
    name: str


@dataclass
class Vararg(Node):
    pass


@dataclass
class Import(Node):
    path: str


@dataclass
class Global(Node):
    name: str


@dataclass
class Upvalue(Node):
    name: str


@dataclass
class LogicalAnd(Node):
    left: Any
    right: Any


@dataclass
class LogicalOr(Node):
    left: Any
    right: Any


@dataclass
class Compare(Node):
    left: Any
    op: str
    right: Any


@dataclass
class Jump(Node):
    target: int


@dataclass
class JumpIf(Node):
    condition: Any
    target: int


@dataclass
class JumpIfNot(Node):
    condition: Any
    target: int


@dataclass
class Proto(Node):
    name: str
    instructions: list = field(default_factory=list)
    constants: list = field(default_factory=list)
    children: list = field(default_factory=list)
