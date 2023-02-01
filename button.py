class Button:
    left: int
    top: int
    height: int
    width: int
    text: str
    is_disabled: bool

    def __init__(self, text: str):
        self.text = text
        self.is_disabled = False

    def is_under_cursor(self, cursor_pos_x: int, cursor_pos_y: int):
        if self.is_disabled:
            return False
        x_in_zone = cursor_pos_x >= self.left and cursor_pos_x <= self.left + self.width
        y_in_zone = cursor_pos_y >= self.top and cursor_pos_y <= self.top + self.height
        return x_in_zone and y_in_zone
