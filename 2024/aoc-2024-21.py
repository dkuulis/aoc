import sys
import re

def leading_int(s):
    match = re.match(r'^(\d+)', s)
    return int(match.group(1)) if match else None

def parse(lines):
    codes = [line.strip() for line in lines]
    return codes

alphanum_keys = {
    '7': (0,0), '8': (1,0), '9': (2,0),
    '4': (0,1), '5': (1,1), '6': (2,1),
    '1': (0,2), '2': (1,2), '3': (2,2),
    ' ': (0,3), '0': (1,3), 'A': (2,3)
}

dir_keys = {
    ' ': (0,0), '^': (1,0), 'A': (2,0),
    '<': (0,1), 'v': (1,1), '>': (2,1)
}

def encode_buttons(code, keys):
    seq = []
    p = 'A'
    bx, by = keys[' ']

    for c in code:
        if p != c:
            cx, cy = keys[p]
            tx, ty = keys[c]

            if tx - cx < 0 and (tx != bx or cy != by): # need to move left via (tx, cy)
                seq.extend(['<'] * (cx - tx))
                cx = tx

            if ty - cy > 0 and (cx != bx or ty != by): # need to move down via (cx, ty)
                seq.extend(['v'] * (ty - cy))
                cy = ty

            if ty - cy < 0 and (cx != bx or ty != by): # need to move up via (cx, ty)
                seq.extend(['^'] * (cy - ty))
                cy = ty

            if tx > cx and (tx != bx or cy != by): # need to move right via (tx, cy)
                seq.extend(['>'] * (tx - cx))
                cx = tx

            # rest of movement
            if tx - cx < 0: # need to move left
                seq.extend(['<'] * (cx - tx))

            if ty - cy > 0: # need to move down
                seq.extend(['v'] * (ty - cy))

            if ty - cy < 0: # need to move up
                seq.extend(['^'] * (cy - ty))

            if tx > cx: # need to move right
                seq.extend(['>'] * (tx - cx))

        seq.append('A')
        p = c

    return seq

def all_buttons2_len(code):

    r1_code = encode_buttons(code, alphanum_keys)
    r2_code = encode_buttons(r1_code, dir_keys)
    r3_code = encode_buttons(r2_code, dir_keys)

    return len(r3_code)

def get_pairs(s):
    return [s[i:i+2] for i in range(len(s) - 1)]

encodings = {}

def encode_len(p, c, alpha, limit):

    if limit == 0:
        return 1

    ref = (p, c, alpha, limit)
    if ref in encodings:
        return encodings[ref]

    keys = alphanum_keys if alpha else dir_keys

    seq = ['A']
    if p != c:
        bx, by = keys[' ']
        cx, cy = keys[p]
        tx, ty = keys[c]

        if tx - cx < 0 and (tx != bx or cy != by): # need to move left via (tx, cy)
            seq.extend(['<'] * (cx - tx))
            cx = tx

        if ty - cy > 0 and (cx != bx or ty != by): # need to move down via (cx, ty)
            seq.extend(['v'] * (ty - cy))
            cy = ty

        if ty - cy < 0 and (cx != bx or ty != by): # need to move up via (cx, ty)
            seq.extend(['^'] * (cy - ty))
            cy = ty

        if tx > cx and (tx != bx or cy != by): # need to move right via (tx, cy)
            seq.extend(['>'] * (tx - cx))
            cx = tx

        # rest of movement
        if tx - cx < 0: # need to move left
            seq.extend(['<'] * (cx - tx))

        if ty - cy > 0: # need to move down
            seq.extend(['v'] * (ty - cy))

        if ty - cy < 0: # need to move up
            seq.extend(['^'] * (cy - ty))

        if tx > cx: # need to move right
            seq.extend(['>'] * (tx - cx))

    seq.append('A')

    length = 0

    for p2, c2 in get_pairs(seq):
        length += encode_len(p2, c2, False, limit - 1)

    encodings[ref] = length
    return length

def all_buttons25_len(code):

    length = 0
    code = 'A' + code

    for p, c in get_pairs(code):
        length += encode_len(p, c, True, 26)

    return length

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    codes = parse(lines)

    result1 = sum(all_buttons2_len(code) * leading_int(code) for code in codes)
    print(result1)

    result2 = sum(all_buttons25_len(code) * leading_int(code) for code in codes)
    print(result2)

if __name__ == "__main__":
    main()
