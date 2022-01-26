# hanoi algorithms
def move(src, to, res):
    res.append((src, to))


def hanoi(src, to, via, n, res):
    """
    Returns the list of moves necessary to move the tower of size n from 'src' pole to 'to' pole using 'via' pole
    """
    if n == 1:
        move(src, to, res)
    else:
        hanoi(src, via, to, n - 1, res)
        move(src, to, res)
        hanoi(via, to, src, n - 1, res)


def _hanoi(src, to, via, n, res):
    if n <= 0:
        return True
    if n == 1:
        move(src, to, res)
    else:
        hanoi(src, via, to, n - 1, res)
        move(src, to, res)
        hanoi(via, to, src, n - 1, res)
    return False


def bicolor_hanoi(src, to, via, n, res):
    """
    Returns the list of moves necessary to split the n discs from 'src' pole
    among the 'via' and 'to' separating discs by color (whether discs index is odd or even)
    """
    assert n % 2 == 0, "Invalid argument. n must be even"
    if _hanoi(src, via, to, n - 1, res):
        return  # move all to the left
    move(src, to, res)  # move the biggest disc
    if _hanoi(via, src, to, n - 3, res):
        return
    move(via, to, res)
    if _hanoi(src, to, via, n - 4, res):
        move(src, via, res)
        return
    move(src, via, res)
    if _hanoi(to, src, via, n - 6, res):
        move(to, via, res)
        return
    move(to, via, res)
    bicolor_hanoi(src, to, via, n - 6, res)


if __name__ == '__main__':
    res = []
    bicolor_hanoi('A', 'B', 'C', 4, res)
    print(res)
