import re
from collections import namedtuple
from functools import reduce
import lib

Reindeer = namedtuple('Reindeer', ["name", "speed", "fly", "rest"])
pattern  = r"(?P<name>\w+) can fly (?P<speed>\d+) km/s for (?P<fly>\d+) seconds, but then must rest for (?P<rest>\d+) seconds\."

def distance(reindeer, time):
    period = reindeer.fly + reindeer.rest
    cycles = time // period
    reminder = time % period
    flytime = reindeer.fly * cycles + min(reminder, reindeer.fly)
    return flytime * reindeer.speed

def points(distances):
    m = max(distances)
    return [1 if d == m else 0 for d in distances]

def distances(reindeers, time):
    return [distance(r, time) for r in reindeers]

def main():
    lines = lib.read_lines()
    data = [lib.ints(re.match(pattern, line).groupdict()) for line in lines]

    reindeers = [Reindeer(**d) for d in data]
    duration = 2503

    result1 = max(distance(r, duration) for r in reindeers)
    print(result1)

    pts = (points(distances(reindeers, t)) for t in range(1, duration+1))
    result2 = max(reduce(lambda a, b: [x + y for x, y in zip(a, b)], pts))
    print(result2)

if __name__ == "__main__":
    main()
