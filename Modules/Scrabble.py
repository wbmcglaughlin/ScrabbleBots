import random
from re import T
from raylibpy import *
from Modules.Graphics import Dimensions, Render

class Board():
    def __init__(self, side_squares: int, triple_words: list[int], double_words: list[int], triple_letters: list[int], double_letters: list[int]) -> None:
        self.side_squares = side_squares
        self.triple_words = triple_words
        self.double_words = double_words
        self.triple_letters = triple_letters
        self.double_letters = double_letters

        self.board_squares: list[Rectangle] = []

    def update_board_squares(self, dimensions: Dimensions):
        self.board_squares.clear()

        square_side_length = dimensions.side_length / self.side_squares

        for i in range(self.side_squares):
            for j in range(self.side_squares):
                self.board_squares.append(Rectangle(
                    dimensions.posx + j * square_side_length,
                    dimensions.posy + i * square_side_length,
                    square_side_length,
                    square_side_length
                ))

    def draw_board(self, dimensions: Dimensions, render: Render):
        # Draws Special Squares
        if self.board_squares == []:
            self.update_board_squares(dimensions)

        for square in self.triple_words:
            draw_rectangle_rec(self.board_squares[square], render.square_colors[0])

        for square in self.double_words:
            draw_rectangle_rec(self.board_squares[square], render.square_colors[1])

        for square in self.triple_letters:
            draw_rectangle_rec(self.board_squares[square], render.square_colors[2])

        for square in self.double_letters:
            draw_rectangle_rec(self.board_squares[square], render.square_colors[3])
        
        # Numbers Board
        for i, square in enumerate(self.board_squares):
            draw_text(str(i), square.x + 1, square.y + 1, 10, BLACK)

        # Draws Border
        square_side_length = dimensions.side_length / self.side_squares
        for i in range(self.side_squares + 1):
            start_ver = Vector2(i * square_side_length + dimensions.posx, 0 + dimensions.posy)
            end_ver   = Vector2(i * square_side_length + dimensions.posx, dimensions.side_length + dimensions.posy)
            draw_line_v(start_ver, end_ver, render.border_color)

            start_hor = Vector2(0 + dimensions.posx, i * square_side_length  + dimensions.posy)
            end_hor   = Vector2(dimensions.side_length + dimensions.posx, i * square_side_length + dimensions.posy)
            draw_line_v(start_hor, end_hor, render.border_color)

class Tile():
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

        self.position = None

class TileBag():
    def __init__(self) -> None:
        self.tiles = self.fill_bag()

    def fill_bag(self):
        tiles = []

        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        tile_value =  [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]
        tile_counts = [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1, 6, 4, 6, 4, 2, 2, 1, 2, 1]

        # Sanity Check
        if len(tile_value) != len(alphabet) and len(tile_counts) != len(alphabet):
            exit(-1)

        for i, count in enumerate(tile_counts):
            for _ in range(count):
                tiles.append(Tile(alphabet[i], tile_value[i]))

        random.shuffle(tiles)

        return tiles

    def print(self):
        for tile in self.tiles:
            print((tile.type, tile.value))
