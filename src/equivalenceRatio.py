"""
This example demonstrates how to set a mixture according to equivalence ratio
and mixture fraction.

Requires: cantera >= 2.5.0
"""

import cantera as ct
import matplotlib.pyplot as plt
import numpy as np
import CoolProp.CoolProp as CP
import math

gas = ct.Solution('mech2/nDodecane_AlphaGP.yaml','nDodecane_PR_ALphaGP')
gas_o = ct.Solution('mech2/nDodecane_AlphaGP.yaml','nDodecane_PR_ALphaGP')
gas_f = ct.Solution('mech2/nDodecane_AlphaGP.yaml','nDodecane_PR_ALphaGP')

# fuel and oxidizer compositions
fuel = "nc10h22:0.780, c6h12:0.098, C6H5CH3:0.122"
oxidizer = "o2:1"

gas_o.TPX = 100, 6000000, oxidizer
gas_f.TPX = 300, 6000000, fuel
n = 200
Z = np.zeros(n)
steps = np.linspace(1, 100, 200)
density = np.zeros(n)
densityCP = np.zeros(n)
CP.apply_simple_mixing_rule('decane', 'CYCLOHEX', 'linear')
CP.apply_simple_mixing_rule('decane', 'toluene', 'linear')
CP.apply_simple_mixing_rule('CYCLOHEX', 'toluene', 'linear')
CP.apply_simple_mixing_rule('CYCLOHEX', 'oxygen', 'linear')
CP.apply_simple_mixing_rule('decane', 'oxygen', 'linear')
CP.apply_simple_mixing_rule('oxygen', 'toluene', 'linear')
for i,  step in enumerate(steps):
    equivalenceratio = step

    # set the mixture composition according to the stoichiometric mixture
    # (equivalence ratio = 1)
    gas.set_equivalence_ratio(equivalenceratio, fuel, oxidizer)

    # This function can be used to compute the equivalence ratio for any mixture.
    # An optional argument "basis" indicates if fuel and oxidizer compositions are
    # provided in terms of mass or mole fractions. Default is mole fractions.
    # If fuel and oxidizer are given in mass fractions, use basis='mass'
    phi = gas.equivalence_ratio(fuel, oxidizer)
    # print("phi = {:1.3f}".format(phi))

    # the mixture fraction Z can be computed as follows:
    Z[i] = gas.mixture_fraction(fuel, oxidizer)
    # print("Z = {:1.3f}".format(Z[i]))

    gas.HP = (1-Z[i])*gas_o.h + Z[i]*gas_f.h, 6000000

    # The mixture fraction is kg fuel / (kg fuel + kg oxidizer). Since the fuel in
    # this example is pure methane and the oxidizer is air, the mixture fraction
    # is the same as the mass fraction of methane in the mixture
    # print("mass fraction of fuel = {:1.3f}".format(gas["c6h12"].X[0]))fuel = "nc10h22:0.780, c6h12:0.098, C6H5CH3:0.122"
    frac1 = gas["o2"].X[0]
    frac2 = gas["C6H5CH3"].X[0]
    frac3 = gas["c6h12"].X[0]
    frac4 = 1- frac1 -frac2 -frac3
    fluid = 'oxygen['+ str(frac1) +']&Cyclohexane['+ str(frac3) + ']&decane[' + str(frac4) + ']&toluene[' + str(frac2) + ']'
    # print(fluid)
    print(Z[i],gas.T)
    densityCP[i] = CP.PropsSI("D", "T", gas.T, "P", 6000000, fluid)
    density[i] = gas.density
    
    # # Mixture fraction and equivalence ratio are invariant to the reaction progress.
    # # For example, they stay constant if the mixture composition changes to the burnt
    # # state
    # gas.equilibrate('HP')
    # phi_burnt = gas.equivalence_ratio(fuel, oxidizer)
    # Z_burnt = gas.mixture_fraction(fuel, oxidizer)
    # print("phi(burnt) = {:1.3f}".format(phi_burnt))
    # print("Z(burnt) = {:1.3f}".format(Z))
fig = plt.figure()
plt.plot(Z, density, 'gp')
plt.plot(Z, densityCP)
plt.xlabel("Mixture fraction")
plt.ylabel("Density")
plt.legend()
plt.show()