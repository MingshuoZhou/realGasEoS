from matplotlib.pyplot import clf, close
from utils import *

import os
print(os.getcwd())

# settings for CO2,CH4,H2,O2,H20
fluids = ["CO2","CH4", "C12","O2","H2O"]
names = ["co2","ch4", "c12h26", "o2","h2o"]
datanames = ["C", "D", "H", "Hmolar", "S", "Smolar", "U", "Umolar", "Cpmolar", "Cvmolar"]
files = ["Cpmass", "Density", "Hmass", "Hmole", "Smass", "Smole", "Umass", "Umole", "Cpmole", "Cvmole"]
steps = [500, 50, 20000, 10000000, 100, 100000, 20000, 10000000,  500000, 10000]*2
eval_strs = ["gas.cp_mass", "gas.density", "gas.enthalpy_mass", "gas.enthalpy_mole", "gas.entropy_mass", "gas.entropy_mole", "gas.int_energy_mass", "gas.int_energy_mole", "gas.cp_mole", "gas.cv_mole"]
unit_converts = [1, 1, 1, 1000, 1, 1000, 1, 1000, 1000, 1000]
T_step = 5
T_lo, T_hi = 300, 1000
# model 2
# P_arr = np.array([10]) * 1e6
# model 3
P_arr = np.array([9.5, 10, 10.5]) * 1e6

def baseline(fluid, CP_str, eval_str,  unit_convert):
    gas = ct.Solution('mech2/nDodecane_temp.yaml','nDodecane_PR')
    gas.TPX = T_lo, P_arr[0], X
    V0 = CP.PropsSI(CP_str,"T",T_lo,"P",P_arr[0],"PR::"+fluid)*unit_convert - eval(eval_str)
    if abs(V0) <= abs(eval(eval_str)/10) :
        V0=0
    return V0

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
            TPD_arr += get_data(fluid, P, T_lo, T_hi, T_step, steps[k], dataname, unit_converts[k])
        TPD_arr = np.array(TPD_arr)

        T = TPD_arr[:, 0]
        P = TPD_arr[:, 1]
        D = TPD_arr[:, 2] - baseline(fluid, dataname, eval_strs[k], unit_converts[k])

        # ===============
        # # save results
        plt.figure()
        plt.plot(T, D, 'gp')
        plt.xlabel("T")
        plt.ylabel(files[k])
        plt.title(fluid)
        # # model 2
        # Data = np.zeros((len(TPD_arr), 2))
        # Data[:,0] = T / Tcrit
        # Data[:,1] = D
        # np.savetxt("mech2/%s/%s.csv" % (files[k], names[i]), Data, delimiter=', ')
        # model 3
        Data = np.zeros(TPD_arr.shape)
        Data[:,0] = T / Tcrit
        Data[:,1] = P / Pcrit
        Data[:,2] = D
        np.savetxt("mech/%s/%s.csv" % (files[k], names[i]), Data, delimiter=', ')

# plt.show()


