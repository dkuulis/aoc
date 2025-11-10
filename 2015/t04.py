import hashlib
import lib


def main():
    content = lib.read_content()

    i = 0
    while True:
        i += 1

        data = content + str(i)

        # Create MD5 hash object
        md5_hash = hashlib.md5()
        md5_hash.update(data.encode('utf-8'))
        md5_digest = md5_hash.hexdigest()

        if md5_digest.startswith("000000"):
            print(i)
            break

if __name__ == "__main__":
    main()
