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
    n = in_int()
    a = in_int_list()

    # s = set(a)
    # if 0 not in s:
    #     print(1)
    #     print(f'{1} {n}')

    res = []
    if n > 4:
        res += [(4, n)]
        a = a[:3] + [1 if 0 in set(a[3:]) else 0]
        # print('\nextended', a)

    zeros = sum(x == 0 for x in a)

    if zeros == 0:
        res += [(1, 4)]
    if zeros == 1:
        if a[0] == 0:
            res += [(1, 2), (1, 3)]
        elif a[1] == 0:
            res += [(1, 2), (1, 3)]
        elif a[2] == 0:
            res += [(3, 4), (1, 3)]
        elif a[3] == 0:
            res += [(3, 4), (1, 3)]
    if zeros == 2:
        if a[0] == 0 and a[1] == 0:
            res += [(1, 2), (1, 3)]
        elif a[2] == 0 and a[3] == 0:
            res += [(3, 4), (1, 3)]
        else:
            res += [(1, 2), (2, 3), (1, 2)]
    if zeros == 3:
        if a[0] != 0:
            res += [(2, 4), (1, 2)]
        elif a[1] != 0:
            res += [(1, 2), (2, 3), (1, 2)]
        elif a[2] != 0:
            res += [(1, 2), (2, 3), (1, 2)]
        elif a[3] != 0:
            res += [(1, 3), (1, 2)]
    if zeros == 4:
        res += [(1, 2), (2, 3), (1, 2)]

    print(len(res))
    for t in res:
        print(' '.join(map(str, t)))


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
