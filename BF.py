import tkinter as tk
import numpy as np
from functools import partial


class Interpreter:

    def __init__(self, program=''):

        self.program = program

        self.mem = np.array((0, 0))

        self.pointer = 0

        self.key = {'+': partial(self.increase, 1),
                    '-': partial(self.increase, -1),
                    '>': partial(self.increment, 1),
                    '<': partial(self.increment, -1),
                    '[': partial(self.jump_to, lambda pointer: self.find_next_loop(pointer, 1), lambda _: self.mem[self.pointer] == 0),
                    ']': partial(self.jump_to, lambda pointer: self.find_next_loop(pointer, -1), lambda _: self.mem[self.pointer]),
                    '.': self.print,
                    ',': self.input}

    def run(self, instruction_pointer=0):

        while not instruction_pointer == len(self.program):

            if (symbol := self.program[instruction_pointer]) in self.key:

                instruction_pointer = self.key[symbol](instruction_pointer)

            instruction_pointer += 1

    def increase(self, value, pointer):

        self.mem[self.pointer] += value

        return pointer

    def increment(self, value, pointer):

        self.pointer += value

        if not self.pointer < len(self.mem):

            self.mem = np.append(self.mem, np.full(self.pointer - len(self.mem) + 1, 0))

        if self.pointer < 0:

            self.pointer = 0

        return pointer

    def jump_to(self, target, condition, pointer):

        if condition(pointer):

            return target(pointer)

        return pointer

    def find_next_loop(self, pointer, direction):

        level = 0

        if self.program[pointer] == '[':

            level += 1

        if self.program[pointer] == ']':

            level += -1

        while not level == 0:

            pointer += direction

            if self.program[pointer] == '[':
                level += 1

            elif self.program[pointer] == ']':
                level += -1

        return pointer

    def print(self, pointer):

        print(chr(self.mem[self.pointer]))

        return pointer

    def input(self, pointer):

        self.mem[self.pointer] = ord(input())

        return pointer


def run(program):

    program = Interpreter(program=program)

    program.run()

    print(program.mem)


if __name__ == '__main__':

    while True:

        run(input())
