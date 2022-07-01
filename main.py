import os

os.environ["RAYLIB_BIN_PATH"] = "__file__"

import raylibpy
import Scrabble


def main():
    Scrabble.start()


if __name__ == '__main__':
    main()
