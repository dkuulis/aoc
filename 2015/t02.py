import lib

def paper(box):

    areas = (box[0]*box[1], box[1]*box[2], box[2]*box[0])
    minimal = min(areas)
    return 2*(sum(areas)) + minimal

def ribbon(box):

    half_perimeters = (box[0]+box[1], box[1]+box[2], box[2]+box[0])
    bow = box[0]*box[1]*box[2]
    return 2*min(half_perimeters) + bow

def main():
    lines = lib.read_lines()
    dimensions = [tuple(map(int, line.split('x'))) for line in lines]

    result1 = sum(paper(box) for box in dimensions)
    print(result1)

    result1 = sum(ribbon(box) for box in dimensions)
    print(result1)

if __name__ == "__main__":
    main()
