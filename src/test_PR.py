from utils import *
from copy import deepcopy

mechs = ['mech/nDodecane_AlphaGP.yaml', 'mech/nDodecane_temp.yaml', 'mech/nDodecane_Reitz.yaml', 'mech/nDodecane_Reitz.yaml']
names = ['nDodecane_PR_ALphaGP', 'nDodecane_PR', 'nDodecane_RK', 'nDodecane_IG']
lines = ['o', 'd', 'v', '.']
colors = ['r', 'b', 'g', 'c']

# ================================================
# settings
# settings for C12
fluid = "C12"
X = {'c12h26':1}
T_step = 3
D_step = 20
T_lo, T_hi = 300, 1000
P_arr = 10*np.array([1]) * 1e6

#settings for o2
fluid = "oxygen"
X = {'o2':1}
T_step = 5
D_step = 20
T_lo, T_hi = 300, 800
P_arr = np.array([10]) * 1e6

gas_arr = []
for k,name in enumerate(names):
    gas = ct.Solution(mechs[k], name)
    gas_arr.append(gas)

# ================================================
# get adaptive TP list and NIST data
TPD_arr = []
for P in P_arr:
    TPD_arr += get_TPD_under_P(fluid, P, T_lo, T_hi, T_step, D_step)
TPD_arr = np.array(TPD_arr)

# ================================================
# the function to compare properties
def compareProperty(TPD_arr, CP_str="D", eval_str="gas.density", unit_convert=1,
                    xlabel="Temperature [K]", ylabel="Density [kg/m^3]", property_name="Density"):
    # get baseline
    gas = gas_arr[1]
    gas.TPX = T_lo, P_arr[0], X
    V0 = CP.PropsSI(CP_str, "T", T_lo, "P", P_arr[0], "PR::"+fluid)*unit_convert - eval(eval_str)
    if abs(V0) <= abs(eval(eval_str))/10:
        V0 = 0
    print("python",V0)

    # get NIST data of variable
    TPV_arr = deepcopy(TPD_arr)
    for i,(T,P,_) in enumerate(TPV_arr):
        TPV_arr[i,2] = CP.PropsSI(CP_str, "T", T, "P", P, fluid)*unit_convert - V0

    # plot NIST result
    fig = plt.figure()
    plt.plot(TPV_arr[:,0], TPV_arr[:,2], 'ks', label="NIST", fillstyle='none')

    # get & plot Cantera's result
    for k,name in enumerate(names):
        gas = gas_arr[k]
        TPV_calc = deepcopy(TPV_arr)
        t0 = time.time()
        
        for i,(T,P,_) in enumerate(TPV_calc):
            gas.TPX = T, P, X
            TPV_calc[i,2] = eval(eval_str)

            # if name == "nDodecane_PR_ALphaGP" and CP_str == "Umolar":
                # print(gas.enthalpy_mole, gas.P, gas.density)
        
        print("%s cost of %-20s = %.5f s"%(property_name, name, time.time()-t0))
        plt.plot(TPV_calc[:,0], TPV_calc[:,2], colors[k]+lines[k], label=name, alpha=0.8, fillstyle='none')
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    # model 2
    # plt.savefig("figs/PRAlphaGP_%s_%s.png"%(fluid, property_name))
    # model 3
    plt.savefig("figs/model3_%s_%s.png"%(fluid, property_name))

# ================================================
# Density
compareProperty(TPD_arr, CP_str="D", eval_str="gas.density", unit_convert=1,
                xlabel="Temperature [K]", ylabel="Density [kg/m^3]", property_name="Density")

# ================================================
# Cp_mole
compareProperty(TPD_arr, CP_str="Cpmolar", eval_str="gas.cp_mole", unit_convert=1000,
                xlabel="Temperature [K]", ylabel="Cp_mole [J/kmol/K]", property_name="Cp_mole")

# ================================================
# intenergy_mole
compareProperty(TPD_arr, CP_str="Umolar", eval_str="gas.int_energy_mole", unit_convert=1000,
                xlabel="Temperature [K]", ylabel="Intenergy [J/kmol]", property_name="Intenergy")

# ================================================
# entropy_mass
compareProperty(TPD_arr, CP_str="S", eval_str="gas.entropy_mass", unit_convert=1,
                xlabel="Temperature [K]", ylabel="Entropy_mass [J/kmol/K]", property_name="Entropy_mass")
                
# ================================================
# cp_mass
compareProperty(TPD_arr, CP_str="C", eval_str="gas.cp_mass", unit_convert=1,
                xlabel="Temperature [K]", ylabel="cp_mass [J/kmol/K]", property_name="cp_mass")
# ================================================
# cv_mole
compareProperty(TPD_arr, CP_str="Cvmolar", eval_str="gas.cv_mole", unit_convert=1000,
                xlabel="Temperature [K]", ylabel="cv_mole [J/kmol/K]", property_name="cv_mole")
            
# Enthalpy_mass
compareProperty(TPD_arr, CP_str="H", eval_str="gas.enthalpy_mass", unit_convert=1,
                xlabel="Temperature [K]", ylabel="Enthalpy_mass [J/kg]", property_name="enthalpy_mass")

# Enthalpy_mole
compareProperty(TPD_arr, CP_str="Hmolar", eval_str="gas.enthalpy_mole", unit_convert=1000,
                xlabel="Temperature [K]", ylabel="Enthalpy_mole [J/kmol]", property_name="enthalpy_mole")
                
# # Soundspeed
# compareProperty(TPD_arr, CP_str="A", eval_str="equilSoundSpeeds(gas)[1]", unit_convert=1,
#                  xlabel="Temperature [K]", ylabel="Soundspeed [m/s]", property_name="Soundspeed")

plt.show()
