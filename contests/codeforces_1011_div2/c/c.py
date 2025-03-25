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


def check(x, y):
    x = list(bin(x)[2:])
    y = list(bin(y)[2:])

    delta = abs(len(x) - len(y))
    if len(x) < len(y):
        x = ['0'] * (delta + 1) + x
        y = ['0'] + y
    else:
        x = ['0'] + x
        y = ['0'] * (delta + 1) + y

    for a, b in zip(x, y):
        if a == b == '1':
            return False
    return True


def update(x, y, reversed=False):
    x = list(bin(x)[2:])
    y = list(bin(y)[2:])

    delta = abs(len(x) - len(y))
    if len(x) < len(y):
        x = ['0'] * (delta + 1) + x
        y = ['0'] + y
    else:
        x = ['0'] + x
        y = ['0'] * (delta + 1) + y

    bases = [2 ** i for i in range(len(x))][::-1]
    # print(x, y, bases)

    cur = 0
    fix = 0
    failed = False

    if reversed:
        x = x[::-1]
        y = y[::-1]
        bases = bases[::-1]
    for a, b, base in zip(x, y, bases):
        # print(a, b, base)
        if a == b == '1':
            fix = 1
            if reversed:
                cur_ = base
        else:
            if fix == 1:
                if a == b == '0':
                    if reversed:
                        cur_ += base
                    else:
                        failed = True
                        fix = 0
                        cur_ = 0
                else:
                    if reversed:
                        cur += cur_
                        cur_ = 0
                        fix = 0
                    else:
                        cur += base
                        fix = 0

    if fix == 1:
        failed = True

    # print(cur, failed)

    return cur, failed

def solve():
    x, y = in_ints()

    if x == y:
        print(-1)
        return

    # if x == 1198372:
    #     cur, failed = update(x, y)
    #     return

    res = 0
    for i in range(100000000):
        res_step = 0
        cur, failed = update(x, y)
        res += cur
        x += cur
        y += cur
        res_step += cur

        cur, failed = update(x, y, reversed=True)
        res += cur
        x += cur
        y += cur
        res_step += cur

        if check(x, y):
            print(res)
            return
        if res_step == 0:
            # print('stopping')
            break

    print(-1)



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

    from utils.utils import check_results
    sys.stdout = sys.__stdout__
    print(check_results())
