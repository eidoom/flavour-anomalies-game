#!/usr/bin/env python
# coding=UTF-8

from random import choice, randint
from argparse import ArgumentParser
from time import perf_counter

TITLE = ("             _    _        \n"
         "\ \  _  / / / \  | \  |    \n"
         " \ \/_\/ / | 0 | | /  |    \n"
         "  \_/ \_/   \_/  | \  |__  d \n")

EMPTY = " "
OBSTACLES = ["T", "O"]
END = "A"
PLAYER = "X"

HORIZONTAL_BORDER = "-"
VERTICAL_BORDER = "|"

SMALL = "small"
MEDIUM = "medium"
LARGE = "large"

SMALL_MAP = (12, 50)
MEDIUM_MAP = (25, 100)
LARGE_MAP = (50, 200)

# NORTH = ["n", "N"]
# EAST = ["e", "E"]
# SOUTH = ["s", "S"]
# WEST = ["w", "W"]

NORTH = ["w", "W"]
EAST = ["d", "D"]
SOUTH = ["s", "S"]
WEST = ["a", "A"]

UNKNOWN_MAP_SIZE_PROMPT = "Unknown map size"
START_PROMPT = "You are the X. Use wasd controls to move. Get to the A!"
MOVE_PROMPT = "Which way to move?"
WRONG_KEY_PROMPT = "Use wasd!"
INVALID_MOVE_PROMPT = "You can't do that!"
WIN_PROMPT = "You won!"


def map_size_to_text(map_dimensions):
    i, j = map_dimensions
    return f"{j}x{i}"


def tiles(empty_ratio):
    return [EMPTY] * empty_ratio + OBSTACLES


# def empty_world_matrix(length):
#     return [EMPTY * length] * length

def world_matrix(limits, empty_ratio):
    i_length, j_length = limits
    return [[choice(tiles(empty_ratio)) for _ in range(j_length)] for _ in range(i_length)]


def render_world(data):
    border = HORIZONTAL_BORDER * (len(data[0]) + 2) + "\n"
    return "".join([border,
                    *["".join([VERTICAL_BORDER, *[a for a in line], VERTICAL_BORDER + "\n"]) for line in data],
                    border])


def generate_random_position(limits):
    i_length, j_length = limits
    return randint(0, i_length - 1), randint(0, j_length - 1)


def generate_allowed_position(data, limits):
    i, j = generate_random_position(limits)
    if data[i][j] in OBSTACLES:
        generate_allowed_position(data, limits)
    return i, j


def move(data, position):
    i, j = position
    direction = input(MOVE_PROMPT)
    if direction in NORTH:
        i -= 1
    elif direction in SOUTH:
        i += 1
    elif direction in WEST:
        j -= 1
    elif direction in EAST:
        j += 1
    else:
        print(WRONG_KEY_PROMPT)
        return move(data, position)
    if any([i < 0, j < 0, i + 1 > len(list(zip(*data))[0]), j + 1 > len(data[0]), data[i][j] in OBSTACLES]):
        print(INVALID_MOVE_PROMPT)
        return move(data, position)
    return i, j


def turn(data, position, end, moves=0):
    i, j = position
    data[i][j] = PLAYER
    print(render_world(data))
    if position == end:
        return moves
    data[i][j] = EMPTY
    return turn(data, move(data, position), end, moves + 1)


def game(i_length, j_length, emptiness):
    sides = i_length, j_length
    data = world_matrix(sides, emptiness)
    start = generate_allowed_position(data, sides)
    end = generate_allowed_position(data, sides)
    i, j = end
    data[i][j] = END
    return turn(data, start, end)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-m", "--map-size", type=str, default=SMALL,
                        help=f"Set the map size to {SMALL} ({map_size_to_text(SMALL_MAP)}), "
                        f"{MEDIUM} ({map_size_to_text(MEDIUM_MAP)}), or {LARGE} ({map_size_to_text(LARGE_MAP)}). "
                        f"Can be overridden by setting map height and map width manually.")
    parser.add_argument("-e", "--emptiness", type=int, default=30,
                        help="Set the map emptiness factor. A higher emptiness factor means less obstacles.")
    parser.add_argument("-y", "--map-height", type=int, default=None,
                        help="Set the map height (vertical side length). "
                             "Must also set map width. Overrides map size.")
    parser.add_argument("-x", "--map-width", type=int, default=None,
                        help="Set the map width (horizontal side length). "
                             "Must also set map height. Overrides map size.")
    args = parser.parse_args()

    if args.map_size == SMALL:
        map_size = SMALL_MAP
    elif args.map_size == MEDIUM:
        map_size = MEDIUM_MAP
    elif args.map_size == LARGE:
        map_size = LARGE_MAP
    else:
        exit(UNKNOWN_MAP_SIZE_PROMPT)

    if (args.map_height is not None) and (args.map_width is not None):
        map_size = (args.map_height, args.map_width)

    return (*map_size, args.emptiness)


def main():
    print(TITLE)
    print(START_PROMPT)
    start_time = perf_counter()
    moves = game(*parse_arguments())
    print(WIN_PROMPT)
    print("\nStatistics:\n"
          f"Moves: {moves}\n"
          f"Time: {perf_counter() - start_time} s")


if __name__ == "__main__":
    main()
