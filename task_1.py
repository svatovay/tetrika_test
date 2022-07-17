def task(array):
    if type(array) is list:
        for i, value in enumerate(array):
            if value == 0 or value == '0':
                return i
    elif type(array) is str:
        return array.index("0")


test_x = "111111111111111111111111100000000"
test_y = "111111111110000000000000000"

tests = (test_x, [int(_) for _ in test_x], list(test_x), test_y, [int(_) for _ in test_y], list(test_y))

if __name__ == '__main__':
    for test in tests:
        test_answer = task(test)
        print(task(test))
