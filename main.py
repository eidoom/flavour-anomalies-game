#!/usr/bin/env python
# coding=UTF-8

from random import choice, randint

EMPTY = " "
OBSTACLE = "0"
PLAYER = "X"
HORIZONTAL_BORDER = "-"
VERTICAL_BORDER = "|"
# NORTH = ["n", "N"]
# EAST = ["e", "E"]
# SOUTH = ["s", "S"]
# WEST = ["w", "W"]
NORTH = ["w", "W"]
EAST = ["d", "D"]
SOUTH = ["s", "S"]
WEST = ["a", "A"]


def main():
    title = ("             _    _        \n"
             "\ \  _  / / / \  | \  |    \n"
             " \ \/_\/ / | 0 | | /  |    \n"
             "  \_/ \_/   \_/  | \  |__  d \n")

    print(title)
    print("Use wasd controls")

    def tiles(empty_ratio):
        return [EMPTY] * empty_ratio + [OBSTACLE]

    # def empty_world_matrix(length):
    #     return [EMPTY * length] * length

    def world_matrix(limits, empty_ratio):
        i_length, j_length = limits
        return [[choice(tiles(empty_ratio)) for _ in range(j_length)] for _ in range(i_length)]

    def render_world(data):
        border = HORIZONTAL_BORDER*(len(data[0])+2) + "\n"
        return "".join([border,
                        *["".join([VERTICAL_BORDER, *[a for a in line], VERTICAL_BORDER + "\n"]) for line in data],
                        border])

    def generate_random_position(limits):
        i_length, j_length = limits
        return randint(0, i_length - 1), randint(0, j_length - 1)

    def generate_start_position(data, limits):
        i, j = generate_random_position(limits)
        if data[i][j] == OBSTACLE:
            generate_start_position(data, limits)
        return i, j

    def move(data, position):
        i, j = position
        direction = input("Which way to move?")
        if direction in NORTH:
            i -= 1
        elif direction in SOUTH:
            i += 1
        elif direction in WEST:
            j -= 1
        elif direction in EAST:
            j += 1
        else:
            print("Use wasd!")
            return move(data, position)
        if (i + 1 > len(list(zip(*data))[0])) or (j + 1 > len(data[0])) or data[i][j] is not EMPTY:
            print("You can't do that!")
            return move(data, position)
        return i, j

    def game(data, position):
        i, j = position
        data[i][j] = PLAYER
        print(render_world(data))
        data[i][j] = EMPTY
        new_position = move(data, position)
        game(data, new_position)

    sides = 50, 200
    world_data = world_matrix(sides, 15)
    start = generate_start_position(world_data, sides)
    game(world_data, start)


if __name__ == "__main__":
    main()
