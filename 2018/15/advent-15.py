from collections import OrderedDict

class Unit:
    def __init__(self,the_type:str,loc:tuple):
        self.type = the_type
        self.ap = 3
        self.hp = 200
        self.location = loc

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
        units = {}
        self.elves = {}
        self.goblins = {}
        for i, row in enumerate(self.grid):
            for j, column in enumerate(row):
                if column == 'G':
                    units[(i,j)] = 'G'
                    self.goblins[(i,j)] = Unit('G',(i,j))
                elif column == 'E':
                    units[(i,j)] = 'E'
                    self.elves[(i,j)] = Unit('E',(i,j))
        self.units = OrderedDict(sorted(units.items()))
    
    def __repr__(self):
        return f"Cave(Dim:{self.max_row}x{self.max_column},Units:{len(self.units)})"

    def __str__(self):
        lines = [''.join(row) for row in self.grid]
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

    def attack_range(self,who:Unit,square:tuple):
        attack_squares = []
        if who.type == 'E':
            they = 'G'
        elif who.type == 'G':
            they = 'E'
        i = square[0]
        j = square[1]
        try_squares = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
        for s in try_squares:
            if s in self.units and self.units[s] == they:
                attack_squares.append(s)
        return attack_squares

    def choose_attackee(self,who:Unit,square:tuple):
        if who.type == 'E':
            enemies = self.goblins
        elif who.type == 'G':
            enemies = self.elves
        targets = self.attack_range(who,square)
        comp_list = []
        if targets != []:
            for t in targets:
                comp_list.append((enemies[t].hp,t,enemies[t]))
        comp_list.sort
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
        paths = [self.find_path(start,x) for x in target_cells]
        steps = [(len(x),x[-1],x[1]) for x in paths if x is not None]
        steps.sort()
        return steps[0][2]
    
    def byebye(self,square:tuple):
        removed_unit = self.units.pop(square)
        if removed_unit == 'E':
            del self.elves[square]
        elif removed_unit == 'G':
            del self.goblins[square]
        self.grid[square[0]][square[1]] = '.'
    
    def move(self,etc.):
        #do later

    def rounds(self):
        round_n = 0
        while True:
            yield self
            #start round
            round_n += 1
            for i in self.units:
                #look for targets
                if self.units[i] == 'E':
                    unit = self.elves[i]
                    enemies = self.goblins
                elif self.units[i] == 'G':
                    unit = self.goblins[i]
                    enemies = self.elves
                if enemies == {}:
                    break
                #check if in range
                #move if not
                #attack if yes
            if self.goblins == {} or self.elves == {}:
                break
        yield self

cave = Cave("test-1.txt")
#cave = Cave("input.txt")
print(cave.choose_target_cell('E',(1,1)))