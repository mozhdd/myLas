import numpy as np
from las import LASReader
from matplotlib.pyplot import plot, show
import matplotlib.pyplot as plt
import pywt
import math
# from scipy.signal import cwt
# from scipy.fftpack import fft




myLas = LASReader('las3.las', null_subs=np.nan)
# print(myLas.data)
# print(myLas.start, myLas.stop, myLas.step)

#print(myLas.well.PROV.data, myLas.well.UWI.data)
# plot(myLas.data['DEPT'], myLas.data['GR'])
# plt.ylim(111.5, 112.5)
# plt.xlim(0,100)
# plot(myLas.data['HVOLTA'])

sig = myLas.data['GR'];


#========================================================
cleanedSig = [x for x in sig if math.isnan(x) != True]
plot(cleanedSig)
show()
#
# arr = pywt.wavedec(cleanedSig, 'db1', level=2)
#
# ca = arr[0]
# for i in range(1,7):
#    cd = arr[i]
#    ca = pywt.idwt(ca, cd, 'db1')
#
# print(ca)
#========================================================




# print(len(cA2)+len(cD2)+len(cD1))
# print(len(cleanedSig))




#A, D = pywt.dwt(myLas.data, 'db2')
#print("-------------------------\n", A)
#print(D)

print("\nOk")
