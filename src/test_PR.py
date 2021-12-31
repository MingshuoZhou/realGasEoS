from numpy.lib.npyio import loadtxt, savetxt
from utils import *
from copy import deepcopy
import os
plt.ion()

# mechs = ['mech2/nDodecane_AlphaGP.yaml', 'mech2/nDodecane_temp.yaml', 'mech2/nDodecane_Reitz.yaml', 'mech2/nDodecane_Reitz.yaml']
# names = ['nDodecane_PR_ALphaGP', 'nDodecane_PR', 'nDodecane_RK', 'nDodecane_IG']
mechs = [ 'binarymech/nDodecane_AlphaGP.yaml', 'binarymech/nDodecane_temp.yaml', 'binarymech/nDodecane_Reitz.yaml']
names = [ 'nDodecane_PR_ALphaGP', 'nDodecane_PR',  'nDodecane_IG']
lines = ['o', 'd', 'v', '.']
colors = ['r', 'b', 'g', 'c']
nist = np.loadtxt('binarymech/nist.csv', delimiter=',')
# ================================================
# settings
# settings for C12
# CP.apply_simple_mixing_rule('decane', 'CYCLOHEX', 'linear')
# CP.apply_simple_mixing_rule('decane', 'toluene', 'linear')
# CP.apply_simple_mixing_rule('CYCLOHEX', 'toluene', 'linear')
CP.apply_simple_mixing_rule('decane','O2', 'linear')
fluid = "co2[0.5]&water[0.5]"
X = {'co2':0.5, 'h2o':0.5}
# fluid = "decane[0.78]&CYCLOHEX[0.098]&toluene[0.122]"
# X = {'nc10h22':0.78, 'c6h12':0.098, 'C6H5CH3':0.122}
T_step = 3
D_step = 20
T_lo, T_hi = 700, 1500
P_arr = 30*np.array([1]) * 1e6

#settings for o2
# fluid = "oxygen"
# X = {'o2':1}
# T_step = 5
# D_step = 20
# T_lo, T_hi = 300, 800
# P_arr = np.array([10]) * 1e6

gas_arr = []
for k,name in enumerate(names):
    gas = ct.Solution(mechs[k], name)
    gas_arr.append(gas)

# ================================================
# get adaptive TP list and NIST data
TPD_arr = []
for P in P_arr:
    TPD_arr += get_uniform_TPD_under_P(fluid, P, T_lo, T_hi, T_step, D_step)
    # TPD_arr += get_TPD_under_P(fluid, P, T_lo, T_hi, T_step, D_step)

TPD_arr = np.array(TPD_arr)

# ================================================
# the function to compare properties
def compareProperty(TPD_arr, CP_str="D", eval_str="gas.density", unit_convert=1,
                    xlabel="Temperature [K]", ylabel="Density [kg/m^3]", property_name="Density", k=3):
    # get baseline
    gas = gas_arr[1]
    T_mi = (T_hi + T_lo) / 2
    gas.TPX = T_mi, P_arr[0], X
    try:
        V0 = CP.PropsSI(CP_str, "T", T_mi, "P", P_arr[0], "PR::"+fluid)*unit_convert - eval(eval_str)
    except:
        print("ERROR::V0 failed")
        V0 = 0
    print( "V0_ratio=", abs(V0) / abs(eval(eval_str)))
    if abs(V0) <= abs(eval(eval_str))*1e-2:
        V0 = 0
    print("V0 =",V0)

    # # get NIST data of variable
    TPV_arr = deepcopy(TPD_arr)
    for i,(T,P,_) in enumerate(TPV_arr):
        try:
            TPV_arr[i,2] = CP.PropsSI(CP_str, "T", T, "P", P, fluid)*unit_convert  - V0
        except:
            TPV_arr[i,2] = np.nan

    # # plot NIST result
    fig = plt.figure()
    # plt.plot(TPV_arr[:,0], TPV_arr[:,2], 'ks', label="NIST", fillstyle='none')
    plt.plot(nist[:,0], nist[:,k-1]*unit_convert, 'ks', label="NIST", fillstyle='none')

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
    plt.title(fluid)
    plt.legend()
    plt.draw()
    plt.pause(1e-6)

    # model 2
    # plt.savefig("figs/simu/PRAlphaGP_%s_%s.png"%(fluid, property_name))
    # savetxt("mech2/data/%s.csv" % CP_str, TPV_calc, delimiter=', ')
    # model 3
    # plt.savefig("figs/model3_%s_%s.png"%(fluid, property_name))
    # mixture
    # plt.savefig("figs/mixture/PRAlphaGP_%s_%s.png"%(fluid, property_name))

# ================================================
# # Density
compareProperty(TPD_arr, CP_str="D", eval_str="gas.density", unit_convert=1,
                xlabel="Temperature [K]", ylabel="Density [kg/m^3]", property_name="Density", k=3)

# ================================================
# # Cp_mole
compareProperty(TPD_arr, CP_str="Cpmolar", eval_str="gas.cp_mole", unit_convert=1000,
                xlabel="Temperature [K]", ylabel="Cp_mole [J/kmol/K]", property_name="Cp_mole", k=4)

# ================================================
# intenergy_mass
compareProperty(TPD_arr, CP_str="U", eval_str="gas.int_energy_mass", unit_convert=1000,
                xlabel="Temperature [K]", ylabel="Intenergy [J/kg]", property_name="Intenergy", k=4)

# ================================================
# Enthalpy_mass
compareProperty(TPD_arr, CP_str="H", eval_str="gas.enthalpy_mass", unit_convert=1000,
                xlabel="Temperature [K]", ylabel="Enthalpy_mass [J/kg]", property_name="enthalpy_mass", k=5)
# ================================================

# entropy_mass
compareProperty(TPD_arr, CP_str="S", eval_str="gas.entropy_mass", unit_convert=1000,
                xlabel="Temperature [K]", ylabel="Entropy_mass [J/kmol/K]", property_name="Entropy_mass", k=6)

# ================================================
# cv_mass
compareProperty(TPD_arr, CP_str="Cv", eval_str="gas.cv_mass", unit_convert=1000,
                xlabel="Temperature [K]", ylabel="cv_mass [J/kg/K]", property_name="cv_mass", k=7)

# ================================================
# cp_mass
compareProperty(TPD_arr, CP_str="C", eval_str="gas.cp_mass", unit_convert=1000,
                xlabel="Temperature [K]", ylabel="cp_mass [J/kg/K]", property_name="cp_mass", k=8)
# ================================================

# # Enthalpy_mole
# compareProperty(TPD_arr, CP_str="Hmolar", eval_str="gas.enthalpy_mole", unit_convert=1000,
#                 xlabel="Temperature [K]", ylabel="Enthalpy_mole [J/kmol]", property_name="enthalpy_mole")
                
# # Soundspeed
# compareProperty(TPD_arr, CP_str="A", eval_str="equilSoundSpeeds(gas)", unit_convert=1,
#                  xlabel="Temperature [K]", ylabel="Soundspeed [m/s]", property_name="Soundspeed")

plt.pause(1e2)