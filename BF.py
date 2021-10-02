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

