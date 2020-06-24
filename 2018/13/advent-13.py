from operator import methodcaller


class Cart:
    """
    a cart on the track, takes coordinates and a direction
    """

    def __init__(self, start, direction):
        self.loc = start
        self.dir = direction
        self.last_turn = None

    def __repr__(self):
        return repr((self.dir, self.loc, self.last_turn))

    def x(self):
        return self.loc[0]

    def y(self):
        return self.loc[1]

    def left_turn(self):
        """
        returns the result of a left turn given the cart's current direction
        """
        if self.dir == ">":
            return "^"
        elif self.dir == "^":
            return "<"
        elif self.dir == "<":
            return "v"
        elif self.dir == "v":
            return ">"

    def right_turn(self):
        """
        returns the result of a right turn given the cart's current direction
        """
        if self.dir == ">":
            return "v"
        elif self.dir == "v":
            return "<"
        elif self.dir == "<":
            return "^"
        elif self.dir == "^":
            return ">"

    def curve(self, curve):
        """
        changes the cart's direction in place when it encounters a curve
        """
        if curve == "/":
            if self.dir in {"^", "v"}:
                next_dir = self.right_turn()
            elif self.dir in {">", "<"}:
                next_dir = self.left_turn()
        elif curve == "\\":
            if self.dir in {"^", "v"}:
                next_dir = self.left_turn()
            elif self.dir in {">", "<"}:
                next_dir = self.right_turn()
        self.dir = next_dir

    def intersection(self):
        """
        changes the cart's direction in place correctly at an intersection
        """
        if self.last_turn in {None, "right"}:
            turn_dir = "left"
        elif self.last_turn == "left":
            turn_dir = "straight"
        elif self.last_turn == "straight":
            turn_dir = "right"
        self.last_turn = turn_dir
        if turn_dir == "left":
            new_dir = self.left_turn()
        elif turn_dir == "right":
            new_dir = self.right_turn()
        elif turn_dir == "straight":
            new_dir = self.dir
        self.dir = new_dir

    def advance(self):
        """
        changes the coordinates as the cart moves -- make sure you update the cart's direction first!
        """
        x = self.x()
        y = self.y()
        if self.dir in {"<", ">"}:
            new_y = y
            if self.dir == "<":
                new_x = x - 1
            elif self.dir == ">":
                new_x = x + 1
        elif self.dir in {"^", "v"}:
            new_x = self.loc[0]
            if self.dir == "^":
                new_y = y - 1
            elif self.dir == "v":
                new_y = y + 1
        self.loc = (new_x, new_y)


class Track:
    """
    takes the name of a file containing a map of a set of tracks and turns it into info about the state of the set of tracks
    """

    def __init__(self, file_name):
        self.tracks = dict()
        self.carts = list()
        self.spots = dict()
        with open(file_name) as f:
            content = f.read()
        rows = content.splitlines()
        for y, row in enumerate(rows):
            for x, char in enumerate(list(row)):
                if char in {"|", "+", "/", "\\", "-"}:
                    self.tracks[(x, y)] = char
                elif char in {">", "<", "^", "v"}:
                    new_cart = Cart((x, y), char)
                    self.carts.append(new_cart)
                    self.spots[(x, y)] = new_cart
                    if char in {">", "<"}:
                        self.tracks[(x, y)] = "-"
                    else:
                        self.tracks[(x, y)] = "|"

    def move_the_carts(self, crash_threshold=1):
        spots = self.spots
        carts = self.carts
        crash = 0
        while crash < crash_threshold:
            yield spots
            carts.sort(key=methodcaller("y"))
            for cart in carts:
                place = cart.loc
                this_spot = spots.pop(place)
                if this_spot == "X":
                    continue
                rails = self.tracks[place]
                if rails == "+":
                    cart.intersection()
                elif rails in {"/", "\\"}:
                    cart.curve(rails)
                cart.advance()
                if cart.loc in spots:
                    crash += 1
                    spots[cart.loc] = "X"
                else:
                    spots[cart.loc] = cart
            crashes = [k for k, v in spots.items() if v == "X"]
            for k in crashes:
                del spots[k]
            carts = [x for x in spots.values()]
        yield spots

    def crashes_before(self, n):
        n_carts = len(self.carts)
        carts_that_will_crash = n_carts - n
        no_crashes = carts_that_will_crash / 2
        return int(no_crashes)


# xmas_track = Track("test.txt")
# xmas_track = Track("test-2.txt")
xmas_track = Track("input.txt")

for tick in xmas_track.move_the_carts(crash_threshold=xmas_track.crashes_before(1)):
    print(tick)
