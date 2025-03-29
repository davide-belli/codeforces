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
    s = in_string_list()

    if len(set(s)) == 1:
        print(-1)
        return

    res = []
    c = {'T': 0, 'L': 0, 'I': 0}
    for x in s:
        c[x] += 1

    min_ = n
    min_letter = None
    for k, v in c.items():
        if v <= min_:
            min_letter = k
            min_ = v

    point = 0
    for i in range(1, n):
        if s[i] != s[i-1]:
            point = i
            second = s[i]
            third = s[i-1]
            first = list({'T', 'L', 'I'}.difference({second, third}))[0]
            if min_letter != third:
                break

    # print(first, second, third, 'point, n, max', point, n, max(c[first], c[second]))
    # print(s)
    m = n - (max(c[first], c[second]))
    for i in range(2 * m):
        res += [point]
        cur = first if i % 2 == 0 else second
        s = s[:point] + [cur] + s[point:]
        c[cur] += 1
        # print(s)

    min_is_first = first == min_letter
    # print(first, second, third, 'point, n, max', point, n, max(c[first], c[second]))
    m = n - (max(c[min_letter], c[third]))
    point += 1
    for i in range(2 * m):
        res += [point]
        cur = third if i % 2 == 0 else min_letter
        s = s[:point] + [cur] + s[point:]
        if not min_is_first:
            point += 1
        c[cur] += 1
        # print(s)

    for k, v in c.items():
        if v != n:
            for i in range(1, len(s)):
                if len({s[i], s[i-1], k}) == 3:
                    res += [i]
                    s = s[:i] + [k] + s[i:]
                    c[k] += 1
                    # print(s)
                    break

    for k, v in c.items():
        if v != n:
            for i in range(1, len(s)):
                if len({s[i], s[i-1], k}) == 3:
                    res += [i]
                    s = s[:i] + [k] + s[i:]
                    c[k] += 1
                    # print(s)
                    break

    # print(c)
    # print(len(res), n * 2)
    print(len(res))
    print('\n'.join([str(x) for x in res]))









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
