from matplotlib.pyplot import clf, close
from utils import *
import math
plt.ion()
import os
print(os.getcwd())

# settings for CO2
fluids = ["CO2"]
names = ["co2"]
datanames = ["C"]#, "V", "A", "C", "D", "H", "S"
T_lo, T_hi = 250, 1250
T_num = 100
T_arr = np.linspace(np.log(T_lo),np.log(T_hi),T_num)
T_arr = np.exp(T_arr)
# T_step = 5
T_min = 1
P_lo, P_hi = 7.38, 20 
P_num = 20
P_arr = np.linspace(np.log(P_lo),np.log(P_hi),P_num)
P_arr = np.exp(P_arr)*1e6


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
            for T in T_arr:
                TPD_arr.append([T,P,CP.PropsSI(dataname, "T", T, "P", P, fluid)])
            # TPD_arr += get_dataco2(fluid, P, T_lo, T_hi, T_step*P/Pcrit, T_min, dataname)
        TPD_arr = np.array(TPD_arr)
        print(np.shape(TPD_arr))

        T1 = TPD_arr[:, 0]
        P1 = TPD_arr[:, 1]
        D1 = TPD_arr[:, 2]
        
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
        Data[:,0] = T1 / Tcrit
        Data[:,1] = P1 / Pcrit
        Data[:,2] = D1
        np.savetxt("mechco2/%s_%s_2.csv" % (fluid, dataname), Data, delimiter=', ')

plt.pause(1e2)


