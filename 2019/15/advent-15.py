from intcode import Intcode
from collections import deque


class RepairDroid:
    def __init__(self, filename):
        self.discovered = set()
        self.parent = {}
        self.edges = {}
        self.way_in = {}
        self.current_position = (0, 0)
        self.program = Intcode.read_program(filename)

    def get_loc(self, n: int):
        if n == 1:
            direction = (0, 1)
        elif n == 2:
            direction = (0, -1)
        elif n == 3:
            direction = (-1, 0)
        elif n == 4:
            direction = (1, 0)
        return (
            self.current_position[0] + direction[0],
            self.current_position[1] + direction[1],
        )

    @staticmethod
    def go_back(n):
        if n == 1:
            return 2
        elif n == 2:
            return 1
        elif n == 3:
            return 4
        elif n == 4:
            return 3

    def test_edge(self, n):
        movement = self.program.run_program([n])
        out = next(movement)
        # print(f"{n}: {out}")
        if out == 0:
            return False
        elif out == 1:
            move = self.go_back(n)
            movement = self.program.run_program([move])
            back = next(movement)
            assert back == 1
            return True
        elif out == 2:
            return "WIN"

    def step_back(self):
        way = self.way_in[self.current_position]
        # print(way)
        move = self.go_back(way)
        # print(move)
        movement = self.program.run_program([move])
        back = next(movement)
        # print(back)
        assert back == 1

    def get_edges(self):
        edges = []
        for n in range(1, 5):
            cell = self.get_loc(n)
            in_cell = self.test_edge(n)
            if in_cell:
                if in_cell == "WIN":
                    return True, (cell, n)
                else:
                    edges.append((cell, n))
        # print(edges)
        return False, edges

    def find_o2(self):
        while True:
            # print(self.way_in)
            if self.current_position not in self.discovered:
                win, edges = self.get_edges()
                self.discovered.add(self.current_position)
                if win:
                    self.parent[edges[0]] = self.current_position
                    self.way_in[edges[0]] = edges[1]
                    return edges[0]
                else:
                    new_edges = [e for e in edges if e[0] not in self.discovered]
                    # print(new_edges)
                    self.edges[self.current_position] = new_edges
                    if new_edges:
                        for e in new_edges:
                            self.parent[e[0]] = self.current_position
                            self.way_in[e[0]] = e[1]
                    else:
                        self.step_back()
            elif self.edges[self.current_position]:
                direct = self.edges[self.current_position].pop()
                if not self.edges[self.current_position]:
                    del self.edges[self.current_position]
                step = self.program.run_program([direct[1]])
                go = next(step)
                if go == 1:
                    self.current_position = self.get_loc(direct[1])
            else:
                self.step_back()
            print(self.current_position)

    def reconstruct_chain(self, position):
        chain = []
        if position != (0, 0):
            papa = self.parent[position]
            chain.append(papa)
            mama = self.reconstruct_chain(papa)
            if mama:
                for m in mama:
                    chain.append(m)
        return chain


o2 = RepairDroid("input.txt")
oxygen = o2.find_o2()
path = o2.reconstruct_chain(oxygen)
print(len(path))
