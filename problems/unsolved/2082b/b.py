import sys

import os
from io import BytesIO, IOBase

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._file = file
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")


def in_int():
    return (int(input()))


def in_ints():
    return (map(int, input().split()))


def in_int_list():
    return (list(map(int, input().split())))


def in_string():
    return input()


def in_string_list():
    s = in_string()
    return (list(s[:len(s)]))


def solve():
    x, floor, ceil = in_ints()

    if floor + ceil > 30:
        print(0, 0)
        return

    n = 0
    x_ = x
    while x_ % 2 == 0:
        x_ = x_ // 2
        n += 1

    # print()
    # print('a')
    # min
    a = min(n, ceil)
    b = floor
    c = max(ceil - a, 0)
    x_min = x
    x_min = x_min // (2 ** a)
    x_min = x_min // (2 ** b)
    # while b > 0 and x_min:
    #     x_min = x_min // 2
    #     b -= 1
    # print('b')
    while c > 0 and x_min > 1:
        x_min += 1
        x_min = x_min // 2
        c -= 1

    # max
    a = min(n, floor)
    b = ceil
    c = max(floor - a, 0)
    # print(a, b, c)
    x_max = x
    x_max = x_max // (2 ** a)
    while b > 0 and x_max > 1:
        x_max += 1
        x_max = x_max // 2
        b -= 1
    # print('c')
    x_max = x_max // (2 ** c)
    # while c > 0 and x_max:
    #     x_max = x_max // 2
    #     c -= 1
    print(x_min, x_max)


def solve_n():
    testcases = int(input())  # multiple testcases
    for _ in range(testcases):
        solve()


if __name__ == "__main__":
    if os.path.exists('input.txt'):
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")

    # solve()
    solve_n()

    # from utils.utils import check_results
    # sys.stdout = sys.__stdout__
    # print(check_results())
