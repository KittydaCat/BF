from functools import partial
import tkinter as tk
import numpy as np


class Interpreter:

    def __init__(self, program):

        self.program = program

        self.program_pointer = 0

        self.mem = np.array((0, 0))

        self.mem_pointer = 0

        self.key = {
            '+': partial(self.increase, 1),
            '-': partial(self.increase, -1),
            '>': partial(self.increment, 1),
            '<': partial(self.increment, -1),
            '[': partial(self.ex_if, partial(self.find_next_loop, 1), lambda: self.mem[self.mem_pointer] == 0),
            ']': partial(self.ex_if, partial(self.find_next_loop, -1), lambda: self.mem[self.mem_pointer]),
            '.': self.input,
            ',': self.output}

    def run(self):

        while self.program_pointer < len(self.program):

            self.execute()

    def execute(self):

        if (command := self.program[self.program_pointer]) in self.key:

            self.key[command]()

        self.program_pointer += 1

    def increase(self, value):

        self.mem[self.mem_pointer] += value

    def increment(self, value):

        self.mem_pointer += value

        if not self.mem_pointer < len(self.mem):

            self.mem = np.append(self.mem, np.full(self.mem_pointer - len(self.mem) + 1, 0))

        if self.mem_pointer < 0:

            self.mem_pointer = 0

    def ex_if(self, func, condition):

        if condition():

            self.program_pointer = func()

    def find_next_loop(self, direction):

        level = 0

        pointer = self.program_pointer

        while True:

            if self.program[pointer] == '[':
                level += 1

            elif self.program[pointer] == ']':
                level += -1

            if level == 0:

                break

            pointer += direction
                
        return pointer

    def input(self):

        self.mem[self.mem_pointer] = ord(input())

    def output(self):

        print(chr(self.mem[self.mem_pointer]))

    def exec(self, program):

        program_pointer = 0

        while program_pointer < len(program):

            if (command := program[program_pointer]) in self.key:

                self.key[command]()

            program_pointer += 1


class BF(Interpreter):

    def __init__(self, program=None):

        # get the program if one wasn't supplied

        if program is None:

            pro_prompt = tk.Tk()

            # set up an entry to get the program
            pro_entry = tk.Entry(pro_prompt)
            pro_entry.pack()

            # set up a check button to set the program var to whatever the user inputted
            def enter():

                global program

                program = pro_entry.get

                pro_prompt.destroy()

            pro_check = tk.Button(text='🗸', command=enter)
            pro_check.pack()

        """BF interpreter stuff"""

        super().__init__(program)

        """GUI stuff"""

        # create the display
        self.display = tk.Tk()

        # set up a text to display program
        self.text = tk.Label(self.display, text=self.program, state=tk.DISABLED, underline=0)
        self.text.pack()

        # display the program's memory
        self.mem_var = tk.StringVar(self.display)
        self.mem_display = tk.Label(self.display, textvariable=self.mem_var, underline=0)
        self.mem_display.pack()

        # setup a frame to hold all the buttons & input
        self.frame = tk.Frame(self.display)
        self.frame.pack()

        # setup the input box
        self.input_var = tk.StringVar(self.frame, value='')
        self.input_var.trace('w', self.enter)
        self.input_box = tk.Entry(self.frame, textvariable=self.input_var, state=tk.DISABLED)
        self.input_box.pack()

        # setup the next arrow
        self.next = tk.Button(self.frame, text='>', command=self.execute)
        self.next.pack()

        # set up the run arrow
        self.next_next = tk.Button(self.frame, text='>>', command=self.run)
        self.next_next.pack()

        # set up the output box
        self.output_var = tk.StringVar(self.display, value='')
        self.output_box = tk.Message(self.display, textvariable=self.output_var)
        self.output_box.pack()

        """Module stuff"""

        self.key['/'] = self.module_exec

    def module_exec(self):

        self.program_pointer += 1

        file_name = self.program[self.program_pointer:self.program[self.program_pointer:].index('/')+self.program_pointer]

        with open(file_name) as file:

            self.exec(file.read())

        self.program_pointer = self.program[self.program_pointer:].index('/') + 1

    def execute(self):

        if (command := self.program[self.program_pointer]) in self.key and self.next_next['state'] == tk.NORMAL:

            self.key[command]()

        self.program_pointer += 1

        self.update()

    def output(self):

        self.output_var.set(self.output_var.get()+chr(self.mem[self.mem_pointer]))

    def input(self):

        self.input_box.config(state=tk.NORMAL)

        self.next.config(state=tk.DISABLED)

        self.next_next.config(state=tk.DISABLED)

    def enter(self, *args):

        self.mem[self.mem_pointer] = ord(self.input_var.get())

        self.input_var.set('')

        self.input_box.config(state=tk.DISABLED)

        self.next.config(state=tk.NORMAL)

        self.next_next.config(state=tk.NORMAL)

        self.update()

    def update(self):

        if self.program_pointer < len(self.program):

            self.text.config(underline=self.program_pointer)

        else:

            self.text.config(underline=-1)

        self.mem_var.set(str(self.mem))

        self.mem_display.config(underline=self.mem_pointer+1)


if __name__ == '__main__':

    pass
