from intcode import Intcode


class Arcade:
    def __init__(self, filename, quarters=None):
        self.program = Intcode.read_program(filename)
        if quarters:
            self.program.memory[0] = 2
        self.grid = dict()
        self.ball_pos = None
        self.pad_pos = None
        self.score = 0

    def play_game(self):
        game = self.program.run_program()
        while True:
            try:
                x = next(game)
                y = next(game)
                tile_id = next(game)
            except StopIteration:
                break
            if (x, y) == (-1, 0):
                self.score = tile_id
            else:
                self.grid[(x, y)] = tile_id
                if tile_id == 4:
                    self.ball_pos = (x, y)
                elif tile_id == 3:
                    self.pad_pos = (x, y)
            if self.ball_pos and self.pad_pos:
                if self.ball_pos[0] < self.pad_pos[0]:
                    joystick = -1
                elif self.ball_pos[0] > self.pad_pos[0]:
                    joystick = 1
                else:
                    joystick = 0
                game = self.program.run_program([joystick])
            else:
                game = self.program.run_program()
        return self.grid, self.score


# breakout = Arcade("input.txt") # part one
breakout = Arcade("input.txt", 2)
endscreen, final_score = breakout.play_game()
# print(len(set([x for x in endscreen if endscreen[x]==2]))) #part one
print(final_score)  # part two

