from raylibpy import Color


class Dimensions:
    # Dimension Class Holding the boards dimensions information
    def __init__(self, side_length: int, posx: int, posy: int) -> None:
        self.side_length = side_length
        self.pos_x = posx
        self.pos_y = posy


class Render:
    # Render Class Holding the boards color information
    def __init__(self, border_thickness: int, border_color: Color, square_colors: list[Color]) -> None:
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.square_colors = square_colors
