import numpy as np
from scipy import interpolate
from matplotlib.pyplot import *


def newt(x, y):
    size = np.shape(y)[0]
    tempTable = np.zeros([size, size])
    tempTable[::,0] = y
    for j in range(1,size):
        for i in range(size-j):
            tempTable[i][j] = (tempTable[i+1][j-1] - tempTable[i][j-1]) / (x[i+j] - x[i])
    result = np.polynomial.Polynomial([0.])
    for i in range(tempTable[0].shape[0]):
        tempPoly = np.polynomial.Polynomial([1.])
        for j in range(i):
            polyMultiplier = np.polynomial.Polynomial([-x[j], 1.])
            tempPoly = tempPoly * polyMultiplier
        tempPoly = tempPoly * tempTable[0][i]
        result = np.polyadd(result, tempPoly)
    return np.flip(result[0].coef, axis=0)

def func2(x,y):
    repack = np.array((x,y))
    tck,u = interpolate.splprep(repack,s=0)
    tempPoint = np.arange(0,1.02,0.01)
    return interpolate.splev(tempPoint,tck)


if __name__ == '__main__':

    #11 punktów wybranych z krzywej

    x = np.linspace(0, 11, 11)
    fx = np.array([0, 3, 5, 3, 8, 6, 15, 4, 0.5, 13, 10.5])

    newtResult = newt(x,fx)
    funcResult = func2(x,fx)
    x_axis = np.linspace(0, 11, num=1000)
    y_axis = np.polyval(newtResult, x_axis)
    plot(x,fx, "ro")
    plot(x_axis, y_axis, label = 'Interpolacja Newtona')
    plot(funcResult[0],funcResult[1],color = "green", label = 'Kubiczna funkcja sklejana')
    legend()
    show()