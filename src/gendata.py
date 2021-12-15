from utils import *

import os
print(os.getcwd())

# settings for CO2,CH4,H2,O2,H20
fluids = ["CO2","CH4","H2","O2","H2O", "C12"]
names = ["co2","ch4","h2","o2","h2o", "c12h26"]
datanames = ["L", "C", "D", "H", "S", "A", "U", "V"]
files = ["conductivity", "Cpmass", "Density", "Hmass", "Smass", "A", "Umass", "viscosity"]
T_step = 2
T_lo, T_hi = 275, 550
P_arr = np.array([10]) * 1e6
D_step = 400
for i, fluid in enumerate(fluids):
    Pcrit = CP.PropsSI(fluid, 'pcrit')
    Tcrit = CP.PropsSI(fluid, 'Tcrit')
    a, b = PR(Tcrit, Pcrit)

    # P_arr = np.array([0.5, 1, 1.817, 3, 5, 7.5, 10, 15, 20, 25, 30, 35, 40, 45, 50]) * 1e6
    # P_arr = np.linspace(0.5, 50, 20) * 1e6

    # load omega
    AS = CP.AbstractState("HEOS", fluid)
    omega = AS.acentric_factor()

    print("Critical Properties: \r\nTc: %f \r\nPc: %f" %(Tcrit, Pcrit))
    print("YAML \r\na: %.4e \r\nb: %.4e"%PR(Tcrit, Pcrit, R_u=R*1e6))
    print("acentric-factor:", omega)
    for k, dataname in enumerate(datanames):
        TPD_arr = []
        for P in P_arr:
            TPD_arr += get_data(fluid, P, T_lo, T_hi, T_step, D_step, dataname)
        TPD_arr = np.array(TPD_arr)

        T = TPD_arr[:, 0]
        P = TPD_arr[:, 1]
        D = TPD_arr[:, 2]
        print(T)
        # ===============
        # # show results
        plt.figure()
        plt.plot(T, D, 'gp')

        # plt.figure()
        # plt.plot(T, V, 'p', label=dataname)

        # ===============
        # # save results
        Data = np.zeros(TPD_arr.shape)
        Data[:,0] = T / Tcrit
        Data[:,1] = P / Pcrit
        Data[:,2] = D
        np.savetxt("mech/%s/%s.csv" % (files[k], names[i]), Data, delimiter=', ')

        # only save Temperature
        # Data = np.zeros((len(TPD_arr), 2))
        # Data[:,0] = T / Tcrit
        # Data[:,1] = Alpha
        # np.savetxt("mech/Alpha/%s.csv"%name, Data, delimiter=', ')

plt.show()
