from utils import *
from copy import deepcopy

mechs = ['mech/nDodecane_AlphaGP.yaml', 'mech/nDodecane_temp.yaml', 'mech/nDodecane_Reitz.yaml', 'mech/nDodecane_Reitz.yaml']
names = ['nDodecane_PR_ALphaGP', 'nDodecane_PR', 'nDodecane_RK', 'nDodecane_IG']
lines = ['o', 'd', 'v', '.']
colors = ['r', 'b', 'g', 'c']

# ================================================
# settings

#settings for C12
# fluid = "C12"
# X = {'c12h26':1}
# T_step = 3
# D_step = 20
# T_lo, T_hi = 275, 800
# P_arr = 10*np.array([1]) * 1e6

#settings for o2
fluid = "oxygen"
X = {'o2':1}
T_step = 5
D_step = 20
T_lo, T_hi = 300, 800
P_arr = np.array([10]) * 1e6

# ================================================
# get adaptive TP list and NIST data
TPD_arr = []
for P in P_arr:
    TPD_arr += get_TPD_under_P(fluid, P, T_lo, T_hi, T_step, D_step)
TPD_arr = np.array(TPD_arr)

# ================================================
# Density
fig = plt.figure()
plt.plot(TPD_arr[:,0], TPD_arr[:,2], 'ks', label="NIST", fillstyle='none')

Tc = CP.PropsSI(fluid, 'Tcrit')
Pc = CP.PropsSI(fluid, 'pcrit')
T, P = 0.7*Tc, 2*Pc
gas = ct.Solution('mech/nDodecane_AlphaGP.yaml', 'nDodecane_PR_ALphaGP')
gas.TP = T, P
print("True D:", CP.PropsSI("D", "T", T, "P", P, fluid))
print("Density:", gas.density)

for k,name in enumerate(names):
    gas = ct.Solution(mechs[k], name)
    TPD_calc = deepcopy(TPD_arr)

    t0 = time.time()
    for i,(T,P,_) in enumerate(TPD_calc):
        gas.TPX = T, P, X
        TPD_calc[i,2] = gas.density
    print("Density cost of %-20s = %.5f s"%(name, time.time()-t0))
    plt.plot(TPD_calc[:,0], TPD_calc[:,2], colors[k]+lines[k], label=name, alpha=0.8, fillstyle='none')
plt.xlabel("Temperature [K]")
plt.ylabel("Density [kg/m^3]")
plt.legend()
plt.savefig("figs/PRAlphaGP_%s_Density.png"%fluid)

# # ================================================
# # Cp_mole
TPV_arr = deepcopy(TPD_arr)
for i,(T,P,_) in enumerate(TPD_calc):
    TPV_arr[i,2] = CP.PropsSI("Cpmolar", "T", T, "P", P, fluid)*1000

fig = plt.figure()
plt.plot(TPV_arr[:,0], TPV_arr[:,2], 'ks', label="NIST", fillstyle='none')

for k,name in enumerate(names):
    gas = ct.Solution(mechs[k], name)
    TPV_calc = deepcopy(TPV_arr)

    t0 = time.time()
    for i,(T,P,_) in enumerate(TPD_calc):
        gas.TPX = T, P, X
        TPV_calc[i,2] = gas.cp_mole
    print("Cp_mass cost of %-20s = %.5f s"%(name, time.time()-t0))
    plt.plot(TPV_calc[:,0], TPV_calc[:,2], colors[k]+lines[k], label=name, alpha=0.8, fillstyle='none')

# plt.ylim([0,30000])
plt.xlabel("Temperature [K]")
plt.ylabel("Cp_mole [J/kg/K]")
plt.legend()
plt.savefig("figs/PRAlphaGP_%s_Cp_mole.png"%fluid)
#
# # Cp_mass
TPV_arr = deepcopy(TPD_arr)
for i,(T,P,_) in enumerate(TPD_calc):
    TPV_arr[i,2] = CP.PropsSI("C", "T", T, "P", P, fluid)

fig = plt.figure()
plt.plot(TPV_arr[:,0], TPV_arr[:,2], 'ks', label="NIST", fillstyle='none')

for k,name in enumerate(names):
    gas = ct.Solution(mechs[k], name)
    TPV_calc = deepcopy(TPV_arr)

    t0 = time.time()
    for i,(T,P,_) in enumerate(TPD_calc):
        gas.TPX = T, P, X
        TPV_calc[i,2] = gas.cp_mass
    print("Cp_mass cost of %-20s = %.5f s"%(name, time.time()-t0))
    plt.plot(TPV_calc[:,0], TPV_calc[:,2], colors[k]+lines[k], label=name, alpha=0.8, fillstyle='none')

# plt.ylim([0,30000])
plt.xlabel("Temperature [K]")
plt.ylabel("Cp_mass [J/kg/K]")
plt.legend()
plt.savefig("figs/PRAlphaGP_%s_Cp_mass.png"%fluid)
#
# # ================================================
# Enthalpy
TPV_arr = deepcopy(TPD_arr)
for i,(T,P,_) in enumerate(TPD_calc):
    TPV_arr[i,2] = CP.PropsSI("H", "T", T, "P", P, fluid)

fig = plt.figure()
plt.plot(TPV_arr[:,0], TPV_arr[:,2], 'ks', label="NIST", fillstyle='none')

for k,name in enumerate(names):
    gas = ct.Solution(mechs[k], name)
    TPV_calc = deepcopy(TPV_arr)

    t0 = time.time()
    for i,(T,P,_) in enumerate(TPD_calc):
        gas.TPX = T, P, X
        TPV_calc[i,2] = gas.enthalpy_mass
    print("Enthalpy cost of %-20s = %.5f s"%(name, time.time()-t0))
    plt.plot(TPV_calc[:,0], TPV_calc[:,2], colors[k]+lines[k], label=name, alpha=0.8, fillstyle='none')
plt.xlabel("Temperature [K]")
plt.ylabel("Enthapy [J/kg]")
plt.legend()
plt.savefig("figs/PRAlphaGP_%s_Enthapy.png"%fluid)

# # ================================================
# Entropy
TPV_arr = deepcopy(TPD_arr)
for i,(T,P,_) in enumerate(TPD_calc):
    TPV_arr[i,2] = CP.PropsSI("S", "T", T, "P", P, fluid)

fig = plt.figure()
plt.plot(TPV_arr[:,0], TPV_arr[:,2], 'ks', label="NIST", fillstyle='none')

for k,name in enumerate(names):
    gas = ct.Solution(mechs[k], name)
    TPV_calc = deepcopy(TPV_arr)

    t0 = time.time()
    for i,(T,P,_) in enumerate(TPD_calc):
        gas.TPX = T, P, X
        TPV_calc[i,2] = gas.entropy_mass
    print("Enthalpy cost of %-20s = %.5f s"%(name, time.time()-t0))
    plt.plot(TPV_calc[:,0], TPV_calc[:,2], colors[k]+lines[k], label=name, alpha=0.8, fillstyle='none')
plt.xlabel("Temperature [K]")
plt.ylabel("Enthapy [J/kg]")
plt.legend()
plt.savefig("figs/PRAlphaGP_%s_Enthapy.png"%fluid)
# # ================================================
# # intenergy
TPV_arr = deepcopy(TPD_arr)
for i,(T,P,_) in enumerate(TPD_calc):
    TPV_arr[i,2] = CP.PropsSI("Umolar", "T", T, "P", P, fluid)*1000

fig = plt.figure()
plt.plot(TPV_arr[:,0], TPV_arr[:,2], 'ks', label="NIST", fillstyle='none')

for k,name in enumerate(names):
    gas = ct.Solution(mechs[k], name)
    TPV_calc = deepcopy(TPV_arr)

    t0 = time.time()
    for i,(T,P,_) in enumerate(TPD_calc):
        gas.TPX = T, P, X
        TPV_calc[i,2] = gas.int_energy_mole
    print("Intenergy cost of %-20s = %.5f s"%(name, time.time()-t0))
    plt.plot(TPV_calc[:,0], TPV_calc[:,2], colors[k]+lines[k], label=name, alpha=0.8, fillstyle='none')
plt.xlabel("Temperature [K]")
plt.ylabel("Intenergy [J/kg]")
plt.legend()
plt.savefig("figs/PRAlphaGP_%s_Intenergy.png"%fluid)


plt.show()
