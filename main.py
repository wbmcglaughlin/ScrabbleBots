# core_color_select.py
import os

os.environ["RAYLIB_BIN_PATH"] = "__file__"

from raylibpy import *
from Modules import Graphics, Scrabble

def main():
    # Dimensions for the board
    width = 800
    height = 800

    board_side_dim = height if (width > height) else width

    border = 20

    dimensions = Graphics.Dimensions(board_side_dim - 2 * border, border, border)

    # Graphics
    border_thickness: int = 3
    border_color: Color = BLACK
    square_colors: list[Color] = [RED, Color(255, 200, 2347, 255), BLUE, GRAY]
    render = Graphics.Render(border_thickness, border_color, square_colors)

    # Scrabble board
    side_squares = 15;
    squares = side_squares * side_squares
    triple_words = [0, 7, 14, 105, 119, 210, 217, 224]
    double_words = [16, 32, 48, 64, 28, 42, 56, 70, 196, 182, 168, 154, 208, 192, 176, 160, 112]
    triple_letters = [20, 24, 76, 136, 200, 204, 88, 148, 80, 84, 140, 144]
    double_letters = [45, 165, 213, 221, 179, 59, 36, 52, 38, 102, 116, 132, 186, 172, 188, 122, 108, 92, 96, 98, 126, 128]

    board = Scrabble.Board(side_squares, triple_words, double_words, triple_letters, double_letters)

    init_window(800, 800, "Scrabble Bots")

    set_target_fps(60)

    while not window_should_close():

        mouse_point = get_mouse_position()

        begin_drawing()

        clear_background(RAYWHITE)

        board.draw_board(dimensions, render)

        end_drawing()

    close_window()


if __name__ == '__main__':
    main()
