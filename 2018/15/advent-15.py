from operator import itemgetter
from collections import OrderedDict

class Unit:
    def __init__(self,the_type:str,loc:tuple):
        self.type = the_type
        self.ap = 3
        self.hp = 200
        self.location = loc
    
    def __repr__(self):
        return f"Unit({self.type}:{self.hp})"

    def attacked_by(self,enemy,grid):
        self.hp -= enemy.ap
        if self.hp <= 0:
            self.dies(grid)
    
    def dies(self,container):
        container.byebye(self.location)

class Cave:
    def __init__(self,filename):
        with open(filename) as f:
            content = f.read().splitlines()
        self.grid = []
        for line in content:
            row = [x for x in line]
            self.grid.append(row)
        self.max_row = len(self.grid)
        self.max_column = len(self.grid[0])
        self.units = {}
        self.elves = {}
        self.goblins = {}
        for i, row in enumerate(self.grid):
            for j, column in enumerate(row):
                if column == 'G':
                    self.units[(i,j)] = 'G'
                    self.goblins[(i,j)] = Unit('G',(i,j))
                elif column == 'E':
                    self.units[(i,j)] = 'E'
                    self.elves[(i,j)] = Unit('E',(i,j))
    
    def __repr__(self):
        return f"Cave(Dim:{self.max_row}x{self.max_column},Units:{len(self.units)})"

    def __str__(self):
        lines = [''.join(row) for row in self.grid]
        lines.append(f"Goblins: {self.goblins}")
        lines.append(f"Elves: {self.elves}")
        return '\n'.join(lines)
    
    def is_open(self,square:tuple):
        try:
            if self.grid[square[0]][square[1]] == ".":
                return True
            else:
                return False
        except IndexError:
            return False

    def in_range(self,square:tuple):
        i = square[0]
        j = square[1]
        open_squares = []
        try_squares = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
        for s in try_squares:
            if self.is_open(s):
                open_squares.append(s)
        return open_squares

    def attack_range(self,who:Unit):
        attack_squares = []
        if who.type == 'E':
            they = 'G'
        elif who.type == 'G':
            they = 'E'
        i = who.location[0]
        j = who.location[1]
        try_squares = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
        for s in try_squares:
            if s in self.units and self.units[s] == they:
                attack_squares.append(s)
        return attack_squares

    def choose_attackee(self,who:Unit):
        if who.type == 'E':
            enemies = self.goblins
        elif who.type == 'G':
            enemies = self.elves
        targets = self.attack_range(who)
        comp_list = []
        if targets != []:
            for t in targets:
                victim = enemies[t]
                comp_list.append((victim.hp,t,victim))
        comp_list.sort(key=itemgetter(0,1))
        return comp_list[0][2]

    def target_ranges(self,targets:list):
        return [x for unit in targets for x in self.in_range(unit)]

    def find_path(self,start:tuple,end:tuple):
        queue = [(start, [])]
        visited = set()
        while len(queue) > 0:
            node, path = queue.pop(0)
            path.append(node)
            visited.add(node)
            if node == end:
                return path
            neighbors = self.in_range(node)
            for item in neighbors:
                if item not in visited:
                    queue.append((item,path[:]))
        return None
    
    def choose_target_cell(self,who:Unit,start:tuple):
        if who.type == 'E':
            target_cells = self.target_ranges(self.goblins)
        elif who.type == 'G':
            target_cells = self.target_ranges(self.elves)
        if target_cells == []:
            return None
        else:
            paths = [self.find_path(start,x) for x in target_cells]
            steps = [(len(x),x[-1],x[1]) for x in paths if x is not None]
            if steps == []:
                return None
            else:
                steps.sort()
                return steps[0][2]
    
    def byebye(self,square:tuple):
        removed_unit = self.units.pop(square)
        if removed_unit == 'E':
            del self.elves[square]
        elif removed_unit == 'G':
            del self.goblins[square]
        self.grid[square[0]][square[1]] = '.'
    
    def move(self,source:tuple,destination:tuple):
        rep = self.units.pop(source)
        if rep == 'G':
            group = self.goblins
        elif rep == 'E':
            group = self.elves
        unit = group.pop(source)
        unit.location = destination
        self.grid[source[0]][source[1]] = '.'
        self.grid[destination[0]][destination[1]] = rep
        self.units[destination] = rep
        group[destination] = unit

    def rounds(self,n=1000):
        round_n = 0
        while round_n < n:
            yield self, round_n
            #start round
            round_n += 1
            units = sorted([(k,v) for k,v in self.units.items()])
            for i in units:
                #look for targets
                if i[1] == 'E':
                    unit = self.elves[i[0]]
                    enemies = self.goblins
                elif i[1] == 'G':
                    unit = self.goblins[i[0]]
                    enemies = self.elves
                if enemies == {}:
                    break
                #move (if necessary)
                if self.attack_range(unit) == []:
                    next_step = self.choose_target_cell(unit,unit.location)
                    if next_step is not None:
                        self.move(unit.location,next_step)
                #attack (if possible)
                if self.attack_range(unit) != []:
                    victim = self.choose_attackee(unit)
                    victim.attacked_by(unit,self)
            if self.goblins == {} or self.elves == {}:
                break
        yield self, round_n
    
    def outcome(self):
        for r,n in self.rounds():
            round_no = n
        if cave.elves == {}:
            winners = cave.goblins
        elif cave.goblins == {}:
            winners = cave.elves
        remaining_hp = sum([v.hp for k,v in winners.items()])
        return remaining_hp*round_no

cave = Cave("test-1.txt")
#cave = Cave("input.txt")
print(cave.outcome())