from matplotlib.pyplot import plot, show
import matplotlib.pyplot as plt
import pywt
from math import sqrt

def readArr():
    f = open("GR1.txt", "r")
    arr = []

    while(True):
        line = f.readline()
        if(line == ""):
            break
        line = line.strip()
        arr.append(float(line))
    f.close()
    return arr

def WeveTransform(lattice, wave):


    # arr = pywt.dwt(wave, "db1")
    # f, axarr = plt.subplots(2, sharex=True)
    # axarr[0].plot(arr[0])
    # axarr[1].plot(arr[1])
    # show()

    # arr = pywt.wavedec(wave, 'db1', level=5)
    # f, axarr = plt.subplots(5, sharex=True)
    # for i in range(0, len(arr)-1):
    #     axarr[i].set_title("a"+str(len(arr)-i-2))
    #     axarr[i].plot(arr[i])
    #     plt.xlim(0, len(arr[i]))

    arr = pywt.wavedec(wave, 'db1', level=5)
    axarr = []

    axarr.append(plt.subplot(210))
    axarr[0].plot(wave)
    axarr[0].set_xlim(0, len(wave)-1)

    i=1
    axarr.append(plt.subplot(210+i))
    axarr[1].plot(arr[0])
    axarr[1].set_xlim(0, len(arr[0])-1)

    # графики накладываются др на друга
    i+=1
    axarr.append(plt.subplot(210+i))
    axarr[1].plot(arr[4])
    axarr[1].set_xlim(0, len(arr[4])-1)

    # i+=1
    # axarr.append(plt.subplot(212))
    # axarr[2].plot(arr[3])
    # axarr[2].set_xlim(0, len(arr[3])-1)

    # rg = range(0, 2)
    # for i in rg: #range(0, len(arr)-1):
    #     axarr.append(plt.subplot(210+i))
    #     axarr[i].plot(arr[i])
    #     axarr[i].set_xlim(0, len(arr[i])-1)


    show()
    return arr[0]


def myTransform(SourceList):
    if len(SourceList) == 1:
        return SourceList

    RetVal = []
    TmpArr = []

    for j in range(0, len(SourceList)-1, 2):
        RetVal.append((SourceList[j] - SourceList[j + 1]) / 2.0)
        TmpArr.append((SourceList[j] + SourceList[j + 1]) / 2.0)

    # RetVal.AddRange(DirectTransform(TmpArr))
    RetVal.extend(myTransform(TmpArr))
    return RetVal


wave = readArr()







signal = [2,4,6,7,8,7,6,4,1,0.5,3,9,5,2]


cA = []
cD = []

# ============================================================================================
def InverseHaar(wave):
    tmp = []
    tmp.append(wave[0]) #saving cA to tmp[0]
    for i in range(1, len(wave)): # looping all cD coefs
        tmp.append([])
        for j in range(len(wave[i])):
            tmp[i].append((tmp[i-1][j] + wave[i][j])/sqrt(2))
            tmp[i].append((tmp[i-1][j] - wave[i][j])/sqrt(2))
        if i < len(wave):  #delete last repeted argument
            if((len(wave[i-1]) % 2) != 0  and wave[i][len(wave[i])-1] == 0):
                del tmp[i][len(tmp[i]) - 1]
        # if i + 1 < len(wave):  #delete last repeted argument
        #     if((len(wave[i+1]) % 2) != 0  and wave[i][len(wave[i])-1] == 0):
        #         del tmp[i][len(tmp[i]) - 1]
    return tmp[len(tmp)-1]
# ============================================================================================
def Haar(wave):
    tmp = []
    d = []
    tmp.append(wave)
    # for i in range(len(tmp[i])):
    i = 0
    while(len(tmp[i]) >= 4):
        tmp.append([])
        d.append(([]))
        for j in range(0, len(tmp[i]), 2):
            if len(tmp[i]) % 2 !=0 and j >= (len(tmp[i])-1):
                tmp[i+1].append(tmp[i][j]*sqrt(2))
                d[i].append(0)
                continue
            tmp[i+1].append(sqrt(2)*(tmp[i][j] + tmp[i][j+1])/2)
            d[i].append(sqrt(2)*(tmp[i][j] - tmp[i][j+1])/2)
        i += 1

    # del tmp[0]
    return ([tmp[len(tmp)-1]] + [el for el in reversed(d)])
# ============================================================================================


# for i in range(0, len(signal), 2):
#     cA.append((signal[i] + signal[i+1])/2)
#     cD.append(signal[i] - cA[(int)(i/2)])
#     cD.append(signal[i+1] - cA[(int)(i/2)] )


# # axarr[0].bar(range(0, len(cD)), cD, 1)
# # axarr[1].bar(range(0, len(cA)), cA, 1)
# axarr[0].plot(cA)
# axarr[0].plot(cD, 'red')
#
#
# arr = pywt.wavedec(signal, 'haar')
# axarr[1].plot(arr[0])
# plot(arr[1])
# plot(arr[2])
# plot(arr[3])
# # show()


cA,cD = pywt.dwt(signal, 'haar')

res = Haar(signal)

# f, axarr = plt.subplots(3, sharex=True)
# axarr[0].bar(range(0, len(res[1])), res[1], 1)
# axarr[1].bar(range(0, len(res[2])), res[2], 1)
# axarr[2].bar(range(0, len(res[3])), res[3], 1)
# show()
print(res[0],'\n', res[1],'\n', res[2],'\n', res[3])
print("-------------------------------------------------------------------------------------")
print(pywt.wavedec(signal, 'haar'))

res2 = InverseHaar(res)

print("========= signal ==========")
print(list(map(lambda x: round(x), res2)))
print(signal)
