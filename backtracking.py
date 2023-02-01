from field import Cell, Board

initial_field = Board()


class BackTracking:
    step: int

    def __init__(self):
        self.step = 0

    def back_tracking(self, field: list[Cell], pos: int, board: Board, draw_board):
        if pos >= len(field):
            return False
        for i in range(1, 10):
            self.step += 1
            cell = field[pos]
            old_value = cell.value
            cell.value = i
            draw_board(board)
            if board.is_solved():
                return True
            if board.check_if_broken():
                cell.value = old_value
                continue
            if pos + 1 < len(field):
                res = self.back_tracking(field, pos + 1, board, draw_board)
                if res:
                    return True
                cell.value = old_value
        return False
