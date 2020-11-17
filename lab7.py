import numpy as np

#functia de activare sigmoida
def functieSigmoida(x):
    return 1/(1 + np.exp(-x))

#derivata functiei de activare sigmoida
def derivataSigmoida(x):
    rez = functieSigmoida(x)
    return rez * (1 - rez)

#Date ale functiei XOR
date_intare = [[0,0], [0,1],[1,0], [1,1]]
rezultat_asteptat = []
print("Introduceti valorile pentru functia logica dorita :")
for i in range (0,4):
    i=int(input())
    rezultat_asteptat.append(i)
print(rezultat_asteptat)
rezultate = []
eroareMedie = 0

#Initializarea ponderilor si a gradientilor
ponderi = []
praguri = []
gradienti = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
corectiiPonderi =[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

erori = []
#date de la tastatura 
epoci= int(input("Numarul de epoci :"))
rataInvatare= float(input("Rata de invatare: "))
#Initializare ponderi
ponderiDate = []
for i in range(1,5):
    if i < 3:
        ponderiDate.append([round(np.random.uniform(-0.1,0.1), 5), round(np.random.uniform(-0.1,0.1), 5)])
    else:
        ponderiDate.append([round(np.random.uniform(-0.1,0.1), 5)])
for i in range(1,5):
    ponderi.append(ponderiDate)
    

#Initializare praguri
for i in range (1,4):
    praguri.append(round(np.random.uniform(-0.1,0.1), 5))

def calculIesireDinStratAscuns(i,x1,x2,j):
    if j == 0:
        sum = x1 * ponderi[i][j][j] + x2 * ponderi[i][j+1][j] - praguri[j]
    elif j == 1:
        sum = x1 * ponderi[i][j-1][j] + x2 * ponderi[i][j][j] - praguri[j]
    return functieSigmoida(sum)

def calculIesireDinRetea(i,y1,y2):
    sum = y1 * ponderi[i][2][0] + y2 * ponderi[i][3][0] - praguri[2]
    return functieSigmoida(sum)

def eroarea_medie_patratica(asteptat, obtinut):
    i = 0
    sum = 0
    while i < len(asteptat):
        dif = asteptat[i] - obtinut[i][2]
        sum += dif
        i += 1
    return round(sum/2,5)


def algoritm():
    for _ in range(0,epoci):
        #Propagare inainte
        i = -1
        for date in date_intare:
            i += 1
            
            y1 = round(calculIesireDinStratAscuns(i,date[0], date[1], 0),5)
            y2 = round(calculIesireDinStratAscuns(i,date[0], date[1], 1),5)
            
            iesire = round(calculIesireDinRetea(i,y1,y2),5)
            rezultate.append([y1,y2,iesire])

            
            print("\nRezultat obtinut pt : " + str(date[0]) + ' ' + str(date[1])+ ' ' + str(rezultate[i][2]))
        
            erori.append(rezultat_asteptat[i]-rezultate[i][2])
            
            #Propagare inapoi
            gradienti[2] = (round(derivataSigmoida(rezultate[i][2]) * erori[i], 5))
            
            for index in range(5,7):
                corectiiPonderi[i][index-1] += round(rataInvatare * rezultate[i][2] * gradienti[2],5)

            gradienti[1] = (round(derivataSigmoida(rezultate[i][1]) * gradienti[2] * ponderi[i][3][0], 5))
            gradienti[0] = (round(derivataSigmoida(rezultate[i][0]) * gradienti[2] * ponderi[i][2][0], 5))
            
            #Actualizam corectiile ponderilor dintre stratul de intrare si stratul ascuns 
            for index in range(1,5):
                if index == 1 or index == 3:
                    if index == 1:
                        corectiiPonderi[i][index-1] += round(rataInvatare * rezultate[i][0] * ponderi[i][0][0],5)
                    else:
                        corectiiPonderi[i][index-1] += round(rataInvatare * rezultate[i][0] * ponderi[i][1][0],5)
                else: 
                    if index == 2:
                        corectiiPonderi[i][index-1] += round(rataInvatare * rezultate[i][1] * ponderi[i][0][1],5)
                    else:
                        corectiiPonderi[i][index-1] += round(rataInvatare * rezultate[i][1] * ponderi[i][1][1],5)

            for index in range(0,4):
                if index == 0:
                    ponderi[i][index][0] += corectiiPonderi[i][0]
                    ponderi[i][index][1] += corectiiPonderi[i][1]
                elif index == 1:
                    ponderi[i][index][0] += corectiiPonderi[i][2]
                    ponderi[i][index][1] += corectiiPonderi[i][3]
                elif index == 2:
                    ponderi[i][index][0] += corectiiPonderi[i][4]
                else:
                    ponderi[i][index][0] += corectiiPonderi[i][5]

algoritm()

# print('\n Valoarea rotunjita a prezicerilor: \n ')
# for valoare in rezultate :
#     print(np.round(valoare))
