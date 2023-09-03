from random import choice
from time import sleep

Letters = ["A", "B", "C", "D", "E", "F"]


def RandomWordHexa(lenght=5, loop=1):
    word = ""
    loop -= 1
    for i in range(lenght):
        word += choice(Letters)
    print(word)
    sleep(0.5)
    if loop > 0:
        RandomWordHexa(lenght, loop)


if __name__ == "__main__":
    RandomWordHexa(6, 10)
