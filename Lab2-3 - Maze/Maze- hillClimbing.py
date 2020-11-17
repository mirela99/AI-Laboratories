
def check_final_state(x, y, xd, yd, labirint):
    if (x == xd and y == yd and labirint[x][y] >= 0):
        return True
    else:
        return False


def check_transition(x, y, labirint, n, m):
    if (x >= 0 and y >= 0 and x < n and y < m and labirint[x][y] == 0):
        return True
    else:
        return False


def HillClimbing(StartLinie, StartColoana, FinalLinie, FinalColoana, matrix, n, m):
    l = StartLinie
    c = StartColoana
    queue1 = []
    queue2 = []
    queue1.append(l)
    queue2.append(c)
    dl = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    while check_final_state(l, c, FinalLinie, FinalColoana, matrix) == 0:
        nextState = False
        for i in range(0, 4):
            lv = l + dl[i]
            cv = c + dc[i]
            if isBetter(lv, cv, l, c, FinalLinie, FinalColoana) and check_transition(lv, cv, matrix, n, m):
                queue1.append(lv)
                queue2.append(cv)
                print(lv)
                nextState = True
                l = lv
                c = cv
                break
        if nextState == True:
            continue
        return (queue1, queue2)
    return (queue1, queue2)


def isBetter(l1, c1, l2, c2, FinalLinie, FinalColoana):
    value1 = getValue(l1, c1, FinalLinie, FinalColoana)
    value2 = getValue(l2, c2, FinalLinie, FinalColoana)
    if value1 == value2:
        return l1 > l2
    return l1 < l2


def getValue(l, c, FinalLinie, FinalColoana):
    return abs(FinalLinie - l) + abs(FinalColoana - c)


if __name__ == '_main_':
    n = 10
    m = 14
    matrix = [
        [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
        [0, 0, 1, 0, 0, 1, 1, 0, 0, 1] 
        ]
    FinalLinie = 7
    FinalColoana = 5
    StartLinie = 0
    StartColoana = 4
    (lines,cols)= HillClimbing(StartLinie, StartColoana, FinalLinie, FinalColoana, matrix, n, m)
    

    for i, j in zip(lines, cols):
        print('(' + str(i) + ', ' + str(j) + ')')