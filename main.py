# core_color_select.py
import os

os.environ["RAYLIB_BIN_PATH"] = "__file__"

from raylibpy import *
from typing import List


def main():
    init_window(800, 800, "Scrabble Bots")

    set_target_fps(60)

    while not window_should_close():

        mouse_point = get_mouse_position()

        begin_drawing()

        clear_background(RAYWHITE)

        end_drawing()

    close_window()


if __name__ == '__main__':
    main()
