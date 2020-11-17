

def isSafe(matrix, visited, x, y):
    return not (matrix[x][y] == 0 or visited[x][y])


# daca nu este o pozitie valida se returneaza fals
def isValid(x, y):
    return M > x >= 0 and N > y >= 0

def findShortestPath(matrix, visited, i, j, x, y, min_dist=float('inf'), dist=0):

    count=0
    # se updateaza distanta minima
    if i == x and j == y:
        return min(dist, min_dist)

    # se marcheaza (i, j) ca fiind vizitate
    visited[i][j] = 1
    print(i,j)
    count=count+1

    # deplsare in jos
    if isValid(i + 1, j) and isSafe(matrix, visited, i + 1, j):
        min_dist = findShortestPath(matrix, visited, i + 1, j, x, y, min_dist, dist + 1)

    # miscare spre dreapta
    if isValid(i, j + 1) and isSafe(matrix, visited, i, j + 1):
        min_dist = findShortestPath(matrix, visited, i, j + 1, x, y, min_dist, dist + 1)

    # deplasare in sus
    if isValid(i - 1, j) and isSafe(matrix, visited, i - 1, j):
        min_dist = findShortestPath(matrix, visited, i - 1, j, x, y, min_dist, dist + 1)

    # deplasare la stanga in matrice
    if isValid(i, j - 1) and isSafe(matrix, visited, i, j - 1):
        min_dist = findShortestPath(matrix, visited, i, j - 1, x, y, min_dist, dist + 1)

    
    # se indeparteaza (i,j) ca fiind vizitate din matrice
    visited[i][j] = 0
    #print("Numarul de pasi pe care il face bkt : ", count)
    return min_dist
 

if __name__ == '__main__':

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

    M = N = 10

    #se retin locurile vizitate
    visited = [[0 for x in range(N)] for y in range(M)]
    
    
    min_dist = findShortestPath(matrix, visited, 0, 5, 7, 6)
    if min_dist != float('inf'):
        print("Cel mai scurt drum in labirint este de lungime :", min_dist)
        
    else:
        print("Nu exista un drum intre punctul de start si cel de final")
    
    
