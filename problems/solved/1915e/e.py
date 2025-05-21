import sys

import os
from io import BytesIO, IOBase

import random
from math import gcd, lcm, floor, ceil, sqrt, isqrt, log, exp, factorial, perm
from collections import defaultdict, Counter, deque
from bisect import bisect_left, bisect_right, insort_left, insort_right


############################################################
# Utils for fast I/O.
############################################################
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


############################################################
# String manipulation
############################################################
def lc_subseq(s1, s2):
    """
    Find the longest common subsequence between s1 and s2.
    Elements of the subsequence don't need to be contiguous in the original strings! Complexity is O(n1 * n2).
    """
    n1, n2 = len(s1) + 1, len(s2) + 1
    maximum = 0
    # f(i, j) = length of longest string starting at position i for s1 and j for s2. we are looking for f(0, 0)
    # if s1[i-1] == s2[j-1]:
    #     f(i-1, j-1) = f(i, j) + 1
    # else:
    #     f(i-1, j-1) = max { f(i, j-1) , f(i-1, j) }
    f = [[0] * n2 for _ in range(n1)]
    for i in range(n1 - 1, 0, -1):
        for j in range(n2 - 1, 0, -1):
            if s1[i - 1] == s2[j - 1]:
                f[i - 1][j - 1] = f[i][j] + 1
            else:
                f[i - 1][j - 1] = max( f[i][j - 1], f[i - 1][j] )
            if f[i - 1][j - 1] > maximum:
                maximum = f[i - 1][j - 1]
    substring = ''
    if maximum > 0:
        j = 0
        for i in range(n1):
            if f[i][j] == maximum and (i == n1 - 1 or f[i + 1][j] != maximum):
                substring += s1[i]
                j += 1
                maximum -= 1
                if maximum == 0:
                    break
    return substring

def lc_substr(s1, s2):
    """
    Find the longest common substring between s1 and s2.
    Elements of the subsequence have to be contiguous in the original strings! Complexity is O(n1 * n2).
    """
    n1, n2 = len(s1) + 1, len(s2) + 1
    index, maximum = None, 0
    # f(i, j) = longest string ending at position i for s1 and j for s2
    # we are looking for max{f(i, j)} with 0 <= i < n1 and 0 <= j < n2
    # f(i+1, j+1) = f(i, j) + 1 if s1[i+1] == s2[j+1] else 0
    f = [[0] * n2 for _ in range(n1)]
    for i in range(1, n1):
        for j in range(1, n2):
            if s1[i - 1] == s2[j - 1]:
                f[i][j] = f[i - 1][j - 1] + 1
                if f[i][j] > maximum:
                    maximum = f[i][j]
                    index = i - 1
            else:
                f[i][j] = 0
    if index != None:
        substring = s1[index - maximum + 1: index + 1]
    else:
        substring = ''
    return substring


############################################################
# Array manipulation
############################################################
def max_sum_subarray(l):
    """ Finds the maximal sum for a contiguous subarray using Kadane 1D algorithm. Complexity is O(n). """
    max_so_far = l[0]
    curr_max = l[0]
    for i in range(1, len(l)):
        curr_max = max(l[i], curr_max + l[i])
        max_so_far = max(max_so_far, curr_max)
    return max_so_far


############################################################
# Primes and divisors.
############################################################
def is_prime(n):
    """ Check if a number is prime with the trial division method. Complexity is O(sqrt(n)). """
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6
    return True

def prime_factors(n):
    """ Find all prime factors of n. Complexity is O(sqrt(n)). """
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
    """ Find list of primes until n. Complexity is O(n). """
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
    """ Find all divisors of n. Complexity is O(sqrt(n)). """
    divisors = []
    for i in range(1, int(number**0.5) + 1):
        if number % i == 0:
            divisors.append(i)
            if i != number // i:
                divisors.append(number // i)
    return divisors


############################################################
# Integer-Bit manipulation
############################################################
def to_int(x):
    """ Converts bit string to its int representation. """
    return int(x, 2)

def to_bit(x, pad=False, pad_to=30):
    """ Converts int to its bit string representation. Optionally left-pad to a given string length. """
    x = bin(x)[2:]
    if pad:
        # pad '1010' to '00000...0001010'
        pad_len = pad_to - len(x)
        padding = '0' * pad_len
        x = padding + x
    return x


############################################################
# Query template for interactive problems
############################################################
def query(q):
    print(q, flush=True)
    ans = in_string()  # TODO update this accordingly!
    return ans


############################################################
# Input parsing
############################################################
def in_int():
    return int(input())


def in_ints():
    return map(int, input().split())


def in_int_list():
    return list(map(int, input().split()))


def in_string():
    return input()


def in_string_list():
    s = in_string()
    return list(s[:len(s)])


############################################################
# Write your solution here!
############################################################
def solve():
    n = in_int()
    a = in_int_list()

    b = [0]

    for i, x in enumerate(a):
        if i % 2 == 1:
            x = -x
        b += [b[-1] + x]

    del a
    b.sort()

    for i in range(len(b) - 1):
        if b[i + 1] == b[i]:
            print('YES')
            return
    print('NO')

    # cur = 0
    # seen = {0}
    #
    # # print(a)
    # for i, x in enumerate(a):
    #     if i % 2 == 1:
    #         x = -x
    #     # print(cur, x, seen)
    #     cur += x
    #     if cur in seen:
    #         print('YES')
    #         return
    #     seen.add(cur)
    # print('NO')


def solve_n():
    """ Wrapper for problems with multiple test cases. """
    testcases = int(input())  # multiple testcases
    for _ in range(testcases):
        solve()


if __name__ == "__main__":
    if os.path.exists('input.txt'):
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")

    # solve()
    solve_n()

    # For local testing. Comment out before submission!
    # from utils.utils import check_results
    # sys.stdout = sys.__stdout__
    # print(check_results())
