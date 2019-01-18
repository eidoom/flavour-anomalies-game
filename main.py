#!/usr/bin/env python
# coding=UTF-8

from random import choice


def main():
    title = ("             _    _        \n"
             "\ \  _  / / / \  | \  |    \n"
             " \ \/_\/ / | 0 | | /  |    \n"
             "  \_/ \_/   \_/  | \  |__  d \n")

    print(title)

    def tiles(empty_ratio):
        return [" "] * empty_ratio + ["0"]

    def empty_world_matrix(length):
        return [" " * length] * length

    def world_matrix(length, empty_ratio):
        return [[choice(tiles(empty_ratio)) for _ in range(length)] for _ in range(length)]

    world_data = world_matrix(100, 14)

    def render_world(data):
        return "".join(["".join([*[a for a in line], "\n"]) for line in data])

    world = render_world(world_data)

    print(world)


if __name__ == "__main__":
    main()
