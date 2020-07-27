import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

x = np.array([1,2,3,4,5,6,7,8,9,10,11])
fx = np.array([1,3,5,3,8,6,15,4,0.5,13,10.5])

def Newton1(x, y):
    size = len(x)
    tempTable = np.zeros((size,size+1))
    tempTable[:,0]= x;
    tempTable[:,1]= y;
    for i in range(2,size+1):
        for j in range(i-1,size):
            tempTable[j][i] = (tempTable[j][i-1]-tempTable[j-1][i-1])/(tempTable[j][0]-tempTable[j-i+1][0])
    result = np.zeros(size)
    for i in range(0,size):
        result[i] = tempTable[i][i+1]
    resultPoly = np.polynomial.Polynomial([0.])
    for i in range(len(result)):
        tempPoly = np.polynomial.Polynomial([1.])
        for j in range(i):
            polyMultiplier = np.polynomial.Polynomial([-x[j], 1.])
            tempPoly = tempPoly * polyMultiplier
        tempPoly = tempPoly * result[i]
        resultPoly = np.polyadd(resultPoly, tempPoly)
    p = np.flip(resultPoly[0].coef, axis=0)
    print(p)
    return p

def poly(t,x,p):
    n = len(x)
    out = p[n-1]
    for i in range(n-2,-1,-1):
        out = out*(t-x[i]) + p[i]
    return out
if __name__ == '__main__':

    newtResult = Newton1(x,fx)
    x_axis = np.linspace(0,11, 100)
    y_axis = poly(x_axis,x,newtResult)
    plt.plot(x, fx, "ro")
    #plt.plot(x_axis, y_axis)
    plt.show()