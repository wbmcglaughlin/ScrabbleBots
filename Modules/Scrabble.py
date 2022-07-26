import random
from typing import Union, List

from raylibpy import *
from Modules.Graphics import Dimensions, Render


class Tile:
    # Scrabble Tile Class
    def __init__(self, letter, value) -> None:
        """

        :param letter: the letter on the tile
        :param value: the value of the letter
        """
        self.type = letter
        self.value = value

        # position of the tiles on either the rack or the board
        self.rack_position: Union[int, None] = None
        self.board_position: Union[int, None] = None

    def draw_tile(self, rec: Rectangle, side_length: float):
        """

        :param rec: tile dimension parameters
        :param side_length: side length of the tile TODO: is this needed?
        :return:
        """

        # Set the color of the tile
        color = Color(227, 204, 32, 255)
        if self.rack_position is not None:
            color = Color(227, 142, 32, 255)

        # Draws rectangle and the tile letter
        draw_rectangle_rec(rec, color)
        font_size = int(side_length / 1.5)
        offset = (side_length - font_size) / 2

        draw_text(self.type, rec.x + offset, rec.y + offset, font_size, BLACK)
        draw_text(str(self.board_position), rec.x + 1, rec.y + 1, int(font_size / 3), BLACK)
        draw_text(str(self.rack_position), rec.x + 1, rec.y + side_length - int(font_size / 3) - 1, int(font_size / 3),
                  BLACK)
        draw_text(str(self.value), rec.x + side_length - int(font_size / 3) - 1,
                  rec.y + side_length - int(font_size / 3) - 1,
                  int(font_size / 3),
                  BLACK)


class TileBag:
    # Scrabble Tile Bag Containing all the remaining tiles
    def __init__(self) -> None:
        self.tiles = self.fill_bag()

    @staticmethod
    def fill_bag():
        """
        returns a List of tiles
        :return: List[tile]
        """
        tiles = []

        # Scrabble Standard Setup
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        tile_value = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]
        tile_counts = [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1, 6, 4, 6, 4, 2, 2, 1, 2, 1]

        # Sanity Check
        if len(tile_value) != len(alphabet) and len(tile_counts) != len(alphabet):
            exit(-1)

        # Appending tiles in order
        for i, count in enumerate(tile_counts):
            for _ in range(count):
                tiles.append(Tile(alphabet[i], tile_value[i]))

        # Shuffling tiles
        random.shuffle(tiles)

        return tiles

    def get_tile(self) -> Tile:
        """
        Gets the last tile from the bag
        :return: tile
        """
        tile: Tile = self.tiles.pop()
        return tile

    def print(self):
        """

        :return:
        """
        for tile in self.tiles:
            print((tile.type, tile.value))


class Player:
    # Player Class
    def __init__(self) -> None:
        self.held_piece = -1
        self.score = 0
        self.tiles: List[Tile] = []

    def get_tiles(self, tile_bag: TileBag):
        """
        Class which fills player tiles

        :param tile_bag: TileBag
        :return:
        """
        tile_max = 7
        if len(self.tiles) == tile_max:
            print("Tile Bag already full")

        for idx, tile in enumerate(self.tiles):
            tile.rack_position = idx
            tile.board_position = None

        for i in range(len(self.tiles), tile_max):
            tile = tile_bag.get_tile()
            tile.rack_position = i
            tile.board_position = None
            self.tiles.append(tile)

    def get_filled_rack_pos(self):
        return [tile.rack_position for tile in self.tiles if tile.rack_position is not None]


class Board:
    # Scrabble Board Class
    def __init__(self, side_squares: int, triple_words: List[int], double_words: List[int], triple_letters: List[int],
                 double_letters: List[int]) -> None:
        """

        :param side_squares: int
        :param triple_words: list[int]
        :param double_words: list[int]
        :param triple_letters: list[int]
        :param double_letters: list[int]
        """
        self.side_squares = side_squares
        self.triple_words = triple_words
        self.double_words = double_words
        self.triple_letters = triple_letters
        self.double_letters = double_letters

        self.board_squares: List[Rectangle] = []
        self.tiles: List[Tile] = []

        self.has_moves: bool = False
        self.legal_moves: List[int] = []

        self.has_movable_tiles: bool = False
        self.movable_tiles: List[int] = []

    def update_board_squares(self, dimensions: Dimensions):
        """
        Board squares containing information about board positions, would
        be updated on window size change

        :param dimensions: Dimensions
        :return:
        """

        # Clears last board squares
        self.board_squares.clear()

        square_side_length = dimensions.side_length / self.side_squares

        # Appending each square to list
        for i in range(self.side_squares):
            for j in range(self.side_squares):
                self.board_squares.append(Rectangle(
                    dimensions.pos_x + j * square_side_length,
                    dimensions.pos_y + i * square_side_length,
                    square_side_length,
                    square_side_length
                ))

    def draw_board(self, dimensions: Dimensions, render: Render):
        """
        Draws the board and special scrabble squares

        :param dimensions: Dimensions
        :param render: Render
        :return:
        """

        # Checks to see if the class has square locations
        if not self.board_squares:
            self.update_board_squares(dimensions)

        # Draws special squares
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

        # Draws Border TODO: Fix this implementation
        square_side_length = dimensions.side_length / self.side_squares
        for i in range(self.side_squares + 1):
            start_ver = Vector2(i * square_side_length + dimensions.pos_x, 0 + dimensions.pos_y)
            end_ver = Vector2(i * square_side_length + dimensions.pos_x, dimensions.side_length + dimensions.pos_y)
            draw_line_v(start_ver, end_ver, render.border_color)

            start_hor = Vector2(0 + dimensions.pos_x, i * square_side_length + dimensions.pos_y)
            end_hor = Vector2(dimensions.side_length + dimensions.pos_x, i * square_side_length + dimensions.pos_y)
            draw_line_v(start_hor, end_hor, render.border_color)

        # Draws board tiles
        for tile in self.tiles:
            tile.draw_tile(self.board_squares[tile.board_position], dimensions.side_length / self.side_squares)

    def draw_circles(self, circle_pos: List[int], color: Color):
        """

        :param color:
        :param circle_pos:
        :return:
        """
        # TODO: why this
        square_recs = self.board_squares

        # Draws a circle at each legal move
        for move in circle_pos:
            draw_circle(square_recs[move].x + square_recs[move].width / 2,
                        square_recs[move].y + square_recs[move].height / 2,
                        5,
                        color)

    def get_legal_moves(self, player: Player) -> List[int]:
        """
        Appends the legal scrabble moves into a list, does not check if the word is valid

        :param player: Player
        :return: list[int]
        """
        def add_all(moves: List[int], pos: int):
            """

            :param moves: list[int]
            :param pos: int
            :return: list[int]
            """
            moves = add_up_down(moves, pos)
            moves = add_left_right(moves, pos)
            return moves

        def add_up_down(moves: List[int], pos: int):
            """

            :param moves: list[int]
            :param pos: int
            :return: list[int]
            """
            moves.append(pos + self.side_squares)
            moves.append(pos - self.side_squares)
            return moves

        def add_left_right(moves: List[int], pos: int):
            """

            :param moves: list[int]
            :param pos: int
            :return: list[int]
            """
            moves.append(pos + 1)
            moves.append(pos - 1)
            return moves

        def get_touching_pos(pos: int):
            touching = []

            for tile in self.tiles:
                if tile.board_position == pos + 1:
                    touching.append(tile.board_position)
                if tile.board_position == pos - 1:
                    touching.append(tile.board_position)
                if tile.board_position == pos - self.side_squares:
                    touching.append(tile.board_position)
                if tile.board_position == pos + self.side_squares:
                    touching.append(tile.board_position)

            return touching

        valid_moves = []

        player_tiles_count = len([tile for tile in player.tiles if tile.board_position is not None])
        board_tiles_count = len(self.tiles)

        # If there is no tiles on the board
        if len(self.tiles) + len([tile for tile in player.tiles if tile.board_position is not None]) == 0:
            self.has_moves = True
            return [int((self.side_squares * self.side_squares - 1) / 2)]

        # If there is no tiles on the board that the current player has played
        elif len([tile for tile in player.tiles if tile.board_position is not None]) == 0:
            for tile in self.tiles:
                valid_moves = add_all(valid_moves, tile.board_position)

        # If there is player tiles on the board
        else:
            player_tiles = [tile for tile in player.tiles if tile.board_position is not None]
            player_tile_board_pos = [tile.board_position for tile in player.tiles if tile.board_position is not None]
            board_tiles = [tile.board_position for tile in self.tiles if tile.board_position is not None]

            # If there is no other board tiles
            if board_tiles_count == 0 and player_tiles_count == 1:
                for tile in player_tiles:
                    valid_moves = add_all(valid_moves, tile.board_position)
            else:
                if len(player_tiles) == 1:
                    if player_tiles[0].board_position is not None:
                        touching_list = get_touching_pos(player_tiles[0].board_position)

                        for touch in touching_list:
                            valid_moves.append(touch + (touch - player_tiles[0].board_position))
                            valid_moves.append(player_tiles[0].board_position - (touch - player_tiles[0].board_position))
                else:
                    if (player_tiles[0].board_position - player_tiles[1].board_position) % self.side_squares == 0:
                        current_pos = player_tiles[0].board_position
                        while current_pos + self.side_squares in player_tile_board_pos or current_pos + self.side_squares in board_tiles:
                            current_pos += self.side_squares
                        valid_moves = add_up_down(valid_moves, current_pos)

                        current_pos = player_tiles[0].board_position
                        while current_pos - self.side_squares in player_tile_board_pos or current_pos - self.side_squares in board_tiles:
                            current_pos -= self.side_squares
                        valid_moves = add_up_down(valid_moves, current_pos)

                    else:
                        current_pos = player_tiles[0].board_position
                        while current_pos + 1 in player_tile_board_pos or current_pos + 1 in board_tiles:
                            current_pos += 1
                        valid_moves = add_left_right(valid_moves, current_pos)

                        current_pos = player_tiles[0].board_position
                        while current_pos - 1 in player_tile_board_pos or current_pos - 1 in board_tiles:
                            current_pos -= 1
                        valid_moves = add_left_right(valid_moves, current_pos)

        # Removing illegal moves
        taken_squares = []
        for tile in player.tiles:
            if tile.board_position is not None:
                taken_squares.append(tile.board_position)

        for tile in self.tiles:
            taken_squares.append(tile.board_position)

        # Checking if valid move has a tile on it
        valid_moves = [v for v in valid_moves if v not in taken_squares]

        self.has_moves = True

        return valid_moves

    def get_movable_tiles(self, player: Player):
        if not self.has_moves:
            self.legal_moves = self.get_legal_moves(player)

        player_tiles = [tile.board_position for tile in player.tiles if tile.board_position is not None]
        touching = []

        for legal_move in self.legal_moves:
            if legal_move + 1 in player_tiles:
                touching.append(legal_move + 1)
            if legal_move - 1 in player_tiles:
                touching.append(legal_move - 1)
            if legal_move - self.side_squares in player_tiles:
                touching.append(legal_move - self.side_squares)
            if legal_move + self.side_squares in player_tiles:
                touching.append(legal_move + self.side_squares)

        return touching

    def get_current_word(self, player: Player):
        player_tile_pos = [tile.board_position for tile in player.tiles if tile.board_position is not None]
        player_tile_let = [tile.type for tile in player.tiles if tile.board_position is not None]

        board_tile_pos = [tile.board_position for tile in self.tiles if tile.board_position is not None]
        board_tile_val = [tile.type for tile in self.tiles if tile.board_position is not None]

        tile_pos = player_tile_pos + board_tile_pos
        tile_val = player_tile_let + board_tile_val

        word_rows = []
        word_cols = []

        for pos in player_tile_pos:
            if pos + 1 in board_tile_pos:
                word_rows.append(int(pos / self.side_squares))
            if pos - 1 in board_tile_pos:
                word_rows.append(int(pos / self.side_squares))
            if pos + self.side_squares in board_tile_pos:
                word_cols.append(pos % self.side_squares)
            if pos - self.side_squares in board_tile_pos:
                word_cols.append(pos % self.side_squares)

        word_rows = set(word_rows)
        word_cols = set(word_cols)

        words = []

        for row in word_rows:
            word = []

            pivot = None
            for pos in player_tile_pos:
                if int(pos / self.side_squares) == row:
                    pivot = pos
                    break

            word.append(player_tile_let[player_tile_pos.index(pivot)])
            if pivot is not None:
                current = pivot + 1
                while current in tile_pos:
                    word.append(tile_val[tile_pos.index(current)])
                    current += 1

                current = pivot - 1
                while current in tile_pos:
                    word.append(tile_val[tile_pos.index(current)])
                    current -= 1

            words.append(word)

        for col in word_cols:
            word = []

            pivot = None
            for pos in player_tile_pos:
                if int(pos % self.side_squares) == col:
                    pivot = pos
                    break

            word.append(player_tile_let[player_tile_pos.index(pivot)])
            if pivot is not None:
                current = pivot + self.side_squares
                while current in tile_pos:
                    word.append(tile_val[tile_pos.index(current)])
                    current += self.side_squares

                current = pivot - self.side_squares
                while current in tile_pos:
                    word.append(tile_val[tile_pos.index(current)])
                    current -= self.side_squares

            words.append(word)

        print(words, word_rows, word_cols)

    def draw_player_pieces(self, dimensions: Dimensions, players: List[Player]):
        """

        :param dimensions: Dimensions
        :param players: list[Player]
        :return:
        """

        # Draws the players pieces at each side of the board
        for player_num, player in enumerate(players):
            tile_positions = self.get_player_tile_rec(dimensions, player_num)
            for i, tile in enumerate(player.tiles):
                if tile.rack_position is not None:
                    tile.draw_tile(tile_positions[tile.rack_position], dimensions.side_length / self.side_squares)
                if tile.board_position is not None:
                    tile.draw_tile(self.board_squares[tile.board_position], dimensions.side_length / self.side_squares)

    @staticmethod
    def get_player_tile_rec(dimensions: Dimensions, player_number) -> List[Rectangle]:
        """
        Gets the players tile positions in a convenience method

        :param dimensions: Dimensions
        :param player_number: int
        :return: list[Rectangle]
        """

        # Top left corner
        top_left_x = dimensions.pos_x + dimensions.side_length / 2 - dimensions.side_length / 15 * 3.5

        # Offset TODO: somewhere else?
        y_offset = 20

        # TODO: Fix this
        if player_number == 1:
            top_left_y = dimensions.pos_y - dimensions.side_length / 15 - y_offset
        else:
            top_left_y = dimensions.pos_y + dimensions.side_length + y_offset

        # Append tile positions into list
        tile_positions = []
        for i in range(7):
            rec = Rectangle(top_left_x + i * dimensions.side_length / 15, top_left_y, dimensions.side_length / 15,
                            dimensions.side_length / 15)
            tile_positions.append(rec)

        return tile_positions
