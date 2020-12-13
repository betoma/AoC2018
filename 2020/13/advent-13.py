from datetime import datetime


class BusStop:
    def __init__(self, filename: str):
        with open(filename) as f:
            content = [line.strip() for line in f.readlines()]
        self.earliest = int(content[0])
        self.id_list = [int(n) if n != "x" else n for n in content[1].split(",")]
        self.busses = [b for b in self.id_list if b != "x"]

    def departures(self, start: int = 0):
        minute = start
        while True:
            if minute == 0:
                yield minute, self.busses
            elif b := [bus for bus in self.busses if minute % bus == 0]:
                yield minute, b
            minute += 1

    def by_minute(self, start: int = 0):
        minute = start
        while True:
            if minute == 0:
                yield minute, self.busses
            else:
                yield minute, [bus for bus in self.busses if minute % bus == 0]
            minute += 1

    def earliest_bus(self):
        bus_times = self.departures(self.earliest)
        return next(bus_times)

    def bus_difference(self):
        minute, busses = self.earliest_bus()
        time_diff = minute - self.earliest
        return time_diff * busses[0]

    def contest(self):
        nec_cond = len(self.id_list)
        cond = 0
        for minute, departure in self.by_minute():
            if cond == nec_cond:
                break
            else:
                current_c = self.id_list[cond]
                if current_c == "x":
                    cond += 1
                elif current_c in departure:
                    cond += 1
                else:
                    cond = 0
                    continue
                if cond == 1:
                    t = minute
        return t


begin_time = datetime.now()

shuttle = BusStop("test.txt")

# part one
print(shuttle.bus_difference())

# part two (too slow to verify, need to rewrite)
print(shuttle.contest())
