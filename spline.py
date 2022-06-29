#!/bin/python3

n = 6
h = (n + 1) * [1]
Px = [1, 2, 3, 4, 5]

gama = n * [0]
ni = n * [0.1]

# spline aberta
h[0] = h[n-1] = 0
for i in range(1, n - 1):
    h[i] = Px[i] - Px[i - 1]

for i in range(0, n):
    gama[i] = 2 * (h[i] + h[i+1])
    gama[i] /= (ni[i] * h[i] * h[i+1] + 2*(h[i] + h[i+1]))
lambd = n * [0]
mi = n * [0]
for i in range(1, n - 1):
    lambd[i] = gama[i-1] * h[i-1] + h[i]
    lambd[i] /= (gama[i-1] * h[i-1] + h[i] + gama[i] * h[i+1])
    mi[i] = gama[i] * h[i]
    mi[i] /= (gama[i] * h[i] + h[i+1] + gama[i+1] * h[i+2])

#spline aberta
gama[0] = gama[n-1] = 0
mi[0] = mi[n-1] = 0

a = n * [0]
b = n * [0]
c = n * [0]
for i in range(0, n):
    delta = h[i] / (h[i] + h[i+1])
    a[i] = (1 - delta) * (1 - lambd[i])
    b[i] = (1 - delta) * lambd[i] + delta * (1 - mi[i])
    c[i] = delta * mi[i]


# Sistema: A D = P
# Matriz A
'''
a = ["a0", "a1", "a2", "a3", "a4", "a5"]
b = ["b0", "b1", "b2", "b3", "b4", "b5"]
c = ["c0", "c1", "c2", "c3", "c4", "c5"]
'''
a = ["a0", "a1", "a2"]
b = ["b0", "b1", "b2"]
c = ["c0", "c1", "c2"]
n = len(a)
A = []
for lin in range(0, n):
    linha = []
    for col in range (0, n):
        if(lin == (col + 1) % n):
            linha.append(a[lin])
        elif(lin == col):
            linha.append(b[lin])
        elif(lin == (col - 1) % n):
            linha.append(c[lin])
        else:
            linha.append(0)
    A.append(linha)
print(A)

# Vetor D
n = 5
D = n * [0]

# Vetor P
n = 5
P = n * [0]
