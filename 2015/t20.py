import lib

def main():
    content = lib.read_content()
    target = int(content) // 10

    house = 0
    while True:
        house += 1
        presents = 0
        for elve in range(1, house+1):
            if house % elve == 0:
                presents += elve
        if presents >= target:
            break
        print(house, presents)
        if house > 5041:
            break

    result1 = house
    print(result1)

    result2 = 0
    print(result2)

if __name__ == "__main__":
    main()
