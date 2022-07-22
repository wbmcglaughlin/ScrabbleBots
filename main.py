import os
from typing import Union

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
    width = 600
    height = 800

    # Need to find dominant width
    board_side_dim = height if (width > height) else width

    # Dimensions Class Init
    border = 20
    spacing = (height - board_side_dim) / 2
    dimensions = Graphics.Dimensions(board_side_dim - 2 * border, border, int(border + spacing))

    # Graphics
    border_thickness: int = 3
    border_color: Color = BLACK
    square_colors: list[Color] = [RED, Color(255, 200, 2347, 255), BLUE, GRAY]
    render: Graphics.Render = Graphics.Render(border_thickness, border_color, square_colors)

    # Scrabble board special tiles
    side_squares = 15
    triple_words = [0, 7, 14, 105, 119,
                    210, 217, 224]
    double_words = [16, 32, 48, 64, 28,
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

    # Generating Tile Bag
    tile_bag = Scrabble.TileBag()

    # Generating Scrabble Board
    board = Scrabble.Board(side_squares, triple_words, double_words, triple_letters, double_letters)

    # Creating players
    player_one = Scrabble.Player()
    player_two = Scrabble.Player()

    turn = 0
    players = [player_one, player_two]

    for player in players:
        player.get_tiles(tile_bag)

    # Creating window
    init_window(width, height, "Scrabble Bots")

    # Target FPS
    set_target_fps(120)

    # Tile selected by player
    selected_tile: Union[Scrabble.Tile, None] = None
    held_rack_position = None

    # Complete Turn Button
    complete_turn_button_rect = Rectangle(10, height - 10 - 30, 30, 30)
    complete_turn_button_clicked = False

    # Main Game Loop
    while not window_should_close():
        # Player mouse position
        mouse_point = get_mouse_position()

        # Begin Drawing and Clearing Background
        begin_drawing()
        clear_background(RAYWHITE)

        # Draw FPS onto Corner
        # draw_fps(5, 5)

        # Draw Board Aspects
        board.draw_board(dimensions, render) # Draws background
        board.draw_player_pieces(dimensions, players) # Draws rack pieces
        board.draw_legal_moves(players[turn]) # Draw legal moves onto board

        # Draw Complete Turn Button
        draw_rectangle_rec(complete_turn_button_rect, Color(63, 201, 24, 255))

        # On Mouse Button Release
        if is_mouse_button_released(MOUSE_LEFT_BUTTON):
            # Check if tile is on top of square
            for square_index, square in enumerate(board.board_squares):
                if check_collision_point_rec(mouse_point, square):
                    # Seeing if moves have been calculated
                    if not board.has_moves:
                        board.legal_moves = board.get_legal_moves(players[turn]) # If not, get moves

                    # Checking if there are legal moves
                    if board.legal_moves is not None:
                        # Checking if square is a legal move
                        if square_index in board.legal_moves:
                            # If a tile has been selected TODO: is this the correct spot?
                            if selected_tile is not None:
                                selected_tile.rack_position = None
                                selected_tile.board_position = square_index
                                board.has_moves = False
                        # Return piece to board
                        elif selected_tile is not None:
                            selected_tile.rack_position = held_rack_position
                            held_rack_position = None

            # Selected tile will always be None after release
            selected_tile = None

            # TODO: move this somewhere else
            complete_turn_button_clicked = False

        # If mouse button is pressed initially
        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
            tiles = board.get_player_tile_rec(dimensions, turn)
            for tile_index, tile in enumerate(tiles):
                # If the tile is not on the board
                if players[turn].tiles[tile_index].board_position is None:
                    # If the tile is under the click position
                    if check_collision_point_rec(mouse_point, tile):
                        # Hold the tile
                        selected_tile = players[turn].tiles[tile_index]
                        held_rack_position = selected_tile.rack_position
                        selected_tile.rack_position = None

            # Check if the complete turn button is pressed
            if check_collision_point_rec(mouse_point, complete_turn_button_rect) and not complete_turn_button_clicked:
                complete_turn_button_clicked = True
                for tile in players[turn].tiles:
                    # Append all the tiles that are placed by a player onto the board tiles
                    if tile.board_position is not None:
                        board.tiles.append(tile)
                        # Remove the tiles from the bag
                        players[turn].tiles.remove(tile)

                # Fill the players tile bag
                players[turn].get_tiles(tile_bag)

                # Next Turn
                turn = (turn + 1) % len(players)

        # Check if the mouse is down still
        if is_mouse_button_down(MOUSE_LEFT_BUTTON):
            # Draws tile under mouse position
            if selected_tile is not None:
                side_length = dimensions.side_length / 15
                selected_tile.draw_tile(
                    Rectangle(mouse_point.x - side_length / 2, mouse_point.y - side_length / 2, side_length,
                              side_length), side_length)

        # End drawing
        end_drawing()

    # Close window on exit
    close_window()


if __name__ == '__main__':
    main()
