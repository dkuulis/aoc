import re
from dataclasses import dataclass
from itertools import combinations
import lib

@dataclass
class State:
    boss_hp: int
    player_hp: int
    player_mana: int
    player_spend: int
    turn: int
    effect_shield: int
    effect_poison: int
    effect_recharge: int
    min_spend: int

spells = {
    "Missile": 53,
    "Drain":  73,
    "Shield": 113,
    "Poison": 173,
    "Recharge": 229
}

MIN_COST = min(cost for cost in spells.values())

boss_damage = 0

def check_victory(state: State, player_move: bool):
    if state.boss_hp <= 0:
        state.min_spend = min(state.min_spend, state.player_spend)
        return (True, state.player_spend, state.turn)

    if state.player_hp <= 0:
        return (False, state.player_spend, state.turn)

    if player_move and state.player_mana < MIN_COST:
        return (False, state.player_spend, state.turn)

    if player_move and state.min_spend < state.player_spend:
        return (False, state.player_spend, state.turn) # cutoff

    return None # indecisive

def do_effects(state: State):

    # shield effect accounted in do_damage_player
    # status.effect_shield

    if state.effect_poison > state.turn:
        state.boss_hp -= 3

    if state.effect_recharge > state.turn:
        state.player_mana += 101

    state.turn += 1

def undo_effects(state: State):

    state.turn -= 1

    # shield effect accounted in do_damage_player

    if state.effect_poison > state.turn:
        state.boss_hp += 3

    if state.effect_recharge > state.turn:
        state.player_mana -= 101

def applicable(name: str, state: State):

    cost = spells[name]
    if state.player_mana < cost:
        return False

    if name == "Shield" and state.effect_shield > state.turn:
        return False
    if name == "Poison" and state.effect_poison > state.turn:
        return False
    if name == "Rechagre" and state.effect_recharge > state.turn:
        return False

    return True

def do_spell(name: str, state: State):

    cost = spells[name]
    state.player_mana -= cost
    state.player_spend += cost

    if name == "Missile":
        state.boss_hp -= 4
        undo = None

    elif name == "Drain":
        state.boss_hp -= 2
        state.player_mana += 2
        undo = None

    elif name == "Shield":
        undo = state.effect_shield
        state.effect_shield = state.turn + 6

    elif name == "Poison":
        undo = state.effect_poison
        state.effect_poison = state.turn + 6

    elif name == "Recharge":
        undo = state.effect_recharge
        state.effect_recharge = state.turn + 5

    return undo

def undo_spell(name: str, state: State, undo):

    cost = spells[name]
    state.player_mana += cost
    state.player_spend -= cost

    if name == "Missile":
        state.boss_hp += 4

    elif name == "Drain":
        state.boss_hp += 2
        state.player_mana -= 2

    elif name == "Shield":
        state.effect_shield = undo

    elif name == "Poison":
        state.effect_poison = undo

    elif name == "Recharge":
        state.effect_recharge = undo

def do_damage_player(state: State):
    damage = boss_damage - (7 if state.effect_shield > state.turn else 0)
    state.player_hp -= damage

def undo_damage_player(state: State):
    damage = boss_damage - (7 if state.effect_shield > state.turn else 0)
    state.player_hp += damage

def play(state: State, player_move: bool):

    do_effects(state)
    victory = check_victory(state, player_move)
    if victory:
        yield victory

    else: # do the moves
        if player_move:
            for spell in spells.keys():
                if applicable(spell, state):
                    undo = do_spell(spell, state)
                    victory = check_victory(state, False) # spell kills boss
                    if victory:
                        yield victory
                    else:
                        yield from play(state, False) # newx turn
                    undo_spell(spell, state, undo)

        else:
            do_damage_player(state)
            victory = check_victory(state, False) # damage kills player
            if victory:
                yield victory
            else:
                yield from play(state, True) # newx turn
            undo_damage_player(state)

    undo_effects(state)

pattern = r"Hit Points: (?P<hp>\d+).*Damage: (?P<damage>\d+)"

def main():
    global boss_damage

    content = lib.read_content()
    data  = lib.ints(re.search(pattern, content, re.DOTALL).groupdict())
    boss_damage = data["damage"]

    state = State(data["hp"], 50, 500, 0, 1, 0, 0, 0, 9999999)
    result = list(play(state, True))
    result1 = state.min_spend
    print(result1)

    result2 = 0
    print(result2)

if __name__ == "__main__":
    main()
