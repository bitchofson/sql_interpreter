from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional, List
from enum import Enum

class AstNode(ABC):
    @property
    def childs(self) -> Tuple[Optional['AstNode'], ...]:
        return ()

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def tree(self) -> List[str]:  
        res = [str(self)]
        childs = self.childs
        for i, child in enumerate(childs):
            if child is None:
                continue
            ch0, ch = '├', '│'
            if i == len(childs) - 1:
                ch0, ch = '└', ' '
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    def visit(self, func: Callable[['AstNode'], None]) -> None:
        func(self)
        for child in self.childs:
            if child is not None:
                child.visit(func)

    def __getitem__(self, index):
        return self.childs[index] if index < len(self.childs) else None


class ExprNode(AstNode):
    pass


class ValueNode(ExprNode):
    pass


class NumNode(ValueNode):
    def __init__(self, num: float):
        super().__init__()
        self.num = float(num)

    def __str__(self) -> str:
        return str(self.num)


class IdentNode(ValueNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = str(name)

    def __str__(self) -> str:
        return str(self.name)

class StrNode(ValueNode):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return f"'{self.value}'"

class BinOp(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    GT = '>'
    GE = '>='
    LT = '<'
    LE = '<='
    EQ = '='
    NEQ = '<>'
    AND = 'and'
    OR = 'or'
    LIKE = 'like'


class BinOpNode(ExprNode):
    def __init__(self, op: BinOp, arg1: ValueNode, arg2: ValueNode):
        super().__init__()
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.arg1, self.arg2

    def __str__(self) -> str:
        return str(self.op.value)


class AsExprNode(ExprNode):
    def __init__(self, expr: ExprNode, name: IdentNode):
        super().__init__()
        self.expr = expr
        self.name = name

    @property
    def childs(self) -> Tuple[ExprNode, IdentNode]:
        return self.expr, self.name

    def __str__(self) -> str:
        return f'{self.expr} as {self.name}'


class ExprListNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ExprNode, ...]:
        return self.exprs

    def __str__(self) -> str:
        return ', '.join(str(expr) for expr in self.exprs)


class CallNode(AstNode):
    def __init__(self, func: IdentNode, *params: Tuple[ExprNode],
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__()
        self.func = func
        self.params = params

    @property
    def childs(self) -> Tuple[IdentNode, ...]:
        return (self.func,) + self.params

    def __str__(self) -> str:
        return f'{self.func}({", ".join(map(str, self.params))})'


class WhereClauseNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ExprNode, ...]:
        return self.exprs

    def __str__(self) -> str:
        return 'where ' + ' and '.join(str(expr) for expr in self.exprs)


class GroupClauseNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ExprNode, ...]:
        return self.exprs

    def __str__(self) -> str:
        return 'group by ' + ', '.join(str(expr) for expr in self.exprs)


class HavingClauseNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ExprNode, ...]:
        return self.exprs

    def __str__(self) -> str:
        return 'having ' + ' and '.join(str(expr) for expr in self.exprs)

class OrderExprNode(AstNode):
    def __init__(self, expr: ExprNode, order: Optional[str] = None):
        super().__init__()
        self.expr = expr
        self.order = order

    @property
    def childs(self) -> Tuple[ExprNode, ...]:
        return (self.expr,)

    def __str__(self) -> str:
        return f"{str(self.expr)} {self.order.upper() if self.order else 'ASC'}"

class OrderExprListNode(AstNode):
    def __init__(self, *order_exprs: OrderExprNode):
        super().__init__()
        self.order_exprs = order_exprs

    @property
    def childs(self) -> Tuple[OrderExprNode, ...]:
        return self.order_exprs

    def __str__(self) -> str:
        return ', '.join(str(order_expr) for order_expr in self.order_exprs)

class OrderClauseNode(AstNode):
    def __init__(self, *order_exprs: OrderExprNode):
        super().__init__()
        self.order_exprs = order_exprs

    @property
    def childs(self) -> Tuple[OrderExprNode, ...]:
        return self.order_exprs

    def __str__(self) -> str:
        return 'order by ' + ', '.join(str(order_expr) for order_expr in self.order_exprs)



class SelectNode(AstNode):
    def __init__(self, selects: ExprListNode, tables: IdentNode, where: WhereClauseNode=None,
                 group_by: GroupClauseNode=None, having: HavingClauseNode=None, order_by: OrderClauseNode=None):
        super().__init__()
        self.selects = selects
        self.tables = tables
        self.where = where
        self.group_by = group_by
        self.having = having
        self.order_by = order_by

    @property
    def childs(self) -> Tuple[ExprListNode, IdentNode, WhereClauseNode, GroupClauseNode, HavingClauseNode, OrderClauseNode]:
        return self.selects, self.tables, self.where, self.group_by, self.having, self.order_by

    def __str__(self) -> str:
        return 'select'
