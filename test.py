import time


def main():
    i = 0
    while True:
        print(i)
        i += i
        time.sleep(60)


if __name__ == '__main__':
    main()
