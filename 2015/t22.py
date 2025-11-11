import re
from itertools import count
from dataclasses import dataclass
from typing import List
import lib

@dataclass
class State:
    boss_hp: int

    player_hp: int
    player_mana: int

    spells: List[int]

    player_spend: int
    min_spend: int

    turn: int

spells = ["Recharge", "Poison", "Shield", "Drain", "Missile"]
costs = [229, 173, 113, 73, 53]
durations = [5, 6, 6, 1, 1]
damages = [0, 3, 0, 2, 4]
hps = [0, 0, 0, 2, 0]
shields = [0, 0, 7, 0, 0]
recharges = [101, 0, 0, 0, 0]

RECHARGE = 0
POISON = 1
SHIELD = 2
DRAIN = 3
MISSILE = 4

SPELL_COUNT = 5

min_cost = min(costs)
boss_damage = 0

def spell_stream(n: int):
    while True:
        s = n % SPELL_COUNT
        n = n // SPELL_COUNT
        yield s
        if n == 0:
            return

def effects(state: State):

    state.turn += 1

    # hard option
    state.player_hp -= 1
    if state.player_hp <= 0:
        return False

    for i in range(SPELL_COUNT):
        if state.spells[i] > 0:

            # wear off
            state.spells[i] -= 1

            # apply
            state.boss_hp -= damages[i]
            state.player_hp += hps[i]
            state.player_mana += recharges[i]

    return state.boss_hp > 0

def apply(state: State, spell_index: int):

    cost = costs[spell_index]
    state.player_mana -= cost

    # lose if out of mana
    if state.player_mana < 0: 
        return False

    # repeat use illegal
    if state.spells[spell_index] > 0:
        return False

    state.player_spend += cost

    # unoptimal
    if state.player_spend >= state.min_spend:
        return False

    state.spells[spell_index] = durations[spell_index]

    return True

def boss(state: State):
    armor = sum(shields[i] if state.spells[i] > 0 else 0 for i in range(SPELL_COUNT))
    damage = max(boss_damage - armor, 1)
    state.player_hp -= damage
    return state.player_hp > 0 # no game end

def execute(case: int, state: State):

    for spell_index in spell_stream(case):
        if not (effects(state) and apply(state, spell_index) and effects(state) and boss(state)):
            break

    return state

def win(state):
    return state.boss_hp <= 0

def report(i: int, state: State):
    s = [spells[s] for s in spell_stream(i)]
    print(s, state.boss_hp, state.player_hp, state.player_mana, state.turn, state.player_spend, state.min_spend) 

def play(boss_hp):

    min_spend = 9999999
    min_boss = 9999999

    turn = 1
    turn_limit = SPELL_COUNT

    for i in count(0):

        if i >= turn_limit:
            turn += 2
            turn_limit *= SPELL_COUNT

        state = State(boss_hp, 50, 500, [0]*SPELL_COUNT, 0, min_spend, 0)
        execute(i, state)

        if state.boss_hp < min_boss and state.turn == turn:
            report(i, state)
            min_boss = state.boss_hp

        if win(state):
            report(i, state)
            min_spend = min(min_spend, state.player_spend)

    return min_spend

pattern = r"Hit Points: (?P<hp>\d+).*Damage: (?P<damage>\d+)"

def main():
    global boss_damage

    content = lib.read_content()
    data  = lib.ints(re.search(pattern, content, re.DOTALL).groupdict())
    boss_damage = data["damage"]

    result = play(data["hp"])
    print(result) # never reached - use reporting

if __name__ == "__main__":
    main()
