import random
from raylibpy import *
from Modules.Graphics import Dimensions, Render

class Tile():
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

        self.position = None

    def draw_tile(self, rec: Rectangle, side_length: float):
        indent = 3

        draw_rectangle_rec(rec, Color(255, 200, 2347, 255))
        font_size = side_length / 1.5
        offset = (side_length - font_size) / 2

        draw_text(self.type, rec.x + offset, rec.y + offset, font_size, BLACK)

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

    def get_tile(self) -> Tile:
        tile: Tile = self.tiles.pop()
        return tile

    def print(self):
        for tile in self.tiles:
            print((tile.type, tile.value))

class Player():
    def __init__(self) -> None:
        self.held_piece = -1
        self.score = 0
        self.tiles: list[Tile] = []
        self.moved_tiles: list[int] = []
    
    def get_tiles(self, tile_bag: TileBag):
        tile_max = 7

        while len(self.tiles) < tile_max:
            self.tiles.append(tile_bag.get_tile())

        print(len(self.tiles))    

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

    def draw_player_pieces(self, dimensions: Dimensions, players: list[Player]):
        for player_num, player in enumerate(players):
            tile_positions = self.get_tile_positions(dimensions, player_num)
            for i, tile in enumerate(player.tiles):
                if tile.position is not None:
                    tile.draw_tile(tile.position, dimensions.side_length / self.side_squares)
                elif i not in player.moved_tiles:
                    tile.draw_tile(tile_positions[i], dimensions.side_length / self.side_squares)

    def get_tile_positions(self, dimensions: Dimensions, player_number) -> list[Rectangle]:
        if player_number == 1:
            top_left_x = dimensions.posx + dimensions.side_length / 2 - dimensions.side_length / 15 * 3.5

            y_offset = 20
            top_left_y = dimensions.posy - dimensions.side_length / 15 - y_offset

            tile_positions = []
            for i in range(7):
                rec = Rectangle(top_left_x + i * dimensions.side_length / 15, top_left_y, dimensions.side_length / 15, dimensions.side_length / 15)
                tile_positions.append(rec)
        else:
            top_left_x = dimensions.posx + dimensions.side_length / 2 - dimensions.side_length / 15 * 3.5

            y_offset = 20
            top_left_y = dimensions.posy + dimensions.side_length + y_offset

            tile_positions = []
            for i in range(7):
                rec = Rectangle(top_left_x + i * dimensions.side_length / 15, top_left_y, dimensions.side_length / 15, dimensions.side_length / 15)
                tile_positions.append(rec)

        return tile_positions




