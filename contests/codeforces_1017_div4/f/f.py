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


def build_block(n, m):
    block = []
    k = 1
    for i in range(n):
        row = []
        for j in range(m):
            row += [k]
            k += 1
        block.append(row)
    return block


def build_block_alt(n, m):
    block = []
    k = 2
    for i in range(n):
        row = []
        for j in range(m):
            row += [k]
            k += 1
        block.append(row)
    block[-1][-1] = 1

    return block





import math

def solve():
    n, m, k = in_ints()
    nb = math.gcd(n, k)
    mb = k // nb

    block = build_block(nb, mb)

    block_alt_n = block
    if nb == 1:
        block_alt_n = build_block_alt(nb, mb)

    block_alt_m = block
    if mb == 1:
        block_alt_m = build_block_alt(nb, mb)

    block_alt_nm = block
    if mb == 1 or nb == 1:
        block_alt_nm = build_block_alt(nb, mb)


    res = []
    for i in range(n):
        row = []
        for j in range(m):
            n_div = i // nb
            n_rem = i % nb

            m_div = j // mb
            m_rem = j % mb

            if n_div % 2 == 0:
                # use block
                if m_div % 2 == 0:
                    # use block
                    row += [block[n_rem][m_rem]]
                else:
                    # use block alt m
                    row += [block_alt_m[n_rem][m_rem]]
            else:
                # use block alt n
                if m_div % 2 == 0:
                    # use block alt n
                    row += [block_alt_n[n_rem][m_rem]]
                else:
                    # use block alt nm
                    row += [block_alt_nm[n_rem][m_rem]]
        res += [row]
        print(*row)

    # print(nb, mb)
    # print(block)
    # print(block_alt_n)
    # print(block_alt_m)


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
