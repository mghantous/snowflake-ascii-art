__author__ = 'mghantous'

import sys
import os
import time

from random import Random
from termcolor import colored


class Snow(object):
    def __init__(self):

        try:
            self.terminal_height = os.get_terminal_size().lines
            self.terminal_width = os.get_terminal_size().columns
        except Exception:
            self.terminal_height = 50
            self.terminal_width = 50

        self.max_snowflakes = 6
        self.slide_duration = 3
        self.random = Random()
        self.skip = False

    def write(self, line, new_line='\n'):
        line = "{}{}".format(line, new_line if new_line else '')
        sys.stdout.write(line)

    def clear(self):
        clear = '\n'*(self.terminal_height-1)
        self.write(clear)

    def make(self):
        colors = ['red', 'green']
        color_index = 0
        while True:
            for filename in os.listdir('slides'):
                filename = os.path.join('slides', filename)

                with open(filename, 'r') as drawing:
                    end_time = time.time() + self.slide_duration

                    while time.time() < end_time:
                        self.make_screen(drawing, color=colors[color_index])
                        drawing.seek(0)
                        time.sleep(.14)

                color_index += 1
                if color_index >= len(colors):
                    color_index = 0

    def snow_the_line(self, line='', color='red'):
        # make full length
        line = line.replace('\n', '')
        line = line + (' '*(self.terminal_width - len(line))) + '\n'

        if self.skip:
            self.skip = False
            return colored(line, color)

        possible_flakes = [
            '*',
            '.',
            # 'o',
            u"\u2666",  # diamond
            u"\u2744",  # snowflake
        ]

        flake_index_locations = []

        for _ in range(0, self.max_snowflakes):
            random_index = self.random.randrange(0, len(line))
            if line[random_index] == ' ':
                new_copy = ''
                # TODO: Can't assign at index. Find better way to replace at index without making copy.
                for index, char in enumerate(line):
                    if index == random_index:
                        flake_index_locations.append(index)
                        flake_index = self.random.randrange(0, len(possible_flakes))
                        new_copy += possible_flakes[flake_index]
                    else:
                        new_copy += char
                line = new_copy

        self.skip = True
        return line

    def make_screen(self, drawing, color='red'):
        lines = ''
        line_count = 0

        for line in drawing.readlines():
            # replace whitespace randomly with *
            # clear screen, repeat
            line = self.snow_the_line(line, color)
            lines += line
            line_count += 1

        # Prepend snow
        while line_count < self.terminal_height:
            lines = self.snow_the_line() + lines
            line_count += 1
        self.write(lines)

snow = Snow()
snow.make()
