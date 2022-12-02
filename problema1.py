"""
Consideremos el caso general de una cuadrícula de M x N donde M, N > 2.
Podemos dar una vuelta completa sobre el borde de la cuadrícula y terminar en
la esquina superior izquierda de una cuadrícula de (M - 2) x (N - 2) con la
misma orientación con la que iniciamos.

    +--+--+--+--+--+
    |> |  |  |  |  |       x   x  x  x  x
    +--+--+--+--+--+         +--+--+--+
    |  |  |  |  |  |       x |> |  |  | x
    +--+--+--+--+--+   ==>   +--+--+--+
    |  |  |  |  |  |       x |  |  |  | x
    +--+--+--+--+--+         +--+--+--+
    |  |  |  |  |  |       x   x  x  x  x
    +--+--+--+--+--+

Repitiendo este procedimiento varias veces, logramos reducir la cuadrícula a
una de M x N donde M = 1, M = 2, N = 1 o N = 2. Por lo tanto, la respuesta
depende de la paridad de M y N. Los casos bases podemos verificarlos
manualmente.
"""
if __name__ == '__main__':
    T = int(input())
    for _ in range(T):
        M, N = list(map(int, input().split()))
        if M <= N:
            # Caso 1: M <= N, M impar. La cuadrícula se reduce a una de 1 x K
            # para algún K >= 1.
            if M % 2 != 0:
                print('R')
            # Caso 2: M <= N, M par. La cuadrícula se reduce a una de 2 x K
            # para algún K >= 2
            else:
                print('L')
        else:
            # Caso 3: M > N, N impar. La cuadrícula se reduce a una de K x 1
            # para algún K > 1.
            if N % 2 != 0:
                print('D')
            # Caso 4: M > N, N par. La cuadrícula se reduce a una de K x 2 para
            # algún K > 2.
            else:
                print('U')
