from field import Cell, Board


initial_field = Board()


class DFS:
    step: int

    def __init__(self):
        self.step = 0

    def dfs(self, field: list[Cell], pos: int, board: Board, draw_board):
        if pos >= len(field):
            return False
        for i in range(1, 10):
            self.step += 1
            cell = field[pos]
            cell.value = i
            draw_board(board)
            if board.is_solved():
                return True
            res = self.dfs(field, pos + 1, board, draw_board)
            if res:
                return True
        return False
