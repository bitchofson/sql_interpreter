from .table import Table

class Context:
    def __init__(self) -> None:
        self.tables: map[str, Table] = {}
        self.curr_table: Table | None = None
        self.curr_row_index = 0

    def get_table(self, name: str) -> Table:
        if name not in self.tables:
            raise Exception(f'Table {name} not found')
        return self.tables[name]
    
    def get_value(self, name: str) -> Table:
        if not self.curr_table:
            raise Exception(f'No table data in context')
        return self.curr_table.get(name, self.curr_row_index)
    
    def next_row(self):
        self.curr_row_index += 1

    def is_end(self):
        if not self.curr_table:
            return True
        return self.curr_row_index >= len(self.curr_table.rows)
