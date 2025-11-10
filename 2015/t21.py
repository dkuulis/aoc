import re
from collections import namedtuple
from itertools import combinations
import lib

Fighter = namedtuple("Fighter", ["hp", "damage", "armor"])

weapons = {
    "Dagger": { "cost": 8, "damage": 4, "armor": 0},
    "Shortsword": { "cost": 10, "damage": 5, "armor": 0},
    "Warhammer": { "cost": 25, "damage": 6, "armor": 0},
    "Longsword": { "cost": 40, "damage": 7, "armor": 0},
    "Greataxe": { "cost": 74, "damage": 8, "armor": 0}
}

armors = {
    "None": { "cost": 0, "damage": 0, "armor": 0},
    "Leather": { "cost": 13, "damage": 0, "armor": 1},
    "Chainmail": { "cost": 31, "damage": 0, "armor": 2},
    "Splintmail": { "cost": 53, "damage": 0, "armor": 3},
    "Bandedmail": { "cost": 75, "damage": 0, "armor": 4},
    "Platemail": { "cost": 102, "damage": 0, "armor": 5}
}

rings = {
    "None 1": { "cost": 0, "damage": 0, "armor": 0},
    "None 2": { "cost": 0, "damage": 0, "armor": 0},
    "Damage +1": { "cost": 25, "damage": 1, "armor": 0},
    "Damage +2": { "cost": 50, "damage": 2, "armor": 0},
    "Damage +3": { "cost": 100, "damage": 3, "armor": 0},
    "Defense +1": { "cost": 20, "damage": 0, "armor": 1},
    "Defense +2": { "cost": 40, "damage": 0, "armor": 2},
    "Defense +3": { "cost": 80, "damage": 0, "armor": 3}
}

def i_win(me, boss):
    my_damage = max(1, me.damage - boss.armor)
    boss_damage = max(1, boss.damage - me.armor)
    my_turns = (boss.hp + my_damage - 1) // my_damage
    boss_turns = (me.hp + boss_damage - 1) // boss_damage
    return my_turns <= boss_turns

def generate(hp):
    for wn, w in weapons.items():
        for an, a in armors.items():
            for r1, r2 in combinations(rings.items(), 2):
                cost = w["cost"] + a["cost"] + r1[1]["cost"] + r2[1]["cost"]
                damage = w["damage"] + a["damage"] + r1[1]["damage"] + r2[1]["damage"]
                armor = w["armor"] + a["armor"] + r1[1]["armor"] + r2[1]["armor"]
                yield cost, Fighter(hp, damage, armor), [wn, an, r1[0], r2[0]]

pattern = r"Hit Points: (?P<hp>\d+).*Damage: (?P<damage>\d+).*Armor: (?P<armor>\d+)"

def main():
    content = lib.read_content()
    data  = lib.ints(re.search(pattern, content, re.DOTALL).groupdict())
    boss = Fighter(**data)

    options = list((cost, desc, i_win(me, boss), me) for cost, me, desc in generate(100))
    
    options1 = [o for o in options if o[2]]
    result1 = min(options1, key=lambda x: x[0])
    print(result1)

    options2 = [o for o in options if not o[2]]
    result2 = max(options2, key=lambda x: x[0])
    print(result2)

if __name__ == "__main__":
    main()
