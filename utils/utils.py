
def check_results():
    with (
        open("solution.txt") as f1,
        open("output.txt") as f2,
    ):
        a = f1.readlines()
        b = f2.readlines()
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x != y:
            return False
    return True
