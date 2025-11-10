import lib

def rle(s):

    encoded = []

    count = 1
    prev = s[0]
    
    for char in s[1:]:
        if char == prev:
            count += 1
        else:
            encoded.append(f"{count}{prev}")
            prev = char
            count = 1

    encoded.append(f"{count}{prev}")
    return ''.join(encoded)

def main():
    content = lib.read_content()
    code = content

    for _ in range(40):
        code = rle(code)
    result1 = len(code)
    print(result1)


    for _ in range(10):
        code = rle(code)
    result2 = len(code)
    print(result2)

if __name__ == "__main__":
    main()
