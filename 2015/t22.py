import re
from dataclasses import dataclass
from itertools import combinations
import lib

@dataclass
class Boss:
    hp: int
    damage: int

@dataclass
class Player:
    hp: int
    mana: int
    spend: int
    effects: dict
    armor: int

@dataclass
class State:
    player: Player
    boss: Boss

spells = {
    "Magic Missile": {"cost": 53, "damage": 4},
    "Drain": {"cost": 73, "damage": 2, "heal": 2},
    "Shield": {"cost": 113, "effect": 6, "armor": 7},
    "Poison": {"cost": 173, "effect": 6, "damage": 3},
    "Recharge": {"cost": 229, "effect": 5, "mana": 101}
}

min_cost = min(spell["cost"] for spell in spells.values())

def apply_missile(state: State):
    state.boss.hp -= 2
    return True

def apply_drain(state: State):
    state.player.hp += 2
    state.boss.hp -= 2
    return True

def apply_effect(player: Player, boss: Boss, effect:str):
    if effect in player.effects

def effect_shield(player: Player, _: Boss):
    player.armor = 7

def effect_poison(_: Player, boss: Boss):
    boss.hp -= 3

def effect_recharge(player: Player, _: Boss):
    player.mana += 101

def effects(player: Player, boss: Boss, turn: int):
    player.armor = 0
    for e in player.effects:
        if e.end > turn:
            e.apply(player, boss)

def check_victory(boss: Boss):
    return False

def go_player(p0: Player, b0: Boss, turn: int, history: list):

    p1, b1 = effects(p0, b0)
    yield check_victory(p1, b1, history)

    for name, spell in spells.items():
        if spell.cost >= p1.mana:
            actions = history + [name]
            p2, b2 = spell.apply(p1, b1, turn)
            yield check_victory(p2, b2, actions)


def go_boss(player: Player, boss: Boss, history: list):
    effects(player, boss)
    check_victory(boss)
    pass

pattern = r"Hit Points: (?P<hp>\d+).*Damage: (?P<damage>\d+)"

def main():
    content = lib.read_content()
    data  = lib.ints(re.search(pattern, content, re.DOTALL).groupdict())
    boss = Boss(**data)
    player = Player(50, 500, [])

    options = go_player(player, boss, [])

    result1 = 0
    print(result1)

    result2 = 0
    print(result2)

if __name__ == "__main__":
    main()
