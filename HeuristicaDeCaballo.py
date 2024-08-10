import sys
import random 
movX = (2, 1, -1, -2, -2, -1, 1, 2)
movY = (-1, -2, -2, -1, 1, 2, 2, 1)
columna = 0
fila = 0
tablero = []
caballo = "_"
paso = " "

def iniciar(y, x):
    with open('tablero.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        row = [int(i) for i in line.split()]
        tablero.append(row)

    global columna, fila
    tablero[y][x] = caballo
    columna = x
    fila = y
    mostrar_tablero()

    while(True):
        valor = input("('?' para salir) cualquier valor para continuar: ")
        if (valor == "?"):
            break
        sys.stdout.write('\033[2J\033[H')
        mover_caballo()
        mostrar_tablero()

def mostrar_tablero():
    for i in tablero:
        print(*i)
    print()

def mover_caballo():
    global columna, fila, movX, movY
    indices = posiciones(True) #devuelve una tupla con los índices de movimientos
    if (indices is None):
        print("Se terminó el juego")
        sys.exit()
    i = 0 #se selecciona el primer índice de indeces, se intuye que es la posición de menor valor
    if (len(indices) > 1): #true solo si las posiciones de menor valor se repiten
        a = columna + movX[indices[i]]
        b = fila + movY[indices[i]]
        value = tablero[b][a]
        origX = columna
        origY = fila
        for j in range(len(indices)): #bloque para hacer movimientos fantasma
            columna += movX[indices[j]]
            fila += movY[indices[j]]
            val = posiciones(False) #devuelve valores numéricos de la tabla (heurística)
            columna = origX
            fila = origY
            if (val is None):
                break
            if (val[0] == value):
                i = j if (random.randint(0,1) == 1) else i
            if (val[0] < value):
                value = val[0]
                i = j 

    i = indices[i] 
    a = columna + movX[i]
    b = fila + movY[i]
    tablero[fila][columna] = paso
    columna = a
    fila = b
    tablero[fila][columna] = caballo

def posiciones(indices: bool):
    global columna, fila, movX, movY
    result = list() #movimientos válidos
    for i in range(8):
        a = columna + movX[i]
        b = fila + movY[i]
        if ((0 <= a <= 7 and 0 <= b <= 7) and (tablero[b][a] not in (paso, caballo))):
            result.append((tablero[b][a], i))
    if (len(result) == 0):
        return None
    result.sort()
    min = result[0][0] #valor mínimo de heurística
    return tuple((lambda : j if(indices) else i)() for i, j in result if(min == i))

if __name__ == "__main__":
    iniciar(2, 3) #posición de inicial