from matplotlib.pyplot import clf, close
from utils import *
plt.ion()
import os
print(os.getcwd())

# settings for CO2
fluids = ["CO2"]
names = ["co2"]
datanames = ["L", "V", "A", "C", "D", "H", "S"]#, "V", "A", "C", "D", "H", "S"
T_lo, T_hi = 250, 1250
# model 2
P_arr = np.array([7.38]) * 1e6 #, 10, 15, 20

for i, fluid in enumerate(fluids):

    Pcrit = CP.PropsSI(fluid, 'pcrit')
    Tcrit = CP.PropsSI(fluid, 'Tcrit')
    a, b = PR(Tcrit, Pcrit)
    X={names[i]:1}

    # load omega
    AS = CP.AbstractState("HEOS", fluid)
    omega = AS.acentric_factor()

    print("Critical Properties: \r\nTc: %f \r\nPc: %f" %(Tcrit, Pcrit))
    print("YAML \r\na: %.4e \r\nb: %.4e"%PR(Tcrit, Pcrit, R_u=R*1e6))
    print("acentric-factor:", omega)
    for k, dataname in enumerate(datanames):
        TPD_arr = []
        for P in P_arr:
            if P == 7.38*1e6 or P == 10*1e6:
                T_step = 3
                T_min = 0.5
                T_lo, T_hi = 250, 1250
            else:
                T_step = 8
                T_min = 0.8
            TPD_arr = get_dataco2(fluid, P, T_lo, T_hi, T_step, T_min, dataname)
            TPD_arr = np.array(TPD_arr)

            Pname = str(math.floor(P/1e6))

            T1 = TPD_arr[:, 0]
            P1 = TPD_arr[:, 1]
            D1 = TPD_arr[:, 2]

            # ===============
            # # save results
            plt.figure()
            plt.plot(T1, D1, 'gp')
            plt.xlabel("T")
            plt.ylabel(dataname)
            plt.legend(Pname)
            plt.title(fluid)
            plt.draw()
            # plt.savefig("figs/data/%s_%s.png" % (names[i], dataname))
            # # model 2
            Data = np.zeros((len(TPD_arr), 2))
            Data[:,0] = T1 / Tcrit
            Data[:,1] = D1
            np.savetxt("mechco2/%s_%s.csv" % (Pname, dataname), Data, delimiter=', ')
            # model 3
            # Data = np.zeros(TPD_arr.shape)
            # Data[:,0] = T / Tcrit
            # Data[:,1] = P / Pcrit
            # Data[:,2] = D
            # np.savetxt("mech/%s/%s.csv" % (files[k], names[i]), Data, delimiter=', ')

plt.pause(1e2)


