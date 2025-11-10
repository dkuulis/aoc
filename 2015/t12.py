import re
import json
import lib

def add(obj, exclude):

    if isinstance(obj, int):
        return obj

    if isinstance(obj, list):
        return sum(add(e, exclude) for e in obj)
    
    if isinstance(obj, dict):
        if exclude in obj.values():
            return 0

        return sum(add(e, exclude) for e in obj.values())
    
    return 0

def main():
    content = lib.read_content()
    obj = json.loads(content)
    
    # sum(int(m[0]) for m in re.finditer(r"-?\d+", content))
    result1 = add(obj, None)
    print(result1)

    result2 = add(obj, "red")
    print(result2)

if __name__ == "__main__":
    main()
