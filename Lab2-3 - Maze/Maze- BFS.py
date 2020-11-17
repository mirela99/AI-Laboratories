from collections import deque
# In listele de mai jos sunt cele 4 posibile miscari, sus , jos, dreapta, stanga

row = [-1, 0, 0, 1]
col = [0, -1, 1, 0]

# Functia verifica daca este posibila mutarea pozitiei in (row,col) din pozitia curenta
# returneazza 0 daca este fals sau daca a fost deja vizitat

def isValid(matrix, visited, row, col):
    return (row >= 0) and (row < M) and (col >= 0) and (col < N) \
           and matrix[row][col] == 1 and not visited[row][col]

def BFS(matrix, i, j, x, y):

    count=0
    # matrice care tine minte nodurile vizitate
    visited = [[False for x in range(N)] for y in range(M)]
    q = deque()
    visited[i][j] = True # se pune nodul ca vizitat si se adauga in coada noastra
    # (i, j, dist) coordonatele matricii si distanta minima de la sursa
    q.append((i, j, 0))

    # memoreaza lungimea celui mai scurt drum din labirint
    min_dist = float('inf')

    # pana cand coada este goala
    while q:
        print(i,j)
        count=count+1
        (i, j, dist) = q.popleft()  # elimina nodul din varf si verifica
        # daca se gaseste punctul final, se updateaza lungimea celui mai scurt drum
        if i == x and j == y:
            min_dist = dist
            break

        # se verifica cele 4 mutari posibilie din punctul in care suntem in matrice si se valideaza fiecare
        for k in range(4):
            
            
            if isValid(matrix, visited, i + row[k], j + col[k]):
                # se marcheaza urmatoarea valoare din matrice ca si vizitata si se adauga in coada
                visited[i + row[k]][j + col[k]] = True
                q.append((i + row[k], j + col[k], dist + 1))
        
    

    if min_dist != float('inf'):
        print("Cel mai scurt drum are lungimea", min_dist)
    else:
        print("Nu exista un drum de la punctul de start la cel de final in acest labirint")

    print("Numarul de pasi pe care ii face bfs : ", count)


if __name__ == '__main__':

    # matricea de input a labirintului 
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

    #Gasirea celui mai scurt drum in labirint de la pozitia de start (0,4) la  pozitia de finist (7,5)
    BFS(matrix, 0, 4, 7, 5)
