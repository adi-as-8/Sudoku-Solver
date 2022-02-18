import itertools


data = []
potentials = []

def main():
    GetInput()
    CreatePotentials()
    evaluates = 0
    tries = 10
    while not Solved():
        if not Valid():
            print("Invalid Sudoku")
            return

        Evaluate()
        evaluates += 1
        if evaluates >= tries:
            break

    if not Solved():
        BruteForce()
    if not Solved():
        print("Invalid Sudoku")
        return

    PrintData()
    print(f"Difficulty rating: {evaluates}")


def GetInput():
    print("Enter the sudoku one row at a time. Replace unknown characters with empty space")
    for i in range(1, 10):
        while True:
            row = input(f"Enter row {i}: ")

            rowvalid = True
            for j in row:
                if j != " " and not j.isnumeric():
                    rowvalid = False
            if len(row) != 9:
                rowvalid = False

            if rowvalid:
                break
            print("Row invalid. Enter the row again.")
        
        newrow = []
        for j in row:
            if j == " ":
                newrow.append(j)
            else:
                newrow.append(int(j))
        data.append(newrow)


def CreatePotentials():
    for i in range(9):
        row = []
        for j in range(9):
            cell = []
            for k in range(1, 10):
                cell.append(k)
            row.append(cell)
        potentials.append(row)


def Solved():
    for row in data:
        for i in row:
            if i == " ":
                return False
    return True


def Evaluate():
    RemovePotentials()
    EvaluateRows()
    RemovePotentials()
    EvaluateColumns()
    RemovePotentials()
    EvaluateBoxes()
    RemovePotentials()

    RemoveFromBoxes()
    RemoveFromTwoBoxes()
    DupletRows()
    DupletColumns()
    DupletBoxes()
    TripletRows()
    TripletColumns()
    TripletBoxes()
    QuadrupletRows()
    QuadrupletColumns()
    QuadrupletBoxes()
    QuintupletRows()
    QuintupletColumns()
    QuintupletBoxes()
    SextupletRows()
    SextupletColumns()
    SextupletBoxes()
    SeptupletRows()
    SeptupletColumns()
    SeptupletBoxes()
    OctupletRows()
    OctupletColumns()
    OctupletBoxes()
    SwordFish()
    UpdateData()


def RemovePotentials():
    for i in range(9):
        for j in range(9):
            if data[i][j] != " ":
                potentials[i][j] = [data[i][j]]

                for k in range(9):
                    if k != i:
                        if data[i][j] in potentials[k][j]:
                            potentials[k][j].remove(data[i][j])
                    if k != j:
                        if data[i][j] in potentials[i][k]:
                            potentials[i][k].remove(data[i][j])

                for row, column in GetBox(i, j):
                    if (row, column) != (i, j):
                        if data[i][j] in potentials[row][column]:
                            potentials[row][column].remove(data[i][j])


def GetBox(row, column):
    if row in range(3):
        rows = range(3)
    elif row in range(3, 6):
        rows = range(3, 6)
    else:
        rows = range(6, 9)

    if column in range(3):
        columns = range(3)
    elif column in range(3, 6):
        columns = range(3, 6)
    else:
        columns = range(6, 9)

    cells = []
    for i in rows:
        for j in columns:
            cells.append([i, j])
    return cells


def EvaluateRows():
    for i in range(1, 10):
        for j in range(9):
            possibilities = []
            for k in range(9):
                if i in potentials[j][k]:
                    possibilities.append(k)
            if len(possibilities) == 1:
                data[j][possibilities[0]] = i


def EvaluateColumns():
    for i in range(1, 10):
        for j in range(9):
            possibilities = []
            for k in range(9):
                if i in potentials[k][j]:
                    possibilities.append(k)
            if len(possibilities) == 1:
                data[possibilities[0]][j] = i


def EvaluateBoxes():
    for i in range(1, 10):
        for row in (2, 5, 8):
            for column in (2, 5, 8):
                possibilities = []
                for j, k in GetBox(row, column):
                    if i in potentials[j][k]:
                        possibilities.append([j, k])
                if len(possibilities) == 1:
                    data[possibilities[0][0]][possibilities[0][1]] = i


def UpdateData():
    for i in range(9):
        for j in range(9):
            if len(potentials[i][j]) == 1:
                data[i][j] = potentials[i][j][0]


def PrintData():
    for i in range(9):
        row = data[i]
        text = ""
        for j in range(9):
            text += str(row[j])
            if j in (2, 5):
                text += "|"
        print(text)
        if i in (2, 5):
            print("---*---*---")


def DupletRows():
    for i in range(9):
        for j in range(9):
            if len(potentials[i][j]) == 2:
                for k in range(j + 1, 9):
                    if set(potentials[i][k]) == set(potentials[i][j]):
                        for l in range(9):
                            if l not in (j, k):
                                if potentials[i][j][0] in potentials[i][l]:
                                    potentials[i][l].remove(potentials[i][j][0])
                                if potentials[i][j][1] in potentials[i][l]:
                                    potentials[i][l].remove(potentials[i][j][1])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[i][j]:
                    possibilities1.append(j)
            if len(possibilities1) == 2:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[i][j]:
                            possibilities2.append(j)
                    if set(possibilities1) == set(possibilities2):
                        for j in range(1, 10):
                            if j not in (num1, num2):
                                if j in potentials[i][possibilities1[0]]:
                                    potentials[i][possibilities1[0]].remove(j)
                                if j in potentials[i][possibilities1[1]]:
                                    potentials[i][possibilities1[1]].remove(j)


def DupletColumns():
    for i in range(9):
        for j in range(9):
            if len(potentials[j][i]) == 2:
                for k in range(j + 1, 9):
                    if set(potentials[k][i]) == set(potentials[j][i]):
                        for l in range(9):
                            if l not in (j, k):
                                if potentials[j][i][0] in potentials[l][i]:
                                    potentials[l][i].remove(potentials[j][i][0])
                                if potentials[j][i][1] in potentials[l][i]:
                                    potentials[l][i].remove(potentials[j][i][1])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[j][i]:
                    possibilities1.append(j)
            if len(possibilities1) == 2:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[j][i]:
                            possibilities2.append(j)
                    if set(possibilities1) == set(possibilities2):
                        for j in range(1, 10):
                            if j not in (num1, num2):
                                if j in potentials[possibilities1[0]][i]:
                                    potentials[possibilities1[0]][i].remove(j)
                                if j in potentials[possibilities1[1]][i]:
                                    potentials[possibilities1[1]][i].remove(j)


def DupletBoxes():
    for row in (2, 5, 8):
        for column in (2, 5, 8):
            for i, j in GetBox(row, column):
                if len(potentials[i][j]) == 2:
                    for k, l in GetBox(row, column):
                        if (k, l) != (i, j) and set(potentials[k][l]) == set(potentials[i][j]):
                            for m, n in GetBox(row, column):
                                if (m, n) not in ((i, j), (k, l)):
                                    if potentials[i][j][0] in potentials[m][n]:
                                        potentials[m][n].remove(potentials[i][j][0])
                                    if potentials[i][j][1] in potentials[m][n]:
                                        potentials[m][n].remove(potentials[i][j][1])

            for num1 in range(1, 10):
                possibilities1 = []
                for i, j in GetBox(row, column):
                    if num1 in potentials[i][j]:
                        possibilities1.append((i, j))
                if len(possibilities1) == 2:
                    for num2 in range(num1 + 1, 10):
                        possibilities2 = []
                        for i, j in GetBox(row, column):
                            if num2 in potentials[i][j]:
                                possibilities2.append((i, j))
                        if set(possibilities2) == set(possibilities1):
                            for i in range(1, 10):
                                if i not in (num1, num2):
                                    if i in potentials[possibilities1[0][0]][possibilities1[0][1]]:
                                        potentials[possibilities1[0][0]][possibilities1[0][1]].remove(i)
                                    if i in potentials[possibilities1[1][0]][possibilities1[1][1]]:
                                        potentials[possibilities1[1][0]][possibilities1[1][1]].remove(i)


def RemoveFromBoxes():
    for row in (2, 5, 8):
        for column in (2, 5, 8):
            for i in range(1, 10):
                rows = set()
                columns =  set()
                for j, k in GetBox(row, column):
                    if i in potentials[j][k]:
                        rows.add(j)
                        columns.add(k)
                if len(rows) == 1:
                    x = rows.pop()
                    for j in range(9):
                        if j not in columns and i in potentials[x][j]:
                            potentials[x][j].remove(i)
                elif len(columns) == 1:
                    x = columns.pop()
                    for j in range(9):
                        if j not in rows and i in potentials[j][x]:
                            potentials[j][x].remove(i)


def TripletRows():
    for i in range(9):
        for j in range(9):
            if len(potentials[i][j]) == 3:
                for k in range(j + 1, 9):
                    if set(potentials[i][k]) == set(potentials[i][j]):
                        for l in range(k + 1, 9):
                            if set(potentials[i][l]) == set(potentials[i][j]):
                                for m in range(9):
                                    if m not in (j, k, l):
                                        if potentials[i][j][0] in potentials[i][m]:
                                            potentials[i][m].remove(potentials[i][j][0])
                                        if potentials[i][j][1] in potentials[i][m]:
                                            potentials[i][m].remove(potentials[i][j][1])
                                        if potentials[i][j][2] in potentials[i][m]:
                                            potentials[i][m].remove(potentials[i][j][2])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[i][j]:
                    possibilities1.append(j)
            if len(possibilities1) == 3:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[i][j]:
                            possibilities2.append(j)
                    if set(possibilities1) == set(possibilities2):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[i][j]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for j in range(1, 10):
                                    if j not in (num1, num2, num3):
                                        if j in potentials[i][possibilities1[0]]:
                                            potentials[i][possibilities1[0]].remove(j)
                                        if j in potentials[i][possibilities1[1]]:
                                            potentials[i][possibilities1[1]].remove(j)
                                        if j in potentials[i][possibilities1[2]]:
                                            potentials[i][possibilities1[2]].remove(j)


def TripletColumns():
    for i in range(9):
        for j in range(9):
            if len(potentials[j][i]) == 3:
                for k in range(j + 1, 9):
                    if set(potentials[k][i]) == set(potentials[j][i]):
                        for l in range(k + 1, 9):
                            if set(potentials[l][i]) == set(potentials[j][i]):
                                for m in range(9):
                                    if m not in (j, k, l):
                                        if potentials[j][i][0] in potentials[m][i]:
                                            potentials[m][i].remove(potentials[j][i][0])
                                        if potentials[j][i][1] in potentials[m][i]:
                                            potentials[m][i].remove(potentials[j][i][1])
                                        if potentials[j][i][2] in potentials[m][i]:
                                            potentials[m][i].remove(potentials[j][i][2])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[j][i]:
                    possibilities1.append(j)
            if len(possibilities1) == 3:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[j][i]:
                            possibilities2.append(j)
                    if set(possibilities1) == set(possibilities2):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[j][i]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for j in range(1, 10):
                                    if j not in (num1, num2, num3):
                                        if j in potentials[possibilities1[0]][i]:
                                            potentials[possibilities1[0]][i].remove(j)
                                        if j in potentials[possibilities1[1]][i]:
                                            potentials[possibilities1[1]][i].remove(j)
                                        if j in potentials[possibilities1[2]][i]:
                                            potentials[possibilities1[2]][i].remove(j)


def TripletBoxes():
    for row in (2, 5, 8):
        for column in (2, 5, 8):
            for i, j in GetBox(row, column):
                if len(potentials[i][j]) == 3:
                    for k, l in GetBox(row, column):
                        if (k, l) != (i, j) and set(potentials[k][l]) == set(potentials[i][j]):
                            for m, n in GetBox(row, column):
                                if (m, n) not in ((i, j), (k, l)) and set(potentials[m][n]) == set(potentials[i][j]):
                                    for o, p in GetBox(row, column):
                                        if (o, p) not in ((i, j), (k, l), (m, n)):
                                            if potentials[i][j][0] in potentials[o][p]:
                                                potentials[o][p].remove(potentials[i][j][0])
                                            if potentials[i][j][1] in potentials[o][p]:
                                                potentials[o][p].remove(potentials[i][j][1])
                                            if potentials[i][j][2] in potentials[o][p]:
                                                potentials[o][p].remove(potentials[i][j][2])

            for num1 in range(1, 10):
                possibilities1 = []
                for i, j in GetBox(row, column):
                    if num1 in potentials[i][j]:
                        possibilities1.append((i, j))
                if len(possibilities1) == 3:
                    for num2 in range(num1 + 1, 10):
                        possibilities2 = []
                        for i, j in GetBox(row, column):
                            if num2 in potentials[i][j]:
                                possibilities2.append((i, j))
                        if set(possibilities2) == set(possibilities1):
                            for num3 in range(num2 + 1, 10):
                                possibilities3 = []
                                for i, j in GetBox(row, column):
                                    if num3 in potentials[i][j]:
                                        possibilities3.append((i, j))
                                if set(possibilities3) == set(possibilities1):
                                    for i in range(1, 10):
                                        if i not in (num1, num2, num3):
                                            if i in potentials[possibilities1[0][0]][possibilities1[0][1]]:
                                                potentials[possibilities1[0][0]][possibilities1[0][1]].remove(i)
                                            if i in potentials[possibilities1[1][0]][possibilities1[1][1]]:
                                                potentials[possibilities1[1][0]][possibilities1[1][1]].remove(i)
                                            if i in potentials[possibilities1[2][0]][possibilities1[2][1]]:
                                                potentials[possibilities1[2][0]][possibilities1[2][1]].remove(i)


def Valid():
    for i in range(1, 10):
        for row in data:
            occurances = 0
            for num in row:
                if num == i:
                    occurances += 1
            if occurances > 1:
                return False

        for column in range(9):
            occurances = 0
            for row in data:
                if row[column] == i:
                    occurances += 1
            if occurances > 1:
                return False

        for row in (2, 5, 8):
            for column in (2, 5, 8):
                occurances = 0
                for j, k in GetBox(row, column):
                    if data[j][k] == i:
                        occurances += 1
                if occurances > 1:
                    return False
    return True


def BruteForce():
    unknowns = []
    for i in range(9):
        for j in range(9):
            if data[i][j] == " ":
                unknowns.append((i, j))
    unknown = len(unknowns)
    index = 0

    while True:
        if index < 0 or index >= unknown:
            break
        if data[unknowns[index][0]][unknowns[index][1]] == " ":
            data[unknowns[index][0]][unknowns[index][1]] = 0
        elif data[unknowns[index][0]][unknowns[index][1]] == 9:
            data[unknowns[index][0]][unknowns[index][1]] = " "
            index -= 1
            continue

        data[unknowns[index][0]][unknowns[index][1]] += 1
        if Valid():
            index += 1


def QuadrupletRows():
    for i in range(9):
        for j in range(9):
            if len(potentials[i][j]) == 4:
                for k in range(j + 1, 9):
                    if set(potentials[i][k]) == set(potentials[i][j]):
                        for l in range(k + 1, 9):
                            if set(potentials[i][l]) == set(potentials[i][j]):
                                for m in range(l + 1, 9):
                                    if set(potentials[i][m]) == set(potentials[i][j]):
                                        for n in range(9):
                                            if n not in (j, k, l, m):
                                                if potentials[i][j][0] in potentials[i][n]:
                                                    potentials[i][n].remove(potentials[i][j][0])
                                                if potentials[i][j][1] in potentials[i][n]:
                                                    potentials[i][n].remove(potentials[i][j][1])
                                                if potentials[i][j][2] in potentials[i][n]:
                                                    potentials[i][n].remove(potentials[i][j][2])
                                                if potentials[i][j][3] in potentials[i][n]:
                                                    potentials[i][n].remove(potentials[i][j][3])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[i][j]:
                    possibilities1.append(j)
            if len(possibilities1) == 4:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[i][j]:
                            possibilities2.append(j)
                    if set(possibilities2) == set(possibilities1):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[i][j]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for num4 in range(num3 + 1, 10):
                                    possibilities4 = []
                                    for j in range(9):
                                        if num4 in potentials[i][j]:
                                            possibilities4.append(j)
                                    if set(possibilities4) == set(possibilities1):
                                        for j in range(1, 10):
                                            if j not in (num1, num2, num3, num4):
                                                if j in potentials[i][possibilities1[0]]:
                                                    potentials[i][possibilities1[0]].remove(j)
                                                if j in potentials[i][possibilities1[1]]:
                                                    potentials[i][possibilities1[1]].remove(j)
                                                if j in potentials[i][possibilities1[2]]:
                                                    potentials[i][possibilities1[2]].remove(j)
                                                if j in potentials[i][possibilities1[3]]:
                                                    potentials[i][possibilities1[3]].remove(j)


def QuadrupletColumns():
    for i in range(9):
        for j in range(9):
            if len(potentials[j][i]) == 4:
                for k in range(j + 1, 9):
                    if set(potentials[k][i]) == set(potentials[j][i]):
                        for l in range(k + 1, 9):
                            if set(potentials[l][i]) == set(potentials[j][i]):
                                for m in range(l + 1, 9):
                                    if set(potentials[m][i]) == set(potentials[j][i]):
                                        for n in range(9):
                                            if n not in (j, k, l, m):
                                                if potentials[j][i][0] in potentials[n][i]:
                                                    potentials[n][i].remove(potentials[j][i][0])
                                                if potentials[j][i][1] in potentials[n][i]:
                                                    potentials[n][i].remove(potentials[j][i][1])
                                                if potentials[j][i][2] in potentials[n][i]:
                                                    potentials[n][i].remove(potentials[j][i][2])
                                                if potentials[j][i][3] in potentials[n][i]:
                                                    potentials[n][i].remove(potentials[j][i][3])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[j][i]:
                    possibilities1.append(j)
            if len(possibilities1) == 4:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[j][i]:
                            possibilities2.append(j)
                    if set(possibilities2) == set(possibilities1):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[j][i]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for num4 in range(num3 + 1, 10):
                                    possibilities4 = []
                                    for j in range(9):
                                        if num4 in potentials[j][i]:
                                            possibilities4.append(j)
                                    if set(possibilities4) == set(possibilities1):
                                        for j in range(1, 10):
                                            if j not in (num1, num2, num3, num4):
                                                if j in potentials[possibilities1[0]][i]:
                                                    potentials[possibilities1[0]][i].remove(j)
                                                if j in potentials[possibilities1[1]][i]:
                                                    potentials[possibilities1[1]][i].remove(j)
                                                if j in potentials[possibilities1[2]][i]:
                                                    potentials[possibilities1[2]][i].remove(j)
                                                if j in potentials[possibilities1[3]][i]:
                                                    potentials[possibilities1[3]][i].remove(j)


def QuadrupletBoxes():
    for row in (2, 5, 8):
        for column in (2, 5, 8):
            for i, j in GetBox(row, column):
                if len(potentials[i][j]) == 4:
                    for k, l in GetBox(row, column):
                        if (k, l) != (i, j) and set(potentials[k][l]) == set(potentials[i][j]):
                            for m, n in GetBox(row, column):
                                if (m, n) not in ((i, j), (k, l)) and set(potentials[m][n]) == set(potentials[i][j]):
                                    for o, p in GetBox(row, column):
                                        if (o, p) not in ((i, j), (k, l), (m, n)) and set(potentials[o][p]) == set(potentials[i][j]):
                                            for q, r in GetBox(row, column):
                                                if (q, r) not in ((i, j), (k, l), (m, n), (o, p)):
                                                    if potentials[i][j][0] in potentials[q][r]:
                                                        potentials[q][r].remove(potentials[i][j][0])
                                                    if potentials[i][j][1] in potentials[q][r]:
                                                        potentials[q][r].remove(potentials[i][j][1])
                                                    if potentials[i][j][2] in potentials[q][r]:
                                                        potentials[q][r].remove(potentials[i][j][2])
                                                    if potentials[i][j][3] in potentials[q][r]:
                                                        potentials[q][r].remove(potentials[i][j][3])

            for num1 in range(1, 10):
                possibilities1 = []
                for i, j in GetBox(row, column):
                    if num1 in potentials[i][j]:
                        possibilities1.append((i, j))
                if len(possibilities1) == 4:
                    for num2 in range(num1 + 1, 10):
                        possibilities2 = []
                        for i, j in GetBox(row, column):
                            if num2 in potentials[i][j]:
                                possibilities2.append((i, j))
                        if set(possibilities2) == set(possibilities1):
                            for num3 in range(num2 + 1, 10):
                                possibilities3 = []
                                for i, j in GetBox(row, column):
                                    if num3 in potentials[i][j]:
                                        possibilities3.append((i, j))
                                if set(possibilities3) == set(possibilities1):
                                    for num4 in range(num3 + 1, 10):
                                        possibilities4 = []
                                        for i, j in GetBox(row, column):
                                            if num4 in potentials[i][j]:
                                                possibilities4.append((i, j))
                                        if set(possibilities4) == set(possibilities1):
                                            for i in range(1, 10):
                                                if i not in (num1, num2, num3, num4):
                                                    if i in potentials[possibilities1[0][0]][possibilities1[0][1]]:
                                                        potentials[possibilities1[0][0]][possibilities1[0][1]].remove(i)
                                                    if i in potentials[possibilities1[1][0]][possibilities1[1][1]]:
                                                        potentials[possibilities1[1][0]][possibilities1[1][1]].remove(i)
                                                    if i in potentials[possibilities1[2][0]][possibilities1[2][1]]:
                                                        potentials[possibilities1[2][0]][possibilities1[2][1]].remove(i)
                                                    if i in potentials[possibilities1[3][0]][possibilities1[3][1]]:
                                                        potentials[possibilities1[3][0]][possibilities1[3][1]].remove(i)


def QuintupletRows():
    for i in range(9):
        for j in range(9):
            if len(potentials[i][j]) == 5:
                for k in range(j + 1, 9):
                    if set(potentials[i][k]) == set(potentials[i][j]):
                        for l in range(k + 1, 9):
                            if set(potentials[i][l]) == set(potentials[i][j]):
                                for m in range(l + 1, 9):
                                    if set(potentials[i][m]) == set(potentials[i][j]):
                                        for n in range(m + 1, 9):
                                            if set(potentials[i][n]) == set(potentials[i][j]):
                                                for o in range(9):
                                                    if o not in (j, k, l, m, n):
                                                        if potentials[i][j][0] in potentials[i][o]:
                                                            potentials[i][o].remove(potentials[i][j][0])
                                                        if potentials[i][j][1] in potentials[i][o]:
                                                            potentials[i][o].remove(potentials[i][j][1])
                                                        if potentials[i][j][2] in potentials[i][o]:
                                                            potentials[i][o].remove(potentials[i][j][2])
                                                        if potentials[i][j][3] in potentials[i][o]:
                                                            potentials[i][o].remove(potentials[i][j][3])
                                                        if potentials[i][j][4] in potentials[i][o]:
                                                            potentials[i][o].remove(potentials[i][j][4])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[i][j]:
                    possibilities1.append(j)
            if len(possibilities1) == 5:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[i][j]:
                            possibilities2.append(j)
                    if set(possibilities2) == set(possibilities1):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[i][j]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for num4 in range(num3 + 1, 10):
                                    possibilities4 = []
                                    for j in range(9):
                                        if num4 in potentials[i][j]:
                                            possibilities4.append(j)
                                    if set(possibilities4) == set(possibilities1):
                                        for num5 in range(num4 + 1, 10):
                                            possibilities5 = []
                                            for j in range(9):
                                                if num5 in potentials[i][j]:
                                                    possibilities5.append(j)
                                            if set(possibilities5) == set(possibilities1):
                                                for j in range(1, 10):
                                                    if j not in (num1, num2, num3, num4, num5):
                                                        if j in potentials[i][possibilities1[0]]:
                                                            potentials[i][possibilities1[0]].remove(j)
                                                        if j in potentials[i][possibilities1[1]]:
                                                            potentials[i][possibilities1[1]].remove(j)
                                                        if j in potentials[i][possibilities1[2]]:
                                                            potentials[i][possibilities1[2]].remove(j)
                                                        if j in potentials[i][possibilities1[3]]:
                                                            potentials[i][possibilities1[3]].remove(j)
                                                        if j in potentials[i][possibilities1[4]]:
                                                            potentials[i][possibilities1[4]].remove(j)


def QuintupletColumns():
    for i in range(9):
        for j in range(9):
            if len(potentials[j][i]) == 5:
                for k in range(j + 1, 9):
                    if set(potentials[k][i]) == set(potentials[j][i]):
                        for l in range(k + 1, 9):
                            if set(potentials[l][i]) == set(potentials[j][i]):
                                for m in range(l + 1, 9):
                                    if set(potentials[m][i]) == set(potentials[j][i]):
                                        for n in range(m + 1, 9):
                                            if set(potentials[n][i]) == set(potentials[j][i]):
                                                for o in range(9):
                                                    if o not in (j, k, l, m, n):
                                                        if potentials[j][i][0] in potentials[o][i]:
                                                            potentials[o][i].remove(potentials[j][i][0])
                                                        if potentials[j][i][1] in potentials[o][i]:
                                                            potentials[o][i].remove(potentials[j][i][1])
                                                        if potentials[j][i][2] in potentials[o][i]:
                                                            potentials[o][i].remove(potentials[j][i][2])
                                                        if potentials[j][i][3] in potentials[o][i]:
                                                            potentials[o][i].remove(potentials[j][i][3])
                                                        if potentials[j][i][4] in potentials[o][i]:
                                                            potentials[o][i].remove(potentials[j][i][4])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[j][i]:
                    possibilities1.append(j)
            if len(possibilities1) == 5:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[j][i]:
                            possibilities2.append(j)
                    if set(possibilities2) == set(possibilities1):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[j][i]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for num4 in range(num3 + 1, 10):
                                    possibilities4 = []
                                    for j in range(9):
                                        if num4 in potentials[j][i]:
                                            possibilities4.append(j)
                                    if set(possibilities4) == set(possibilities1):
                                        for num5 in range(num4 + 1, 10):
                                            possibilities5 = []
                                            for j in range(9):
                                                if num5 in potentials[j][i]:
                                                    possibilities5.append(j)
                                            if set(possibilities5) == set(possibilities1):
                                                for j in range(1, 10):
                                                    if j not in (num1, num2, num3, num4, num5):
                                                        if j in potentials[possibilities1[0]][i]:
                                                            potentials[possibilities1[0]][i].remove(j)
                                                        if j in potentials[possibilities1[1]][i]:
                                                            potentials[possibilities1[1]][i].remove(j)
                                                        if j in potentials[possibilities1[2]][i]:
                                                            potentials[possibilities1[2]][i].remove(j)
                                                        if j in potentials[possibilities1[3]][i]:
                                                            potentials[possibilities1[3]][i].remove(j)
                                                        if j in potentials[possibilities1[4]][i]:
                                                            potentials[possibilities1[4]][i].remove(j)


def QuintupletBoxes():
    for row in (2, 5, 8):
        for column in (2, 5, 8):
            for i, j in GetBox(row, column):
                if len(potentials[i][j]) == 5:
                    for k, l in GetBox(row, column):
                        if (k, l) != (i, j) and set(potentials[k][l]) == set(potentials[i][j]):
                            for m, n in GetBox(row, column):
                                if (m, n) not in ((i, j), (k, l)) and set(potentials[m][n]) == set(potentials[i][j]):
                                    for o, p in GetBox(row, column):
                                        if (o, p) not in ((i, j), (k, l), (m, n)) and set(potentials[o][p]) == set(potentials[i][j]):
                                            for q, r in GetBox(row, column):
                                                if (q, r) not in ((i, j), (k, l), (m, n), (o, p)) and set(potentials[q][r]) == set(potentials[i][j]):
                                                    for s, t in GetBox(row, column):
                                                        if (s, t) not in ((i, j), (k, l), (m, n), (o, p), (q, r)):
                                                            if potentials[i][j][0] in potentials[s][t]:
                                                                potentials[s][t].remove(potentials[i][j][0])
                                                            if potentials[i][j][1] in potentials[s][t]:
                                                                potentials[s][t].remove(potentials[i][j][1])
                                                            if potentials[i][j][2] in potentials[s][t]:
                                                                potentials[s][t].remove(potentials[i][j][2])
                                                            if potentials[i][j][3] in potentials[s][t]:
                                                                potentials[s][t].remove(potentials[i][j][3])
                                                            if potentials[i][j][4] in potentials[s][t]:
                                                                potentials[s][t].remove(potentials[i][j][4])

            for num1 in range(1, 10):
                possibilities1 = []
                for i, j in GetBox(row, column):
                    if num1 in potentials[i][j]:
                        possibilities1.append((i, j))
                if len(possibilities1) == 5:
                    for num2 in range(num1 + 1, 10):
                        possibilities2 = []
                        for i, j in GetBox(row, column):
                            if num2 in potentials[i][j]:
                                possibilities2.append((i, j))
                        if set(possibilities2) == set(possibilities1):
                            for num3 in range(num2 + 1, 10):
                                possibilities3 = []
                                for i, j in GetBox(row, column):
                                    if num3 in potentials[i][j]:
                                        possibilities3.append((i, j))
                                if set(possibilities3) == set(possibilities1):
                                    for num4 in range(num3 + 1, 10):
                                        possibilities4 = []
                                        for i, j in GetBox(row, column):
                                            if num4 in potentials[i][j]:
                                                possibilities4.append((i, j))
                                        if set(possibilities4) == set(possibilities1):
                                            for num5 in range(num4 + 1, 10):
                                                possibilities5 = []
                                                for i, j in GetBox(row, column):
                                                    if num5 in potentials[i][j]:
                                                        possibilities5.append((i, j))
                                                if set(possibilities5) == set(possibilities1):
                                                    for i in range(1, 10):
                                                        if i not in (num1, num2, num3, num4, num5):
                                                            if i in potentials[possibilities1[0][0]][possibilities1[0][1]]:
                                                                potentials[possibilities1[0][0]][possibilities1[0][1]].remove(i)
                                                            if i in potentials[possibilities1[1][0]][possibilities1[1][1]]:
                                                                potentials[possibilities1[1][0]][possibilities1[1][1]].remove(i)
                                                            if i in potentials[possibilities1[2][0]][possibilities1[2][1]]:
                                                                potentials[possibilities1[2][0]][possibilities1[2][1]].remove(i)
                                                            if i in potentials[possibilities1[3][0]][possibilities1[3][1]]:
                                                                potentials[possibilities1[3][0]][possibilities1[3][1]].remove(i)
                                                            if i in potentials[possibilities1[4][0]][possibilities1[4][1]]:
                                                                potentials[possibilities1[4][0]][possibilities1[4][1]].remove(i)


def SextupletRows():
    for i in range(9):
        for j in range(9):
            if len(potentials[i][j]) == 6:
                for k in range(j + 1, 9):
                    if set(potentials[i][k]) == set(potentials[i][j]):
                        for l in range(k + 1, 9):
                            if set(potentials[i][l]) == set(potentials[i][j]):
                                for m in range(l + 1, 9):
                                    if set(potentials[i][m]) == set(potentials[i][j]):
                                        for n in range(m + 1, 9):
                                            if set(potentials[i][n]) == set(potentials[i][j]):
                                                for o in range(n + 1, 9):
                                                    if set(potentials[i][o]) == set(potentials[i][j]):
                                                        for p in range(9):
                                                            if p not in (j, k, l, m, n, o):
                                                                if potentials[i][j][0] in potentials[i][p]:
                                                                    potentials[i][p].remove(potentials[i][j][0])
                                                                if potentials[i][j][1] in potentials[i][p]:
                                                                    potentials[i][p].remove(potentials[i][j][1])
                                                                if potentials[i][j][2] in potentials[i][p]:
                                                                    potentials[i][p].remove(potentials[i][j][2])
                                                                if potentials[i][j][3] in potentials[i][p]:
                                                                    potentials[i][p].remove(potentials[i][j][3])
                                                                if potentials[i][j][4] in potentials[i][p]:
                                                                    potentials[i][p].remove(potentials[i][j][4])
                                                                if potentials[i][j][5] in potentials[i][p]:
                                                                    potentials[i][p].remove(potentials[i][j][5])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[i][j]:
                    possibilities1.append(j)
            if len(possibilities1) == 6:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[i][j]:
                            possibilities2.append(j)
                    if set(possibilities2) == set(possibilities1):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[i][j]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for num4 in range(num3 + 1, 10):
                                    possibilities4 = []
                                    for j in range(9):
                                        if num4 in potentials[i][j]:
                                            possibilities4.append(j)
                                    if set(possibilities4) == set(possibilities1):
                                        for num5 in range(num4 + 1, 10):
                                            possibilities5 = []
                                            for j in range(9):
                                                if num5 in potentials[i][j]:
                                                    possibilities5.append(j)
                                            if set(possibilities5) == set(possibilities1):
                                                for num6 in range(num5 + 1, 10):
                                                    possibilities6 = []
                                                    for j in range(9):
                                                        if num6 in potentials[i][j]:
                                                            possibilities6.append(j)
                                                    if set(possibilities6) == set(possibilities1):
                                                        for j in range(1, 10):
                                                            if j not in (num1, num2, num3, num4, num5, num6):
                                                                if j in potentials[i][possibilities1[0]]:
                                                                    potentials[i][possibilities1[0]].remove(j)
                                                                if j in potentials[i][possibilities1[1]]:
                                                                    potentials[i][possibilities1[1]].remove(j)
                                                                if j in potentials[i][possibilities1[2]]:
                                                                    potentials[i][possibilities1[2]].remove(j)
                                                                if j in potentials[i][possibilities1[3]]:
                                                                    potentials[i][possibilities1[3]].remove(j)
                                                                if j in potentials[i][possibilities1[4]]:
                                                                    potentials[i][possibilities1[4]].remove(j)
                                                                if j in potentials[i][possibilities1[5]]:
                                                                    potentials[i][possibilities1[5]].remove(j)


def SextupletColumns():
    for i in range(9):
        for j in range(9):
            if len(potentials[j][i]) == 6:
                for k in range(j + 1, 9):
                    if set(potentials[k][i]) == set(potentials[j][i]):
                        for l in range(k + 1, 9):
                            if set(potentials[l][i]) == set(potentials[j][i]):
                                for m in range(l + 1, 9):
                                    if set(potentials[m][i]) == set(potentials[j][i]):
                                        for n in range(m + 1, 9):
                                            if set(potentials[n][i]) == set(potentials[j][i]):
                                                for o in range(n + 1, 9):
                                                    if set(potentials[o][i]) == set(potentials[j][i]):
                                                        for p in range(9):
                                                            if p not in (j, k, l, m, n, o):
                                                                if potentials[j][i][0] in potentials[p][i]:
                                                                    potentials[p][i].remove(potentials[j][i][0])
                                                                if potentials[j][i][1] in potentials[p][i]:
                                                                    potentials[p][i].remove(potentials[j][i][1])
                                                                if potentials[j][i][2] in potentials[p][i]:
                                                                    potentials[p][i].remove(potentials[j][i][2])
                                                                if potentials[j][i][3] in potentials[p][i]:
                                                                    potentials[p][i].remove(potentials[j][i][3])
                                                                if potentials[j][i][4] in potentials[p][i]:
                                                                    potentials[p][i].remove(potentials[j][i][4])
                                                                if potentials[j][i][5] in potentials[p][i]:
                                                                    potentials[p][i].remove(potentials[j][i][5])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[j][i]:
                    possibilities1.append(j)
            if len(possibilities1) == 6:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[j][i]:
                            possibilities2.append(j)
                    if set(possibilities2) == set(possibilities1):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[j][i]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for num4 in range(num3 + 1, 10):
                                    possibilities4 = []
                                    for j in range(9):
                                        if num4 in potentials[j][i]:
                                            possibilities4.append(j)
                                    if set(possibilities4) == set(possibilities1):
                                        for num5 in range(num4 + 1, 10):
                                            possibilities5 = []
                                            for j in range(9):
                                                if num5 in potentials[j][i]:
                                                    possibilities5.append(j)
                                            if set(possibilities5) == set(possibilities1):
                                                for num6 in range(num5 + 1, 10):
                                                    possibilities6 = []
                                                    for j in range(9):
                                                        if num6 in potentials[j][i]:
                                                            possibilities6.append(j)
                                                    if set(possibilities6) == set(possibilities1):
                                                        for j in range(1, 10):
                                                            if j not in (num1, num2, num3, num4, num5, num6):
                                                                if j in potentials[possibilities1[0]][i]:
                                                                    potentials[possibilities1[0]][i].remove(j)
                                                                if j in potentials[possibilities1[1]][i]:
                                                                    potentials[possibilities1[1]][i].remove(j)
                                                                if j in potentials[possibilities1[2]][i]:
                                                                    potentials[possibilities1[2]][i].remove(j)
                                                                if j in potentials[possibilities1[3]][i]:
                                                                    potentials[possibilities1[3]][i].remove(j)
                                                                if j in potentials[possibilities1[4]][i]:
                                                                    potentials[possibilities1[4]][i].remove(j)
                                                                if j in potentials[possibilities1[5]][i]:
                                                                    potentials[possibilities1[5]][i].remove(j)


def SextupletBoxes():
    for row in (2, 5, 8):
        for column in (2, 5, 8):
            for i, j in GetBox(row, column):
                if len(potentials[i][j]) == 6:
                    for k, l in GetBox(row, column):
                        if (k, l) != (i, j) and set(potentials[k][l]) == set(potentials[i][j]):
                            for m, n in GetBox(row, column):
                                if (m, n) not in ((i, j), (k, l)) and set(potentials[m][n]) == set(potentials[i][j]):
                                    for o, p in GetBox(row, column):
                                        if (o, p) not in ((i, j), (k, l), (m, n)) and set(potentials[o][p]) == set(potentials[i][j]):
                                            for q, r in GetBox(row, column):
                                                if (q, r) not in ((i, j), (k, l), (m, n), (o, p)) and set(potentials[q][r]) == set(potentials[i][j]):
                                                    for s, t in GetBox(row, column):
                                                        if (s, t) not in ((i, j), (k, l), (m, n), (o, p), (q, r)) and set(potentials[s][t]) == set(potentials[i][j]):
                                                            for u, v in GetBox(row, column):
                                                                if (u, v) not in ((i, j), (k, l), (m, n), (o, p), (q, r), (s, t)):
                                                                    if potentials[i][j][0] in potentials[u][v]:
                                                                        potentials[u][v].remove(potentials[i][j][0])
                                                                    if potentials[i][j][1] in potentials[u][v]:
                                                                        potentials[u][v].remove(potentials[i][j][1])
                                                                    if potentials[i][j][2] in potentials[u][v]:
                                                                        potentials[u][v].remove(potentials[i][j][2])
                                                                    if potentials[i][j][3] in potentials[u][v]:
                                                                        potentials[u][v].remove(potentials[i][j][3])
                                                                    if potentials[i][j][4] in potentials[u][v]:
                                                                        potentials[u][v].remove(potentials[i][j][4])
                                                                    if potentials[i][j][5] in potentials[u][v]:
                                                                        potentials[u][v].remove(potentials[i][j][5])

            for num1 in range(1, 10):
                possibilities1 = []
                for i, j in GetBox(row, column):
                    if num1 in potentials[i][j]:
                        possibilities1.append((i, j))
                if len(possibilities1) == 6:
                    for num2 in range(num1 + 1, 10):
                        possibilities2 = []
                        for i, j in GetBox(row, column):
                            if num2 in potentials[i][j]:
                                possibilities2.append((i, j))
                        if set(possibilities2) == set(possibilities1):
                            for num3 in range(num2 + 1, 10):
                                possibilities3 = []
                                for i, j in GetBox(row, column):
                                    if num3 in potentials[i][j]:
                                        possibilities3.append((i, j))
                                if set(possibilities3) == set(possibilities1):
                                    for num4 in range(num3 + 1, 10):
                                        possibilities4 = []
                                        for i, j in GetBox(row, column):
                                            if num4 in potentials[i][j]:
                                                possibilities4.append((i, j))
                                        if set(possibilities4) == set(possibilities1):
                                            for num5 in range(num4 + 1, 10):
                                                possibilities5 = []
                                                for i, j in GetBox(row, column):
                                                    if num5 in potentials[i][j]:
                                                        possibilities5.append((i, j))
                                                if set(possibilities5) == set(possibilities1):
                                                    for num6 in range(num5 + 1, 10):
                                                        possibilities6 = []
                                                        for i, j in GetBox(row, column):
                                                            if num6 in potentials[i][j]:
                                                                possibilities6.append((i, j))
                                                        if set(possibilities6) == set(possibilities1):
                                                            for i in range(1, 10):
                                                                if i not in (num1, num2, num3, num4, num5, num6):
                                                                    if i in potentials[possibilities1[0][0]][possibilities1[0][1]]:
                                                                        potentials[possibilities1[0][0]][possibilities1[0][1]].remove(i)
                                                                    if i in potentials[possibilities1[1][0]][possibilities1[1][1]]:
                                                                        potentials[possibilities1[1][0]][possibilities1[1][1]].remove(i)
                                                                    if i in potentials[possibilities1[2][0]][possibilities1[2][1]]:
                                                                        potentials[possibilities1[2][0]][possibilities1[2][1]].remove(i)
                                                                    if i in potentials[possibilities1[3][0]][possibilities1[3][1]]:
                                                                        potentials[possibilities1[3][0]][possibilities1[3][1]].remove(i)
                                                                    if i in potentials[possibilities1[4][0]][possibilities1[4][1]]:
                                                                        potentials[possibilities1[4][0]][possibilities1[4][1]].remove(i)
                                                                    if i in potentials[possibilities1[5][0]][possibilities1[5][1]]:
                                                                        potentials[possibilities1[5][0]][possibilities1[5][1]].remove(i)


def SeptupletRows():
    for i in range(9):
        for j in range(9):
            if len(potentials[i][j]) == 7:
                for k in range(j + 1, 9):
                    if set(potentials[i][k]) == set(potentials[i][j]):
                        for l in range(k + 1, 9):
                            if set(potentials[i][l]) == set(potentials[i][j]):
                                for m in range(l + 1, 9):
                                    if set(potentials[i][m]) == set(potentials[i][j]):
                                        for n in range(m + 1, 9):
                                            if set(potentials[i][n]) == set(potentials[i][j]):
                                                for o in range(n + 1, 9):
                                                    if set(potentials[i][o]) == set(potentials[i][j]):
                                                        for p in range(o + 1, 9):
                                                            if set(potentials[i][p]) == set(potentials[i][j]):
                                                                for q in range(9):
                                                                    if q not in (j, k, l, m, n, o, p):
                                                                        if potentials[i][j][0] in potentials[i][q]:
                                                                            potentials[i][q].remove(potentials[i][j][0])
                                                                        if potentials[i][j][1] in potentials[i][q]:
                                                                            potentials[i][q].remove(potentials[i][j][1])
                                                                        if potentials[i][j][2] in potentials[i][q]:
                                                                            potentials[i][q].remove(potentials[i][j][2])
                                                                        if potentials[i][j][3] in potentials[i][q]:
                                                                            potentials[i][q].remove(potentials[i][j][3])
                                                                        if potentials[i][j][4] in potentials[i][q]:
                                                                            potentials[i][q].remove(potentials[i][j][4])
                                                                        if potentials[i][j][5] in potentials[i][q]:
                                                                            potentials[i][q].remove(potentials[i][j][5])
                                                                        if potentials[i][j][6] in potentials[i][q]:
                                                                            potentials[i][q].remove(potentials[i][j][6])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[i][j]:
                    possibilities1.append(j)
            if len(possibilities1) == 7:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[i][j]:
                            possibilities2.append(j)
                    if set(possibilities2) == set(possibilities1):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[i][j]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for num4 in range(num3 + 1, 10):
                                    possibilities4 = []
                                    for j in range(9):
                                        if num4 in potentials[i][j]:
                                            possibilities4.append(j)
                                    if set(possibilities4) == set(possibilities1):
                                        for num5 in range(num4 + 1, 10):
                                            possibilities5 = []
                                            for j in range(9):
                                                if num5 in potentials[i][j]:
                                                    possibilities5.append(j)
                                            if set(possibilities5) == set(possibilities1):
                                                for num6 in range(num5 + 1, 10):
                                                    possibilities6 = []
                                                    for j in range(9):
                                                        if num6 in potentials[i][j]:
                                                            possibilities6.append(j)
                                                    if set(possibilities6) == set(possibilities1):
                                                        for num7 in range(num6 + 1, 10):
                                                            possibilities7 = []
                                                            for j in range(9):
                                                                if num7 in potentials[i][j]:
                                                                    possibilities7.append(j)
                                                            if set(possibilities7) == set(possibilities1):
                                                                for j in range(1, 10):
                                                                    if j not in (num1, num2, num3, num4, num5, num6, num7):
                                                                        if j in potentials[i][possibilities1[0]]:
                                                                            potentials[i][possibilities1[0]].remove(j)
                                                                        if j in potentials[i][possibilities1[1]]:
                                                                            potentials[i][possibilities1[1]].remove(j)
                                                                        if j in potentials[i][possibilities1[2]]:
                                                                            potentials[i][possibilities1[2]].remove(j)
                                                                        if j in potentials[i][possibilities1[3]]:
                                                                            potentials[i][possibilities1[3]].remove(j)
                                                                        if j in potentials[i][possibilities1[4]]:
                                                                            potentials[i][possibilities1[4]].remove(j)
                                                                        if j in potentials[i][possibilities1[5]]:
                                                                            potentials[i][possibilities1[5]].remove(j)
                                                                        if j in potentials[i][possibilities1[6]]:
                                                                            potentials[i][possibilities1[6]].remove(j)


def SeptupletColumns():
    for i in range(9):
        for j in range(9):
            if len(potentials[j][i]) == 7:
                for k in range(j + 1, 9):
                    if set(potentials[k][i]) == set(potentials[j][i]):
                        for l in range(k + 1, 9):
                            if set(potentials[l][i]) == set(potentials[j][i]):
                                for m in range(l + 1, 9):
                                    if set(potentials[m][i]) == set(potentials[j][i]):
                                        for n in range(m + 1, 9):
                                            if set(potentials[n][i]) == set(potentials[j][i]):
                                                for o in range(n + 1, 9):
                                                    if set(potentials[o][i]) == set(potentials[j][i]):
                                                        for p in range(o + 1, 9):
                                                            if set(potentials[p][i]) == set(potentials[j][i]):
                                                                for q in range(9):
                                                                    if q not in (j, k, l, m, n, o, p):
                                                                        if potentials[j][i][0] in potentials[q][i]:
                                                                            potentials[q][i].remove(potentials[j][i][0])
                                                                        if potentials[j][i][1] in potentials[q][i]:
                                                                            potentials[q][i].remove(potentials[j][i][1])
                                                                        if potentials[j][i][2] in potentials[q][i]:
                                                                            potentials[q][i].remove(potentials[j][i][2])
                                                                        if potentials[j][i][3] in potentials[q][i]:
                                                                            potentials[q][i].remove(potentials[j][i][3])
                                                                        if potentials[j][i][4] in potentials[q][i]:
                                                                            potentials[q][i].remove(potentials[j][i][4])
                                                                        if potentials[j][i][5] in potentials[q][i]:
                                                                            potentials[q][i].remove(potentials[j][i][5])
                                                                        if potentials[j][i][6] in potentials[q][i]:
                                                                            potentials[q][i].remove(potentials[j][i][6])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[j][i]:
                    possibilities1.append(j)
            if len(possibilities1) == 7:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[j][i]:
                            possibilities2.append(j)
                    if set(possibilities2) == set(possibilities1):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[j][i]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for num4 in range(num3 + 1, 10):
                                    possibilities4 = []
                                    for j in range(9):
                                        if num4 in potentials[j][i]:
                                            possibilities4.append(j)
                                    if set(possibilities4) == set(possibilities1):
                                        for num5 in range(num4 + 1, 10):
                                            possibilities5 = []
                                            for j in range(9):
                                                if num5 in potentials[j][i]:
                                                    possibilities5.append(j)
                                            if set(possibilities5) == set(possibilities1):
                                                for num6 in range(num5 + 1, 10):
                                                    possibilities6 = []
                                                    for j in range(9):
                                                        if num6 in potentials[j][i]:
                                                            possibilities6.append(j)
                                                    if set(possibilities6) == set(possibilities1):
                                                        for num7 in range(num6 + 1, 10):
                                                            possibilities7 = []
                                                            for j in range(9):
                                                                if num7 in potentials[j][i]:
                                                                    possibilities7.append(j)
                                                            if set(possibilities7) == set(possibilities1):
                                                                for j in range(1, 10):
                                                                    if j not in (num1, num2, num3, num4, num5, num6, num7):
                                                                        if j in potentials[possibilities1[0]][i]:
                                                                            potentials[possibilities1[0]][i].remove(j)
                                                                        if j in potentials[possibilities1[1]][i]:
                                                                            potentials[possibilities1[1]][i].remove(j)
                                                                        if j in potentials[possibilities1[2]][i]:
                                                                            potentials[possibilities1[2]][i].remove(j)
                                                                        if j in potentials[possibilities1[3]][i]:
                                                                            potentials[possibilities1[3]][i].remove(j)
                                                                        if j in potentials[possibilities1[4]][i]:
                                                                            potentials[possibilities1[4]][i].remove(j)
                                                                        if j in potentials[possibilities1[5]][i]:
                                                                            potentials[possibilities1[5]][i].remove(j)
                                                                        if j in potentials[possibilities1[6]][i]:
                                                                            potentials[possibilities1[6]][i].remove(j)


def SeptupletBoxes():
    for row in (2, 5, 8):
        for column in (2, 5, 8):
            for i, j in GetBox(row, column):
                if len(potentials[i][j]) == 7:
                    for k, l in GetBox(row, column):
                        if (k, l) != (i, j) and set(potentials[k][l]) == set(potentials[i][j]):
                            for m, n in GetBox(row, column):
                                if (m, n) not in ((i, j), (k, l)) and set(potentials[m][n]) == set(potentials[i][j]):
                                    for o, p in GetBox(row, column):
                                        if (o, p) not in ((i, j), (k, l), (m, n)) and set(potentials[o][p]) == set(potentials[i][j]):
                                            for q, r in GetBox(row, column):
                                                if (q, r) not in ((i, j), (k, l), (m, n), (o, p)) and set(potentials[q][r]) == set(potentials[i][j]):
                                                    for s, t in GetBox(row, column):
                                                        if (s, t) not in ((i, j), (k, l), (m, n), (o, p), (q, r)) and set(potentials[s][t]) == set(potentials[i][j]):
                                                            for u, v in GetBox(row, column):
                                                                if (u, v) not in ((i, j), (k, l), (m, n), (o, p), (q, r), (s, t)) and set(potentials[u][v]) == set(potentials[i][j]):
                                                                    for w, x in GetBox(row, column):
                                                                        if (w, x) not in ((i, j), (k, l), (m, n), (o, p), (q, r), (s, t), (u, v)):
                                                                            if potentials[i][j][0] in potentials[w][x]:
                                                                                potentials[w][x].remove(potentials[i][j][0])
                                                                            if potentials[i][j][1] in potentials[w][x]:
                                                                                potentials[w][x].remove(potentials[i][j][1])
                                                                            if potentials[i][j][2] in potentials[w][x]:
                                                                                potentials[w][x].remove(potentials[i][j][2])
                                                                            if potentials[i][j][3] in potentials[w][x]:
                                                                                potentials[w][x].remove(potentials[i][j][3])
                                                                            if potentials[i][j][4] in potentials[w][x]:
                                                                                potentials[w][x].remove(potentials[i][j][4])
                                                                            if potentials[i][j][5] in potentials[w][x]:
                                                                                potentials[w][x].remove(potentials[i][j][5])
                                                                            if potentials[i][j][6] in potentials[w][x]:
                                                                                potentials[w][x].remove(potentials[i][j][6])

            for num1 in range(1, 10):
                possibilities1 = []
                for i, j in GetBox(row, column):
                    if num1 in potentials[i][j]:
                        possibilities1.append((i, j))
                if len(possibilities1) == 7:
                    for num2 in range(num1 + 1, 10):
                        possibilities2 = []
                        for i, j in GetBox(row, column):
                            if num2 in potentials[i][j]:
                                possibilities2.append((i, j))
                        if set(possibilities2) == set(possibilities1):
                            for num3 in range(num2 + 1, 10):
                                possibilities3 = []
                                for i, j in GetBox(row, column):
                                    if num3 in potentials[i][j]:
                                        possibilities3.append((i, j))
                                if set(possibilities3) == set(possibilities1):
                                    for num4 in range(num3 + 1, 10):
                                        possibilities4 = []
                                        for i, j in GetBox(row, column):
                                            if num4 in potentials[i][j]:
                                                possibilities4.append((i, j))
                                        if set(possibilities4) == set(possibilities1):
                                            for num5 in range(num4 + 1, 10):
                                                possibilities5 = []
                                                for i, j in GetBox(row, column):
                                                    if num5 in potentials[i][j]:
                                                        possibilities5.append((i, j))
                                                if set(possibilities5) == set(possibilities1):
                                                    for num6 in range(num5 + 1, 10):
                                                        possibilities6 = []
                                                        for i, j in GetBox(row, column):
                                                            if num6 in potentials[i][j]:
                                                                possibilities6.append((i, j))
                                                        if set(possibilities6) == set(possibilities1):
                                                            for num7 in range(num6 + 1, 10):
                                                                possibilities7 = []
                                                                for i, j in GetBox(row, column):
                                                                    if num7 in potentials[i][j]:
                                                                        possibilities7.append((i, j))
                                                                if set(possibilities7) == set(possibilities1):
                                                                    for i in range(1, 10):
                                                                        if i not in (num1, num2, num3, num4, num5, num6, num7):
                                                                            if i in potentials[possibilities1[0][0]][possibilities1[0][1]]:
                                                                                potentials[possibilities1[0][0]][possibilities1[0][1]].remove(i)
                                                                            if i in potentials[possibilities1[1][0]][possibilities1[1][1]]:
                                                                                potentials[possibilities1[1][0]][possibilities1[1][1]].remove(i)
                                                                            if i in potentials[possibilities1[2][0]][possibilities1[2][1]]:
                                                                                potentials[possibilities1[2][0]][possibilities1[2][1]].remove(i)
                                                                            if i in potentials[possibilities1[3][0]][possibilities1[3][1]]:
                                                                                potentials[possibilities1[3][0]][possibilities1[3][1]].remove(i)
                                                                            if i in potentials[possibilities1[4][0]][possibilities1[4][1]]:
                                                                                potentials[possibilities1[4][0]][possibilities1[4][1]].remove(i)
                                                                            if i in potentials[possibilities1[5][0]][possibilities1[5][1]]:
                                                                                potentials[possibilities1[5][0]][possibilities1[5][1]].remove(i)
                                                                            if i in potentials[possibilities1[6][0]][possibilities1[6][1]]:
                                                                                potentials[possibilities1[6][0]][possibilities1[6][1]].remove(i)


def OctupletRows():
    for i in range(9):
        for j in range(9):
            if len(potentials[i][j]) == 8:
                for k in range(j + 1, 9):
                    if set(potentials[i][k]) == set(potentials[i][j]):
                        for l in range(k + 1, 9):
                            if set(potentials[i][l]) == set(potentials[i][j]):
                                for m in range(l + 1, 9):
                                    if set(potentials[i][m]) == set(potentials[i][j]):
                                        for n in range(m + 1, 9):
                                            if set(potentials[i][n]) == set(potentials[i][j]):
                                                for o in range(n + 1, 9):
                                                    if set(potentials[i][o]) == set(potentials[i][j]):
                                                        for p in range(o + 1, 9):
                                                            if set(potentials[i][p]) == set(potentials[i][j]):
                                                                for q in range(p + 1, 9):
                                                                    if set(potentials[i][q]) == set(potentials[i][j]):
                                                                        for r in range(9):
                                                                            if r not in (j, k, l, m, n, o, p, q):
                                                                                if potentials[i][j][0] in potentials[i][r]:
                                                                                    potentials[i][r].remove(potentials[i][j][0])
                                                                                if potentials[i][j][1] in potentials[i][r]:
                                                                                    potentials[i][r].remove(potentials[i][j][1])
                                                                                if potentials[i][j][2] in potentials[i][r]:
                                                                                    potentials[i][r].remove(potentials[i][j][2])
                                                                                if potentials[i][j][3] in potentials[i][r]:
                                                                                    potentials[i][r].remove(potentials[i][j][3])
                                                                                if potentials[i][j][4] in potentials[i][r]:
                                                                                    potentials[i][r].remove(potentials[i][j][4])
                                                                                if potentials[i][j][5] in potentials[i][r]:
                                                                                    potentials[i][r].remove(potentials[i][j][5])
                                                                                if potentials[i][j][6] in potentials[i][r]:
                                                                                    potentials[i][r].remove(potentials[i][j][6])
                                                                                if potentials[i][j][7] in potentials[i][r]:
                                                                                    potentials[i][r].remove(potentials[i][j][7])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[i][j]:
                    possibilities1.append(j)
            if len(possibilities1) == 8:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[i][j]:
                            possibilities2.append(j)
                    if set(possibilities2) == set(possibilities1):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[i][j]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for num4 in range(num3 + 1, 10):
                                    possibilities4 = []
                                    for j in range(9):
                                        if num4 in potentials[i][j]:
                                            possibilities4.append(j)
                                    if set(possibilities4) == set(possibilities1):
                                        for num5 in range(num4 + 1, 10):
                                            possibilities5 = []
                                            for j in range(9):
                                                if num5 in potentials[i][j]:
                                                    possibilities5.append(j)
                                            if set(possibilities5) == set(possibilities1):
                                                for num6 in range(num5 + 1, 10):
                                                    possibilities6 = []
                                                    for j in range(9):
                                                        if num6 in potentials[i][j]:
                                                            possibilities6.append(j)
                                                    if set(possibilities6) == set(possibilities1):
                                                        for num7 in range(num6 + 1, 10):
                                                            possibilities7 = []
                                                            for j in range(9):
                                                                if num7 in potentials[i][j]:
                                                                    possibilities7.append(j)
                                                            if set(possibilities7) == set(possibilities1):
                                                                for num8 in range(num7 + 1, 10):
                                                                    possibilities8 = []
                                                                    for j in range(9):
                                                                        if num8 in potentials[i][j]:
                                                                            possibilities8.append(j)
                                                                    if set(possibilities8) == set(possibilities1):
                                                                        for j in range(1, 10):
                                                                            if j not in (num1, num2, num3, num4, num5, num6, num7, num8):
                                                                                if j in potentials[i][possibilities1[0]]:
                                                                                    potentials[i][possibilities1[0]].remove(j)
                                                                                if j in potentials[i][possibilities1[1]]:
                                                                                    potentials[i][possibilities1[1]].remove(j)
                                                                                if j in potentials[i][possibilities1[2]]:
                                                                                    potentials[i][possibilities1[2]].remove(j)
                                                                                if j in potentials[i][possibilities1[3]]:
                                                                                    potentials[i][possibilities1[3]].remove(j)
                                                                                if j in potentials[i][possibilities1[4]]:
                                                                                    potentials[i][possibilities1[4]].remove(j)
                                                                                if j in potentials[i][possibilities1[5]]:
                                                                                    potentials[i][possibilities1[5]].remove(j)
                                                                                if j in potentials[i][possibilities1[6]]:
                                                                                    potentials[i][possibilities1[6]].remove(j)
                                                                                if j in potentials[i][possibilities1[7]]:
                                                                                    potentials[i][possibilities1[7]].remove(j)


def OctupletColumns():
    for i in range(9):
        for j in range(9):
            if len(potentials[j][i]) == 8:
                for k in range(j + 1, 9):
                    if set(potentials[k][i]) == set(potentials[j][i]):
                        for l in range(k + 1, 9):
                            if set(potentials[l][i]) == set(potentials[j][i]):
                                for m in range(l + 1, 9):
                                    if set(potentials[m][i]) == set(potentials[j][i]):
                                        for n in range(m + 1, 9):
                                            if set(potentials[n][i]) == set(potentials[j][i]):
                                                for o in range(n + 1, 9):
                                                    if set(potentials[o][i]) == set(potentials[j][i]):
                                                        for p in range(o + 1, 9):
                                                            if set(potentials[p][i]) == set(potentials[j][i]):
                                                                for q in range(p + 1, 9):
                                                                    if set(potentials[q][i]) == set(potentials[j][i]):
                                                                        for r in range(9):
                                                                            if r not in (j, k, l, m, n, o, p, q):
                                                                                if potentials[j][i][0] in potentials[r][i]:
                                                                                    potentials[r][i].remove(potentials[j][i][0])
                                                                                if potentials[j][i][1] in potentials[r][i]:
                                                                                    potentials[r][i].remove(potentials[j][i][1])
                                                                                if potentials[j][i][2] in potentials[r][i]:
                                                                                    potentials[r][i].remove(potentials[j][i][2])
                                                                                if potentials[j][i][3] in potentials[r][i]:
                                                                                    potentials[r][i].remove(potentials[j][i][3])
                                                                                if potentials[j][i][4] in potentials[r][i]:
                                                                                    potentials[r][i].remove(potentials[j][i][4])
                                                                                if potentials[j][i][5] in potentials[r][i]:
                                                                                    potentials[r][i].remove(potentials[j][i][5])
                                                                                if potentials[j][i][6] in potentials[r][i]:
                                                                                    potentials[r][i].remove(potentials[j][i][6])
                                                                                if potentials[j][i][7] in potentials[r][i]:
                                                                                    potentials[r][i].remove(potentials[j][i][7])

        for num1 in range(1, 10):
            possibilities1 = []
            for j in range(9):
                if num1 in potentials[j][i]:
                    possibilities1.append(j)
            if len(possibilities1) == 8:
                for num2 in range(num1 + 1, 10):
                    possibilities2 = []
                    for j in range(9):
                        if num2 in potentials[j][i]:
                            possibilities2.append(j)
                    if set(possibilities2) == set(possibilities1):
                        for num3 in range(num2 + 1, 10):
                            possibilities3 = []
                            for j in range(9):
                                if num3 in potentials[j][i]:
                                    possibilities3.append(j)
                            if set(possibilities3) == set(possibilities1):
                                for num4 in range(num3 + 1, 10):
                                    possibilities4 = []
                                    for j in range(9):
                                        if num4 in potentials[j][i]:
                                            possibilities4.append(j)
                                    if set(possibilities4) == set(possibilities1):
                                        for num5 in range(num4 + 1, 10):
                                            possibilities5 = []
                                            for j in range(9):
                                                if num5 in potentials[j][i]:
                                                    possibilities5.append(j)
                                            if set(possibilities5) == set(possibilities1):
                                                for num6 in range(num5 + 1, 10):
                                                    possibilities6 = []
                                                    for j in range(9):
                                                        if num6 in potentials[j][i]:
                                                            possibilities6.append(j)
                                                    if set(possibilities6) == set(possibilities1):
                                                        for num7 in range(num6 + 1, 10):
                                                            possibilities7 = []
                                                            for j in range(9):
                                                                if num7 in potentials[j][i]:
                                                                    possibilities7.append(j)
                                                            if set(possibilities7) == set(possibilities1):
                                                                for num8 in range(num7 + 1, 10):
                                                                    possibilities8 = []
                                                                    for j in range(9):
                                                                        if num8 in potentials[j][i]:
                                                                            possibilities8.append(j)
                                                                    if set(possibilities8) == set(possibilities1):
                                                                        for j in range(1, 10):
                                                                            if j not in (num1, num2, num3, num4, num5, num6, num7, num8):
                                                                                if j in potentials[possibilities1[0]][i]:
                                                                                    potentials[possibilities1[0]][i].remove(j)
                                                                                if j in potentials[possibilities1[1]][i]:
                                                                                    potentials[possibilities1[1]][i].remove(j)
                                                                                if j in potentials[possibilities1[2]][i]:
                                                                                    potentials[possibilities1[2]][i].remove(j)
                                                                                if j in potentials[possibilities1[3]][i]:
                                                                                    potentials[possibilities1[3]][i].remove(j)
                                                                                if j in potentials[possibilities1[4]][i]:
                                                                                    potentials[possibilities1[4]][i].remove(j)
                                                                                if j in potentials[possibilities1[5]][i]:
                                                                                    potentials[possibilities1[5]][i].remove(j)
                                                                                if j in potentials[possibilities1[6]][i]:
                                                                                    potentials[possibilities1[6]][i].remove(j)
                                                                                if j in potentials[possibilities1[7]][i]:
                                                                                    potentials[possibilities1[7]][i].remove(j)


def OctupletBoxes():
    for row in (2, 5, 8):
        for column in (2, 5, 8):
            for i, j in GetBox(row, column):
                if len(potentials[i][j]) == 8:
                    for k, l in GetBox(row, column):
                        if (k, l) != (i, j) and set(potentials[k][l]) == set(potentials[i][j]):
                            for m, n in GetBox(row, column):
                                if (m, n) not in ((i, j), (k, l)) and set(potentials[m][n]) == set(potentials[i][j]):
                                    for o, p in GetBox(row, column):
                                        if (o, p) not in ((i, j), (k, l), (m, n)) and set(potentials[o][p]) == set(potentials[i][j]):
                                            for q, r in GetBox(row, column):
                                                if (q, r) not in ((i, j), (k, l), (m, n), (o, p)) and set(potentials[q][r]) == set(potentials[i][j]):
                                                    for s, t in GetBox(row, column):
                                                        if (s, t) not in ((i, j), (k, l), (m, n), (o, p), (q, r)) and set(potentials[s][t]) == set(potentials[i][j]):
                                                            for u, v in GetBox(row, column):
                                                                if (u, v) not in ((i, j), (k, l), (m, n), (o, p), (q, r), (s, t)) and set(potentials[u][v]) == set(potentials[i][j]):
                                                                    for w, x in GetBox(row, column):
                                                                        if (w, x) not in ((i, j), (k, l), (m, n), (o, p), (q, r), (s, t), (u, v)) and set(potentials[w][x]) == set(potentials[i][j]):
                                                                            for y, z in GetBox(row, column):
                                                                                if (y, z) not in ((i, j), (k, l), (m, n), (o, p), (q, r), (s, t), (u, v), (w, x)):
                                                                                    if potentials[i][j][0] in potentials[y][z]:
                                                                                        potentials[y][z].remove(potentials[i][j][0])
                                                                                    if potentials[i][j][1] in potentials[y][z]:
                                                                                        potentials[y][z].remove(potentials[i][j][1])
                                                                                    if potentials[i][j][2] in potentials[y][z]:
                                                                                        potentials[y][z].remove(potentials[i][j][2])
                                                                                    if potentials[i][j][3] in potentials[y][z]:
                                                                                        potentials[y][z].remove(potentials[i][j][3])
                                                                                    if potentials[i][j][4] in potentials[y][z]:
                                                                                        potentials[y][z].remove(potentials[i][j][4])
                                                                                    if potentials[i][j][5] in potentials[y][z]:
                                                                                        potentials[y][z].remove(potentials[i][j][5])
                                                                                    if potentials[i][j][6] in potentials[y][z]:
                                                                                        potentials[y][z].remove(potentials[i][j][6])
                                                                                    if potentials[i][j][7] in potentials[y][z]:
                                                                                        potentials[y][z].remove(potentials[i][j][7])

            for num1 in range(1, 10):
                possibilities1 = []
                for i, j in GetBox(row, column):
                    if num1 in potentials[i][j]:
                        possibilities1.append((i, j))
                if len(possibilities1) == 8:
                    for num2 in range(num1 + 1, 10):
                        possibilities2 = []
                        for i, j in GetBox(row, column):
                            if num2 in potentials[i][j]:
                                possibilities2.append((i, j))
                        if set(possibilities2) == set(possibilities1):
                            for num3 in range(num2 + 1, 10):
                                possibilities3 = []
                                for i, j in GetBox(row, column):
                                    if num3 in potentials[i][j]:
                                        possibilities3.append((i, j))
                                if set(possibilities3) == set(possibilities1):
                                    for num4 in range(num3 + 1, 10):
                                        possibilities4 = []
                                        for i, j in GetBox(row, column):
                                            if num4 in potentials[i][j]:
                                                possibilities4.append((i, j))
                                        if set(possibilities4) == set(possibilities1):
                                            for num5 in range(num4 + 1, 10):
                                                possibilities5 = []
                                                for i, j in GetBox(row, column):
                                                    if num5 in potentials[i][j]:
                                                        possibilities5.append((i, j))
                                                if set(possibilities5) == set(possibilities1):
                                                    for num6 in range(num5 + 1, 10):
                                                        possibilities6 = []
                                                        for i, j in GetBox(row, column):
                                                            if num6 in potentials[i][j]:
                                                                possibilities6.append((i, j))
                                                        if set(possibilities6) == set(possibilities1):
                                                            for num7 in range(num6 + 1, 10):
                                                                possibilities7 = []
                                                                for i, j in GetBox(row, column):
                                                                    if num7 in potentials[i][j]:
                                                                        possibilities7.append((i, j))
                                                                if set(possibilities7) == set(possibilities1):
                                                                    for num8 in range(num7 + 1, 10):
                                                                        possibilities8 = []
                                                                        for i, j in GetBox(row, column):
                                                                            if num8 in potentials[i][j]:
                                                                                possibilities8.append((i, j))
                                                                        if set(possibilities8) == set(possibilities1):
                                                                            for i in range(1, 10):
                                                                                if i not in (num1, num2, num3, num4, num5, num6, num7, num8):
                                                                                    if i in potentials[possibilities1[0][0]][possibilities1[0][1]]:
                                                                                        potentials[possibilities1[0][0]][possibilities1[0][1]].remove(i)
                                                                                    if i in potentials[possibilities1[1][0]][possibilities1[1][1]]:
                                                                                        potentials[possibilities1[1][0]][possibilities1[1][1]].remove(i)
                                                                                    if i in potentials[possibilities1[2][0]][possibilities1[2][1]]:
                                                                                        potentials[possibilities1[2][0]][possibilities1[2][1]].remove(i)
                                                                                    if i in potentials[possibilities1[3][0]][possibilities1[3][1]]:
                                                                                        potentials[possibilities1[3][0]][possibilities1[3][1]].remove(i)
                                                                                    if i in potentials[possibilities1[4][0]][possibilities1[4][1]]:
                                                                                        potentials[possibilities1[4][0]][possibilities1[4][1]].remove(i)
                                                                                    if i in potentials[possibilities1[5][0]][possibilities1[5][1]]:
                                                                                        potentials[possibilities1[5][0]][possibilities1[5][1]].remove(i)
                                                                                    if i in potentials[possibilities1[6][0]][possibilities1[6][1]]:
                                                                                        potentials[possibilities1[6][0]][possibilities1[6][1]].remove(i)
                                                                                    if i in potentials[possibilities1[7][0]][possibilities1[7][1]]:
                                                                                        potentials[possibilities1[7][0]][possibilities1[7][1]].remove(i)


def RemoveFromTwoBoxes():
    for num in range(1, 10):
        for row1 in (2, 5, 8):
            for column1 in (2, 5, 8):
                for row2 in (2, 5, 8):
                    for column2 in (2, 5, 8):
                        if row1 == row2 and column1 != column2:
                            rows1 = []
                            for i, j in GetBox(row1, column1):
                                if num in potentials[i][j] and i not in rows1:
                                    rows1.append(i)
                            if len(rows1) == 2:
                                rows2 = []
                                for i, j in GetBox(row2, column2):
                                    if num in potentials[i][j] and i not in rows2:
                                        rows2.append(i)
                                if set(rows2) == set(rows1):
                                    for column3 in (2, 5, 8):
                                        if column3 not in (column1, column2):
                                            for i, j in GetBox(row1, column3):
                                                if i in rows1 and num in potentials[i][j]:
                                                    potentials[i][j].remove(num)

                        if row1 != row2 and column1 == column2:
                            columns1 = []
                            for i, j in GetBox(row1, column1):
                                if num in potentials[i][j] and j not in columns1:
                                    columns1.append(j)
                            if len(columns1) == 2:
                                columns2 = []
                                for i, j in GetBox(row2, column2):
                                    if num in potentials[i][j] and j not in columns2:
                                        columns2.append(j)
                                if set(columns2) == set(columns1):
                                    for row3 in (2, 5, 8):
                                        if row3 not in (row1, row2):
                                            for i, j in GetBox(row3, column1):
                                                if j in columns1 and num in potentials[i][j]:
                                                    potentials[i][j].remove(num)


def SwordFish():
    for num in range(1, 10):
        points = []
        rows = []
        for i in range(9):
            possibilities = []
            for j in range(9):
                if num in potentials[i][j]:
                    possibilities.append((i, j))
            if len(possibilities) == 2:
                points.append(possibilities[0])
                points.append(possibilities[1])
                rows.append(i)
        if len(rows) >= 2:
            newrows = GetCombinations(rows)
            for combination in newrows:
                newpoints = []
                for i, j in points:
                    if i in combination:
                        newpoints.append((i, j))
                if FormsSwordFish(newpoints):
                    for i, j in newpoints:
                        for k in range(9):
                            if (k, j) not in newpoints and num in potentials[k][j]:
                                potentials[k][j].remove(num)

        points = []
        columns = []
        for i in range(9):
            possibilities = []
            for j in range(9):
                if num in potentials[j][i]:
                    possibilities.append((j, i))
            if len(possibilities) == 2:
                points.append(possibilities[0])
                points.append(possibilities[1])
                columns.append(i)
        if len(columns) >= 2:
            newcolumns = GetCombinations(columns)
            for combination in newcolumns:
                newpoints = []
                for j, i in points:
                    if i in combination:
                        newpoints.append((j, i))
                if FormsSwordFish(newpoints):                    
                    for i, j in newpoints:
                        for k in range(9):
                            if (i, k) not in newpoints and num in potentials[i][k]:
                                potentials[i][k].remove(num)


def FormsSwordFish(points):
    for i, j in points:
        xneighbours, yneighbours = 0, 0
        for l, m in points:
            if (i, j) != (l, m):
                if i == l:
                    yneighbours += 1
                if j == m:
                    xneighbours += 1
        if (xneighbours, yneighbours) != (1, 1):
            return False
    return True


def GetCombinations(numbers):
    combinations = []
    for i in range(2, len(numbers) + 1):
        for j in itertools.combinations(numbers, i):
            combinations.append(j)
    return combinations


main()
