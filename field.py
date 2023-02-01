from enum import Enum

BOARD_SIZE = 0

DIRECTION_DOWN = 1
DIRECTION_RIGHT = 2


class CellType(Enum):
    EMPTY = 1
    VALUE = 2
    SUM = 3


class Cell:
    cellType: CellType
    value: int

    def __init__(self, cell_type: CellType, value: int):
        self.cellType = cell_type
        self.value = value


class SumCell(Cell):
    direction: int

    def __init__(self, direction: int, value: int):
        super().__init__(CellType.SUM, value)
        self.direction = direction
        self.value = value


class ValueCell(Cell):
    def __init__(self, value: int):
        super().__init__(CellType.VALUE, value)


def create_field(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    initial_field = []

    for line in lines:
        parts = line.strip().split(' ')
        row = []
        for part in parts:
            if part.endswith('a'):
                part = part.replace('a', '')
                value = int(part)
                row.append(SumCell(1, value))
            elif part.endswith('b'):
                part = part.replace('b', '')
                value = int(part)
                row.append(SumCell(2, value))
            elif part == '0':
                row.append(Cell(CellType.VALUE, 0))
            else:
                row.append(Cell(CellType.EMPTY, -1))
        initial_field.append(row)
    global BOARD_SIZE
    BOARD_SIZE = len(initial_field)
    return initial_field


def is_array_solved(array: list[int], summa: int):
    if 0 in array:
        return False
    all_unique = len(array) == len(set(array))
    if not all_unique:
        return False
    if sum(array) == summa:
        return True
    return False


def is_array_broken(array: list[int], summa: int):
    res = [i for i in array if i != 0]
    all_unique = len(res) == len(set(res))
    if not all_unique:
        return True
    if sum(res) > summa:
        return True
    help_help = sum(res) + (len(array)-len(res)) * 9
    if help_help < summa:
        return True
    return False


class Board:
    board: list[list[Cell]]

    field_names = ["field_3x3_easy.txt", "field_3x3.txt", "field_4x4.txt", "field_5x5.txt", "field_unsolved.txt"]
    field_idx = 0

    def __init__(self):
        self.load_next_field()

    def load_next_field(self):
        self.board: list[list[Cell]] = create_field(
            self.field_names[self.field_idx])
        self.field_idx += 1
        if self.field_idx > 4:
            self.field_idx = 0

    def is_solved(self):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if type(cell) == SumCell:
                    values = []
                    if cell.direction == 1:
                        start_y = i + 1
                        for k in range(start_y, BOARD_SIZE):
                            value_cell = self.board[k][j]
                            if value_cell.value == -1 or value_cell.value > 9:
                                break
                            values.append(value_cell.value)
                    else:
                        start_x = j + 1
                        for k in range(start_x, BOARD_SIZE):
                            value_cell = self.board[i][k]
                            if value_cell.value == -1 or value_cell.value > 9:
                                break
                            values.append(value_cell.value)
                    is_current_array_solved = is_array_solved(
                        values, cell.value)
                    if not is_current_array_solved:
                        return False
        return True

    def check_if_broken(self):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if type(cell) == SumCell:
                    values = []
                    if cell.direction == 1:
                        start_y = i + 1
                        for k in range(start_y, BOARD_SIZE):
                            value_cell = self.board[k][j]
                            if value_cell.value == -1 or value_cell.value > 9:
                                break
                            values.append(value_cell.value)
                    else:
                        start_x = j + 1
                        for k in range(start_x, BOARD_SIZE):
                            value_cell = self.board[i][k]
                            if value_cell.value == -1 or value_cell.value > 9:
                                break
                            values.append(value_cell.value)
                    is_current_array_broken = is_array_broken(
                        values, cell.value)
                    if is_current_array_broken:
                        return True
        return False
