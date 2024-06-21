from typing import Any

class Table:

    def __init__(self, col_names: list[str], rows: list[list[Any]]) -> None:
        self.col_names = col_names
        self.rows = rows

    def get(self, col_name: str, row_index: int) -> Any:
        if col_name == '*':
            return self.get_all(row_index)
        if col_name not in self.col_names:
            raise Exception(f'Column [{col_name}] not found')
        if row_index < 0 or row_index >= len(self.rows):
            raise Exception(f'Wrong row index [{row_index}]')
        col_index = self.col_names.index(col_name)
        return self.rows[row_index][col_index]
    
    def get_all(self, row_index: int) -> list[Any]:
        if row_index < 0 or row_index >= len(self.rows):
            raise Exception(f'Wrong row index [{row_index}]')
        return self.rows[row_index]