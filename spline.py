#!/bin/python3
import math as m
class spline:
    def __init__(self, pontos):
        self.pontos = pontos

    def distancia(self, ponto0, ponto1):
        ponto0x = ponto0[0]
        ponto0y = ponto0[1]
        ponto1x = ponto1[0]
        ponto1y = ponto1[1]
        deltaX = ponto0x - ponto1x
        deltaY = ponto0y - ponto1y
        dist = (deltaX**2 + deltaY**2)**0.5
        return dist


    def pivotamento(self, A, b, j):
        p = j
        n = len(A)
        for k in range(j + 1, n):
            if(m.fabs(A[k][j]) > m.fabs(A[p][j])):
                p = k
        for k in range(j, n):
            aux = A[j][k]
            A[j][k] = A[p][k]
            A[p][k] = aux

        aux = b[j]
        b[j] = b[p]
        b[p] = aux
        return [A, b]

    def retroSubst (self, A, b):
        n = len(A)
        x = [0] * n
        for i in range(n - 1, -1, -1):
            s = 0
            for j in range(i + 1, n):
                s += A[i][j] * x[j]
            x[i] = (b[i] - s) / A[i][i]
        return x

    def gauss(self, A, b):
        n = len(A)
        for j in range(n - 1):
            y = self.pivotamento(A, b, j)
            A = y[0]
            b = y[1]
            for i in range (j+1, n):
                f = A[i][j] / A[j][j]
                for k in range(j, n):
                    A[i][k] -= A[j][k] * f
                b[i] -= b[j] * f
        return self.retroSubst(A, b)

    def casteljau(self, b, t, i, k):
        if (k > 1):
            return (1 - t)*self.casteljau(b, t, i, k - 1) + t * self.casteljau(b, t, i + 1, k - 1)
        else:
            return (1 - t) * b[i] + t * b[i + 1]

    def calculaSpline(self, tensao, uniforme = True, aberta = True):
        n = len(self.pontos)
        h = [0] * (n + 1)
        if(uniforme == True):
            for i in range(1, n):
                h[i] = 1
        else:
            for i in range(1, n):
                h[i] = self.distancia(self.pontos[i], self.pontos[i - 1])
        if(aberta == True):
            h[0] = h[n] = 0
        else:
            h[0] = h[n] = self.distancia(self.pontos[-1], self.pontos[0])
        # Cálculo do gama
        gama = [0] * n
        for i in range(0, n):
            gama[i] = 2 * (h[i] + h[i + 1])
            gama[i] /= (tensao[i]*h[i]*h[i+1] + 2 * (h[i] + h[i + 1]))
        # Cálculo do lambda e do mi
        lambd = [0] * n
        mi = [0] * n
        for i in range(1, n - 1):
            lambd[i] = gama[i - 1] * h[i - 1] + h[i]
            lambd[i] /= gama[i - 1]*h[i - 1] + h[i] + gama[i]*h[i + 1]
            mi[i] = gama[i] * h[i]
            mi[i] /= gama[i] * h[i] + h[i + 1] + gama[i + 1] * h[i + 2]
        if(aberta == True):
            lambd[0] = lambd[-1] = 1
            mi[0] = mi[-1] = 0
        else:
            lambd[0] = gama[-1] * h[-1] + h[0]
            lambd[0] /= gama[-1]*h[-1] + h[0] + gama[0]*h[1]
            mi[0] = gama[0] * h[0]
            mi[0] /= gama[0] * h[0] + h[1] + gama[1] * h[2]
            lambd[-1] = gama[-2] * h[-2] + h[-1]
            lambd[-1] /= gama[-2]*h[-2] + h[-1] + gama[-1]*h[0]
            mi[-1] = gama[-1] * h[-1]
            mi[-1] /= gama[-1] * h[-1] + h[n] + gama[0] * h[1]
        # Cálculo do delta
        delta = [0] * n
        a = [0] * n
        b = [0] * n
        c = [0] * n
        for i in range(n):
            delta[i] = h[i] / (h[i] + h[i+1])
            a[i] = (1 - delta[i]) * (1 - lambd[i])
            b[i] = (1 - delta[i]) * lambd[i] + delta[i] * (1 - mi[i])
            c[i] = delta[i] * mi[i]
        print(a)
        print(b)
        print(c)
        A = []
        for i in range(n):
            linha = []
            for j in range(n):
                if(j == i):
                    linha.append(b[i])
                elif(j - i == 1):
                    linha.append(c[i])
                elif(i - j == 1):
                    linha.append(a[i])
                elif(i == 0 and j == n - 1):
                    linha.append(a[i])
                elif(i == n - 1 and j == 0):
                    linha.append(c[i])
                else:
                    linha.append(0)
            A.append(linha)

        print(A)
        b = n * [0]
        #Para x:
        for i in range(n):
            b[i] = self.pontos[i][0]
        self.Dx = self.gauss(A, b)
        #Para y:
        for i in range(n):
            b[i] = self.pontos[i][1]
        self.Dy = self.gauss(A, b)
        # Cálculo de R e L
        self.Rx = n * [0]
        self.Ry = n * [0]
        self.Lx = n * [0]
        self.Ly = n * [0]
        for i in range(n - 1):
            self.Rx[i] = (1 - mi[i]) * self.Dx[i] + mi[i] * self.Dx[i + 1]
            self.Ry[i] = (1 - mi[i]) * self.Dy[i] + mi[i] * self.Dy[i + 1]
            self.Lx[i] = (1 - lambd[i + 1]) * self.Dx[i] + lambd[i + 1] * self.Dx[i + 1]
            self.Ly[i] = (1 - lambd[i + 1]) * self.Dy[i] + lambd[i + 1] * self.Dy[i + 1]
            
    def avalia(self, t, i):
        bx = [self.Px[i], self.Rx[i], self.Lx[i], self.Px[i + 1]]
        by = [self.Py[i], self.Ry[i], self.Ly[i], self.Py[i + 1]]

pontos = [[0, 0], [1, 2], [2, 3]]
tensao = [0, 0, 0]
mySpline = spline(pontos)
mySpline.calculaSpline(tensao)
print(mySpline.casteljau([21, 10.2139, 33, 66], 5, 0, 3))
