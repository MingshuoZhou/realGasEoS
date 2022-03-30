from matplotlib.pyplot import clf, close
from utils import *
import math
plt.ion()
import os
print(os.getcwd())

# settings for decane[0.78]&CYCLOHEX[0.098]&toluene[0.122]
CP.apply_simple_mixing_rule('decane', 'toluene', 'linear')
dataname = "D"#, "V", "A", "C", "D", "H", "S"
T_lo, T_hi = 300,800
P_arr = np.array([3,4,5,6,8,10,12,15,18,20]) * 1e6 #, 10, 15, 20
X_i = np.linspace(0,1,10)
TPD_arr = []

for i, x_i in enumerate(X_i):

    fluid = "decane[%f]&toluene[%f]" % (x_i,1-x_i)
    names = {'nc10h22':x_i, 'C6H5CH3':1-x_i}
    Pcrit = CP.PropsSI(fluid, 'pcrit')
    Tcrit = CP.PropsSI(fluid, 'Tcrit')
    a, b = PR(Tcrit, Pcrit)
    print(Tcrit, Pcrit)

    # load omega
    for P in P_arr:
        if P == 2*1e6 or P==3*1e6:
            T_step = 2
            T_min = 0.3
        else:
            T_step = 5
            T_min = 0.5
        TPD_arr += get_dataptx(fluid, P, x_i, T_lo, T_hi, T_step, T_min, dataname)
        # print(P)

TPD_arr = np.array(TPD_arr)

T1 = TPD_arr[:, 0]
P1 = TPD_arr[:, 1]
D1 = TPD_arr[:, 2]
X1 = TPD_arr[:,3]
# ===============
# # save results
plt.figure()
plt.plot(T1, D1, 'gp')
plt.xlabel("T")
plt.ylabel(dataname)
plt.title(fluid)
plt.draw()
# plt.savefig("figs/data/%s_%s.png" % (names[i], dataname))
# # model 2
# Data = np.zeros((len(TPD_arr), 2))
# Data[:,0] = T1 / Tcrit
# Data[:,1] = D1
# np.savetxt("mechco2/%s_%s.csv" % (Pname, dataname), Data, delimiter=', ')
# model 3
Data = np.zeros(TPD_arr.shape)
Data[:,0] = T1
Data[:,1] = P1/1e6
Data[:,2] = X1
Data[:,3] = D1
np.savetxt("mech/ptx.csv", Data, delimiter=', ')

plt.pause(1e2)


