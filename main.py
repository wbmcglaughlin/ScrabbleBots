# core_color_select.py
import os
import csv
from re import T

os.environ["RAYLIB_BIN_PATH"] = "__file__"

from raylibpy import *
from Modules import Graphics, Scrabble

def main():
    # Scrabble Words
    words = []
    with open("./Resources/ScrabbleWords.txt", "r") as word_file:
        lines = word_file.readlines()
        for line in lines:
            words.append(line.removesuffix('\n').lower())

    # Dimensions for the board
    width  = 600
    height = 800

    board_side_dim = height if (width > height) else width

    border     = 20
    spacing    = (height - board_side_dim) / 2
    dimensions = Graphics.Dimensions(board_side_dim - 2 * border, border, border + spacing)

    # Graphics
    border_thickness: int      = 3
    border_color: Color        = BLACK
    square_colors: list[Color] = [RED, Color(255, 200, 2347, 255), BLUE, GRAY]
    render: Graphics.Render    = Graphics.Render(border_thickness, border_color, square_colors)

    # Scrabble board
    side_squares   = 15
    triple_words   = [0, 7, 14, 105, 119, 
                        210, 217, 224]
    double_words   = [16, 32, 48, 64, 28, 
                        42, 56, 70, 196, 182, 
                        168, 154, 208, 192, 176, 
                        160, 112]
    triple_letters = [20, 24, 76, 136, 200, 
                        204, 88, 148, 80, 84, 
                        140, 144]
    double_letters = [45, 165, 213, 221, 179, 
                        59, 36, 52, 38, 102, 
                        116, 132, 186, 172, 188, 
                        122, 108, 92, 96, 98, 
                        126, 128]

    tile_bag = Scrabble.TileBag()

    board = Scrabble.Board(side_squares, triple_words, double_words, triple_letters, double_letters)

    player_one = Scrabble.Player()
    player_two = Scrabble.Player()

    players = [player_one, player_two]

    for player in players:
        player.get_tiles(tile_bag)

    init_window(width, height, "Scrabble Bots")

    set_target_fps(120)

    turn = 0
    selected_tile: Scrabble.Tile = None
    selected_tile_index: int = None

    while not window_should_close():

        mouse_point = get_mouse_position()

        begin_drawing()
        clear_background(RAYWHITE)

        draw_fps(5, 5)
        board.draw_board(dimensions, render)
        board.draw_player_pieces(dimensions, players)

        if is_mouse_button_released(MOUSE_LEFT_BUTTON):
            for square in board.board_squares:
                if check_collision_point_rec(mouse_point, square):
                    selected_tile.position = square
                elif len(players[turn].moved_tiles) > 0:
                    players[turn].moved_tiles.remove(selected_tile_index)

            selected_tile = None

        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
            tiles = board.get_tile_positions(dimensions, turn)
            for tile_index, tile in enumerate(tiles):
                if check_collision_point_rec(mouse_point, tile):
                    selected_tile = players[turn].tiles[tile_index]
                    selected_tile_index = tile_index
                    players[turn].moved_tiles.append(tile_index)

        if is_mouse_button_down(MOUSE_LEFT_BUTTON):
            if selected_tile is not None:
                side_length = dimensions.side_length / 15
                selected_tile.draw_tile(Rectangle(mouse_point.x - side_length / 2, mouse_point.y - side_length / 2, side_length, side_length), side_length)

        end_drawing()

    close_window()


if __name__ == '__main__':
    main()
