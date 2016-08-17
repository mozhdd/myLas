from numpy import *
from pylab import *
import pylab
from numpy.polynomial.legendre import *
import lasio
import math
import os
import statistics as st
import scipy.stats as stats


def expLegendre():
    L_deg = 3

    x = arange(-1., 1.0, .2)
    y = exp(x)
    c = legfit(x, y, L_deg)
    p = legval(x, c)   #polynomial value

    plot(x, y, 'b', label='func')
    plot(x, p, 'r', label='legendre')
    legend()
    show()
    # ----------------------------------


def nan_interp(y):
    def nan_helper(y):
        """Helper to handle indices and logical indices of NaNs.

        Input:
            - y, 1d numpy array with possible NaNs
        Output:
            - nans, logical indices of NaNs
            - index, a function, with signature indices= index(logical_indices),
              to convert logical indices of NaNs to 'equivalent' indices
        Example:
            >>> # linear interpolation of NaNs
            >>> nans, x = nan_helper(y)
            >>> y[nans] = np.interp(x(nans), x(~nans), y[~nans])
        """

        return np.isnan(y), lambda z: z.nonzero()[0]

    nans, x = nan_helper(y)
    y[nans] = np.interp(x(nans), x(~nans), y[~nans])
    return y
    # ----------------------------------------------------------


def readLAS():
    l = lasio.read("las.las")   # reading las
    print(l.keys())
    res = [l[i] for i in range(1, len(l.keys()))]   # move data to array (except depth)
    res = list(map(lambda x: nan_interp(x), res))   # interpolating all nan
    return [l[0], res]
    # ----------------------------------------------------------


def plotLAS(las):
    x = linspace(-1, 1, len(las[0]))
    for i in range(len(las)):
        plot(x, las[i], label=str(i))
    legend()
    grid()
    show()
    # -------------------------------


def read_lases_from_dir(dir_name):
    files = os.listdir(dir_name)
    tmp = []
    for f in files:
        try:
            l = lasio.read(os.path.join(dir_name + '/' + f))
            if not (l['GR'] is None):
                tmp.append(nan_interp(np.array(l['GR'])))  # interpolating all nan from GR
        except Exception:
            raise
    return tmp


# las - list
# las[i] - ndarray
def crop_las(las):
    N = min([el.size for el in las])                # length of the shortest las
    las = [np.resize(el, (1, N))[0] for el in las]  # cropping lases witg min len from first element
    return las


# normal distribution of sample
# plot histogram and normal distributeg curve
def NormDistrib(arr, bins):

    bins = 12

    mu = st.mean(arr)
    D = st.pvariance(arr)

    arr = sorted(arr)
    fit = stats.norm.pdf(arr, mu, sqrt(D))

    t1, t2, t3 = hist(arr, bins, normed=True, label='mu = ' + str(mu))
    plot(arr, fit, 'r', lw=3, label='variance = ' + str(D))
    legend()

    print(t1)
    print(t2)

    show()



#
# =================================== main =====================================
#
#
# las = read_lases_from_dir('C:/Users/Евгений/Desktop/GazpromNeft/tmp')
# las = crop_las(las)

# x = linspace(-1, 1, len(las[0]))
# c = []
# # разложение многочленами Лежандра
# for el in las:
#     c.append(legfit(x, el, 20))




# importing data (las and Legendre coefs from files)
import data_pickle
var1 = data_pickle.variable('las.pickle')
las = var1.import_variable()
var2 = data_pickle.variable('LegCoefs.pickle')
c = var2.import_variable()



# plotting histogram from zerro-coefs
arr = np.array([el[0] for el in c])
# NormDistrib(arr, 19)


# arr = [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,
#        0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,4,
#        4,4,4,4,5,5,5,6,6,6,7,7,8,9,10,11,
#        16,16,16,16,16,16,16,16,16,16,16,16,16,17,17,17,17,18,18,
#        19,19,19,20,20,20,21,22,22,23,25,27]
# NormDistrib(arr, 30)

# arr = [-1, 0, 1, 2, 3, 5, 6, 7, 10, 15]
# NormDistrib(arr, 8)



f, axarr = plt.subplots(3, sharex=True)

# Q-Q plots
(osm, osr) = stats.probplot(arr, dist="norm", plot=axarr[0])
# show()

x = osm[0]
y = osm[1]
# least squares regression line
a ,b = np.polyfit(x, y, 1)

axarr[1].plot(x, y, '.')
axarr[1].plot(x, a*x + b, '-')
axarr[0].set_title('Q-Q - plot')
axarr[1].set_title('least squares regression line')




x = stats.shapiro(arr)
print(x)
# x[0] - W
# x[1] - F(z) - Вероятность стандартного нормального распределения соответствующей квантили

# arr = [0.2, 0.33, 0.445, 0.49, 0.78, 0.92, 0.95, 0.97, 1.04, 1.71, 2.22, 2.275,
#        3.65, 7, 8.8]
arr = np.array(sorted(arr))
n = arr.size
k = range(1, n+1)
p = [(el_k-3/8)/(n+1/4) for el_k in k]

print(len(arr))
print(len(p))
axarr[2].plot(arr, p, '.')
axarr[2].set_title('my qq')
a ,b = np.polyfit(arr, p, 1)
axarr[2].plot(arr, a*arr + b, '-')

grid()
show()