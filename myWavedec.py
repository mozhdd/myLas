import pywt
from math import sqrt, pow, log
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, show
import numpy as np
import math
import timeit

wavelet = pywt.Wavelet("db2")

s=[1,2,3,4,5,6,7,8, 9,10,11,12,13,14,15]
s = np.linspace(0, 17, 24)
# s = [2,1,1,1,1,1,1,1,2]
# s = [1,2,3,4,5,6,7,8]

# print('========= dwt ===========')
# cA, cD =  pywt.dwt(s, 'db2')
# print(cA)
# print(cD)


print('========= wavedec ===========')
res = pywt.wavedec(s, "db3")
for el in res:
    print(el)



def test_filter(s, h):
    print('====== Test filter ======')
    for j in range(len(h)):
        tmp = 0
        for i in range(j+1):
            tmp += h[i] * s[len(s) - 1 - j + i]
        print(tmp)


# http://cs636123.vk.me/v636123054/49d9/wM663kU3vkQ.jpg
def dec1(x, h):
    N = len(x)
    L = len(h)
    res = np.zeros(N + L - 1)
    for t in range(0, N + L - 1):
        for l in range(0, L):
            if t-l < 0:
                tmp = l - t - 1
                res[t] += h[l] * x[tmp]  # continue
                continue
            if t-l >= N:
                tmp = 2*N - t - 1 + l
                res[t] += h[l] * x[tmp]  # continue
            else: res[t] += h[l] * x[t - l]
    return [res[i] for i in range(1, len(res), 2)]

# downsapling inside
def dec2(x, h):
    N = len(x)
    L = len(h)
    res = []
    for t in range(1, N + L - 1, 2):
        res.append(0)
        for l in range(0, L):
            if t-l < 0:
                tmp = l - t - 1
                res[len(res)-1] += h[l] * x[tmp]  # continue
                continue
            if t-l >= N:
                tmp = 2*N - t - 1 + l
                res[len(res)-1] += h[l] * x[tmp]  # continue
            else: res[len(res)-1] += h[l] * x[t - l]
    return res

def dwt(s, level):
    wavelet = pywt.Wavelet('db'+str(level))
    return [dec2(s,wavelet.dec_lo), dec2(s,wavelet.dec_hi)]

# ============= best time ================
def dwt2(x, level):
    wavelet = pywt.Wavelet('db'+str(level))
    h = wavelet.dec_lo
    g = wavelet.dec_hi
    N = len(x)
    L = len(h)
    cA = []
    cD = []
    for t in range(1, N + L - 1, 2):
        cA.append(0)
        cD.append(0)
        for l in range(0, L):
            if t-l < 0:
                cA[len(cA)-1] += h[l] * x[l - t - 1]
                cD[len(cD)-1] += g[l] * x[l - t - 1]
                continue
            if t-l >= N:
                cA[len(cA)-1] += h[l] * x[2*N - t - 1 + l]
                cD[len(cD)-1] += g[l] * x[2*N - t - 1 + l]
            else:
                cA[len(cA)-1] += h[l] * x[t - l]
                cD[len(cD)-1] += g[l] * x[t - l]
    return [cA, cD]


def myWaveDec(s, level):
    res = []
    cA = s
    wavelet = pywt.Wavelet('db' + str(level))
    #dec_level = pywt.dwt_max_level(len(s), len(wavelet.dec_lo))
    dec_level = math.floor(log(len(s) / (len(wavelet.dec_lo) - 1)) / log(2))

    for i in range(0, dec_level-1):
        (cA, cD) = dwt2(cA, level)
        res.append(cD)
    (cA, cD) = dwt2(cA, level)
    res.append(cD)
    res.append(cA)
    return res

print('========= my wavedec ===========')
res = myWaveDec(s, 3)
for el in reversed(res):
    print(el)

# cA, cD = dwt(s, 2)
# print('========= dwt ===========')
# print(cA)
# print(cD)


# st = '[9,8,7,6,4,3,2,1,1,2,2,3,3,3,3,3,3,2,2,2,-5,6,7,34,345,345,543,5,3,4,3],2)'
# # print(timeit.timeit("dwt([9,8,7,6,4,3,2,1],2)", setup="from dwt import dwt"))
# print(min(timeit.Timer('dwt('+st, setup="from dwt import dwt").repeat(7, 1000)))
# print('=================')
# print(min(timeit.Timer('dwt2('+st, setup="from dwt import dwt2").repeat(7, 1000)))


# h = wavelet.dec_lo
# # print('========= filter ===========\n', h)
# res = dec1(s, h)
# print('========= my dwt1 ===========\n',res)
# print('========= my dwt2 ===========\n',dec2(s, h))