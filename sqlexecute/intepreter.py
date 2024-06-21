from sqlparser.mel_ast import *
from .context import Context
from typing import Any


class SQLInterpreter:

    def execute(self, node: AstNode, context: Context) -> Any | None:
        if isinstance(node, NumNode):
            return self.executeNumNode(node, context)
        if isinstance(node, IdentNode):
            return self.executeIdentNode(node, context)
        if isinstance(node, BinOpNode):
            return self.executeBinOpNode(node, context)
        if isinstance(node, AsExprNode):
            return self.executeAsExprNode(node, context)
        if isinstance(node, ExprListNode):
            return self.executeExprListNode(node, context)
        if isinstance(node, CallNode):
            return self.executeCallNode(node, context)
        if isinstance(node, WhereClauseNode):
            return self.executeWhereClauseNode(node, context)
        if isinstance(node, GroupClauseNode):
            return self.executeGroupClauseNode(node, context)
        if isinstance(node, HavingClauseNode):
            return self.executeHavingClauseNode(node, context)
        if isinstance(node, OrderClauseNode):
            return self.executeOrderClauseNode(node, context)
        if isinstance(node, SelectNode):
            return self.executeSelectNode(node, context)
        if isinstance(node, StrNode):
            return self.executeStrNode(node, context)
        if isinstance(node, OrderExprNode):
            return self.executeOrderExprNode(node, context)
        if isinstance(node, OrderExprListNode):
            return self.executeOrderExprListNode(node, context)
        raise Exception(f'Unsupported node type: {type(node)}')

    def executeAsExprNode(self, node: AsExprNode, context: Context) -> Any:
        return self.execute(node.expr, context)

    def executeExprListNode(self, node: ExprListNode, context: Context) -> list:
        return [self.execute(expr, context) for expr in node.exprs]

    def executeCallNode(self, node: CallNode, context: Context) -> Any:
        raise NotImplementedError('CallNode execution not implemented yet')

    def executeWhereClauseNode(self, node: WhereClauseNode, context: Context) -> list:
        result = []
        for i in range(len(context.curr_table.rows)):
            context.curr_row_index = i
            if self.execute(node.exprs[0], context):
                result.append(context.curr_table.rows[i])
        return result

    def executeGroupClauseNode(self, node: GroupClauseNode, context: Context) -> dict:
        grouped_rows = {}
        for row in context.curr_table.rows:
            context.curr_row_index = context.curr_table.rows.index(row)
            key = tuple(self.execute(expr, context) for expr in node.exprs)
            if key not in grouped_rows:
                grouped_rows[key] = []
            grouped_rows[key].append(row)
        return grouped_rows

    def executeHavingClauseNode(self, node: HavingClauseNode, context: Context) -> Any:
        raise NotImplementedError('HavingClauseNode execution not implemented yet')

    def executeOrderExprNode(self, node: OrderExprNode, context: Context) -> tuple:
        value = self.execute(node.expr, context)
        is_desc = node.order and node.order.upper() == 'DESC'
        return value, is_desc

    def executeOrderExprListNode(self, node: OrderExprListNode, context: Context) -> list:
        return [self.execute(order_expr, context) for order_expr in node.order_exprs]

    def executeOrderClauseNode(self, node: OrderClauseNode, context: Context) -> Any:
        def key_func(row):
            context.curr_row_index = context.curr_table.rows.index(row)
            # Получаем значения и направления сортировки
            sort_keys = []
            for expr in node.order_exprs:
                value, is_desc = self.execute(expr, context)[0]
                sort_keys.append((value, is_desc))
            return sort_keys

        sorted_rows = sorted(context.curr_table.rows, key=lambda row: [val for val, _ in key_func(row)], reverse=False)
        # Корректируем порядок в зависимости от направления
        for idx, expr in enumerate(node.order_exprs):
            is_desc = self.execute(expr, context)[0][1]
            if is_desc:
                sorted_rows = sorted(sorted_rows, key=lambda row: key_func(row)[idx][0], reverse=True)

        return sorted_rows

    def executeSelectNode(self, node: SelectNode, context: Context) -> Any:
        context.curr_table = context.get_table(node.tables.name)
        if isinstance(node.where, WhereClauseNode):
            result_rows = self.execute(node.where, context)
        else:
            result_rows = context.curr_table.rows

        if isinstance(node.group_by, GroupClauseNode):
            context.curr_table.rows = result_rows
            grouped_rows = self.execute(node.group_by, context)
            result_rows = []
            for key, group in grouped_rows.items():
                context.curr_group_rows = group
                context.curr_row_index = 0  # Инициализируем для агрегации
                # Для каждой группы собираем агрегированные данные (здесь можно выполнять агрегатные функции)
                result_rows.append([self.execute(expr, context) for expr in node.selects.exprs])
        else:
            context.curr_group_rows = None

        if isinstance(node.order_by, OrderClauseNode):
            context.curr_table.rows = result_rows
            result_rows = self.execute(node.order_by, context)

        result = []
        for row in result_rows:
            context.curr_row_index = context.curr_table.rows.index(row)
            row_result = []
            for expr in node.selects.exprs:
                executed_value = self.execute(expr, context)
                if isinstance(expr, IdentNode) and expr.name == '*':
                    row_result.extend(executed_value)  # Добавляем элементы напрямую
                else:
                    row_result.append(executed_value)
            result.append(row_result)

        return result

    def executeNumNode(self, node: NumNode, context: Context) -> int | float:
        return node.num

    def executeIdentNode(self, node: IdentNode, context: Context) -> Any:
        return context.curr_table.get(node.name, context.curr_row_index)

    def executeBinOpNode(self, node: BinOpNode, context: Context) -> Any:
        arg1 = self.execute(node.arg1, context)
        arg2 = self.execute(node.arg2, context)
        if node.op == BinOp.ADD:
            return arg1 + arg2
        if node.op == BinOp.SUB:
            return arg1 - arg2
        if node.op == BinOp.MUL:
            return arg1 * arg2
        if node.op == BinOp.DIV:
            return arg1 / arg2
        if node.op == BinOp.GT:
            return arg1 > arg2
        if node.op == BinOp.GE:
            return arg1 >= arg2
        if node.op == BinOp.LT:
            return arg1 < arg2
        if node.op == BinOp.LE:
            return arg1 <= arg2
        if node.op == BinOp.EQ:
            return arg1 == arg2
        if node.op == BinOp.NEQ:
            return arg1 != arg2
        if node.op == BinOp.AND:
            return arg1 and arg2
        if node.op == BinOp.OR:
            return arg1 or arg2
        if node.op == BinOp.LIKE:
            return str(arg1) in str(arg2)
        raise Exception(f'Unsupported binary operator: {node.op}')

    def executeStrNode(self, node: StrNode, context: Context) -> str:
        return node.value
