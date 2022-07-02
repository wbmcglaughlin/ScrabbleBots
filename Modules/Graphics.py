from raylibpy import Color


class Dimensions:
    def __init__(self, side_length: int, posx: int, posy: int) -> None:
        self.side_length = side_length
        self.posx = posx
        self.posy = posy

class Render:
    def __init__(self, border_thickness: int, border_color: Color, square_colors: list[Color]) -> None:
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.square_colors = square_colors