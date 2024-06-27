import os
import sqlparser.mel_parser
from sqlexecute.table import Table
from sqlexecute.context import Context
from sqlexecute.intepreter import SQLInterpreter


def where_test_1(context: Context, interpreter: SQLInterpreter):
    table_1 = Table(
        col_names=['col1', 'col2'],
        rows=[
            [1, 'a'],
            [22, 'b'],
            [3, 'c'],
            [3, 'c']
        ]
    )

    context.curr_table = table_1
    context.tables['table_1'] = table_1

    sql_query = '''select * from table_1 where col1 < 3'''
    prog = sqlparser.mel_parser.parse(sql_query)
    print(*prog.tree, sep=os.linesep)
    print(interpreter.execute(prog, context))

def order_by_test_1(context: Context, interpreter: SQLInterpreter):
    table_2 = Table(
        col_names=['age', 'name'],
        rows=[
            [14, 'bob'],
            [32, 'tom'],
            [2, 'cail'],
            [11, 'sasha'],
            [18, 'alex']
        ]
    )
    sql_query = '''select name from table_2 where age >= 10 order by name asc'''
    prog = sqlparser.mel_parser.parse(sql_query)
    print(*prog.tree, sep=os.linesep)

    context.curr_table = table_2
    context.tables['table_2'] = table_2

    print(interpreter.execute(prog, context))

def group_by_test_1(context: Context, interpreter: SQLInterpreter):
    table_3 = Table(
        col_names=['apple', 'banana'],
        rows=[
            [18, 5],
            [14, 8],
            [32, 32],
            [2, 8],
            [14, 32]
        ]
    )
    sql_query = '''select apple, banana from table_3 group by banana'''
    prog = sqlparser.mel_parser.parse(sql_query)
    print(*prog.tree, sep=os.linesep)

    context.curr_table = table_3
    context.tables['table_3'] = table_3

    print(interpreter.execute(prog, context))

def like_test_1(context: Context, interpreter: SQLInterpreter):
    table_4 = Table(
        col_names=['first_name', 'age'],
        rows=[
            ['John', 31],
            ['Robert', 22],
            ['David', 22],
            ['John', 25],
            ['Betty', 28]
        ]
    )
    sql_query = '''select first_name, age from table_4 where first_name like 'R%' '''
    prog = sqlparser.mel_parser.parse(sql_query)
    print(*prog.tree, sep=os.linesep)

    context.curr_table = table_4
    context.tables['table_4'] = table_4

    print(interpreter.execute(prog, context))


def main():
    context = Context()
    interpreter = SQLInterpreter()

    where_test_1(context=context, interpreter=interpreter)
    order_by_test_1(context=context, interpreter=interpreter)
    group_by_test_1(context=context, interpreter=interpreter)
    like_test_1(context=context, interpreter=interpreter)



if __name__ == '__main__':
    main()
