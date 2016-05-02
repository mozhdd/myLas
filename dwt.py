import pywt
from math import sqrt, pow
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, show
import numpy as np
import math
from scipy.signal import decimate

wavelet = pywt.Wavelet("db2")
lo = np.array(wavelet.dec_lo[::-1]) #reversed(wavelet.dec_lo)
hi = np.array(wavelet.dec_hi[::-1]) #reversed(wavelet.dec_hi)

s=[1,2,3,4,5,6,7,8, 9,10,11,12,13,14,15]
s = np.linspace(0, 17, 16)
# s = [2,1,1,1,1,1,1,1,2]
# s = [1,2,3,4,5,6,7,8]
# s = [32, 10, 20, 38, 37, 28, 38, 34, 18, 24, 18, 9, 23, 24, 28, 34]

print('========= dwt ===========')
cA, cD =  pywt.dwt(s, 'db2')
print(cA)
# for el in pywt.wavedec(s, "db2"):
#     print(el)


def test_filter(s, h):
    print('====== Test filter ======')
    for j in range(len(h)):
        tmp = 0
        for i in range(j+1):
            tmp += h[i] * s[len(s) - 1 - j + i]
        print(tmp)


# http://cs636123.vk.me/v636123054/49d9/wM663kU3vkQ.jpg
def dwt1(x, h):
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
def dwt2(x, h):
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



h = wavelet.dec_lo
# print('========= filter ===========\n', h)
res = dwt1(s, h)
print('========= my dwt1 ===========\n',res)
print('========= my dwt2 ===========\n',dwt2(s, h))


# N = len(s)
# print('========= test ===========')
# print(h[0]*s[0] + h[1]*s[0] + h[2]*s[1] + h[3]*s[2])
# print(h[0]*s[1] + h[1]*s[0] + h[2]*s[0] + h[3]*s[1])
# print(h[0]*s[2] + h[1]*s[1] + h[2]*s[0] + h[3]*s[0])
# print(h[3]*s[N-1] + h[2]*s[N-1] + h[1]*s[N-2] + h[0]*s[N-3])
# print(h[0]*s[0] + h[1]*s[N-1] + h[2]*s[N-2] + h[3]*s[N-3])

# print(h[0]*s[1] + h[1]*s[0] + h[2]*s[N-1] + h[3]*s[N-2])
# print(h[0]*s[0] + h[1]*s[N-1] + h[2]*s[N-2] + h[3]*s[N-3])
# print(h[0]*s[N-1] + h[1]*s[N-2] + h[2]*s[N-3] + h[3]*s[N-4])

