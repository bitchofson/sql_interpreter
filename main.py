import os
import sqlparser.mel_parser
from sqlexecute.table import Table
from sqlexecute.context import Context
from sqlexecute.intepreter import SQLInterpreter

def test_1(context: Context, interpreter: SQLInterpreter):
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

    sql_query = '''select * from table_1 where col1=1 '''
    prog = sqlparser.mel_parser.parse(sql_query) 
    print(*prog.tree, sep=os.linesep)
    print(interpreter.execute(prog, context))

def test_2(context: Context, interpreter: SQLInterpreter):
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
    sql_query = '''select name from table_2 where age >= 18 order by name'''
    prog = sqlparser.mel_parser.parse(sql_query)  

    context.curr_table = table_2
    context.tables['table_2'] = table_2

    print(interpreter.execute(prog, context))

def test_3(context: Context, interpreter: SQLInterpreter):
    table_3 = Table(
        col_names=['apple', 'banana'],
        rows=[
            [18, 5],
            [14, 87],
            [32, 32],
            [2, 8],
            [11, 12]
        ]
    )
    sql_query = '''select apple from table_3 where apple >= 4'''
    prog = sqlparser.mel_parser.parse(sql_query)  

    context.curr_table = table_3
    context.tables['table_3'] = table_3

    print(interpreter.execute(prog, context))


def main():
    
    context = Context()
    interpreter = SQLInterpreter() 

    #test_1(context=context, interpreter=interpreter)
    #test_2(context=context, interpreter=interpreter)
    #test_3(context=context, interpreter=interpreter)
    

    
if __name__ == '__main__':
    main()