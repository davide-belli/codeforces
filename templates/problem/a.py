import sys

import os
from io import BytesIO, IOBase

from math import gcd, floor, sqrt, log, ceil
from collections import defaultdict, Counter, deque
from bisect import bisect_left, bisect_right, insort_left, insort_right

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

def prime_factors(n):
    i = 2
    primfac = []
    while i * i <= n:
        while n % i == 0:
            primfac.append(i)
            n = n / i
        i = i + 1
    if n > 1:
        primfac.append(int(n))
    return primfac

def prime_sieve(n):
    is_prime = [True for _ in range(n + 1)]
    is_prime[0] = is_prime[1] = False
    i = 2
    while i * i <= n:
        if is_prime[i]:
            j = i * i
            while j <= n:
                is_prime[j] = False
                j += i
        i += 1
    return is_prime

def find_divisors(number):
    divisors = []
    for i in range(1, int(number**0.5) + 1):
        if number % i == 0:
            divisors.append(i)
            if i != number // i:
                divisors.append(number // i)
    return divisors


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
    pass


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
