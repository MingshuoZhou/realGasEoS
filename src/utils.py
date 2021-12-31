import os, sys, time
import numpy as np
import cantera as ct
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
import math
print('Running Cantera version: ' + ct.__version__)

plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['figure.autolayout'] = True
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['font.family'] = 'serif'

R = 8.31446
def PR(T_c, P_c, R_u=R):
    a = 0.45724 * R_u**2 * T_c**2 / P_c
    b = 0.07780 * R_u * T_c / P_c
    return a, b

def PR_alpha(T, P, T_c, P_c, omega):
    a = 0.45724 * R**2 * T_c**2 / P_c
    b = 0.07780 * R * T_c / P_c
    kappa = 0.37464 + 1.54226*omega - 0.26992*omega**2
    alpha = ( 1 + kappa * (1-np.sqrt(T/T_c)) )**2
    return alpha

def PR_dalphadT(T, P, T_c, P_c, omega):
    a = 0.45724 * R**2 * T_c**2 / P_c
    b = 0.07780 * R * T_c / P_c
    kappa = 0.37464 + 1.54226*omega - 0.26992*omega**2
    dalphadT = kappa*kappa/T_c - (kappa*kappa+kappa)/np.sqrt(T_c) * T**(-1/2)
    return dalphadT

def PR_d2alphadT2(T, P, T_c, P_c, omega):
    a = 0.45724 * R**2 * T_c**2 / P_c
    b = 0.07780 * R * T_c / P_c
    kappa = 0.37464 + 1.54226*omega - 0.26992*omega**2
    d2alphadT2 = 0.5*(kappa*kappa+kappa)/np.sqrt(T_c) * T**(-3/2)
    return d2alphadT2

def get_TPD_under_P(fluid,P, T_lo, T_hi, T_step=20, D_step=40):
    TPD_arr = []
    T = T_lo
    D = CP.PropsSI("D", "T", T, "P", P, fluid)
    T_old = T
    D_old = D
    count = 0
    alpha = 0.50
    while T <= T_hi:
        D = CP.PropsSI("D", "T", T, "P", P, fluid)
        if abs(D_old - D) < D_step or count > 5:
            TPD_arr.append([T, P, D])
            T_old = T
            D_old = D
            T += T_step
            count = 0
        else:
            T = T - alpha*(T - T_old)
            count += 1
    return TPD_arr

def get_uniform_TPD_under_P(fluid,P, T_lo, T_hi, T_step=20, D_step=40):
    TPD_arr = []
    T = T_lo
    while T < T_hi - T_step/2:
        T += T_step / 2
        try:
            D = CP.PropsSI("D", "T", T, "P", P, fluid)
        except:
            D = 0
        TPD_arr.append([T,P,D])
    T = T_hi
    try:
        D = CP.PropsSI("D", "T", T, "P", P, fluid)
    except:
        D = 0
    TPD_arr.append([T,P,D])
    return TPD_arr

def get_data(fluid,P, T_lo, T_hi, T_step, D_step, Dataname, unit_convert):
    TPD_arr = []
    T = T_lo
    D = CP.PropsSI("D", "T", T, "P", P, fluid)*unit_convert
    T_old = T
    D_old = D
    count = 0
    alpha = 0.50
    while T <= T_hi:
        D = CP.PropsSI(Dataname, "T", T, "P", P, fluid)*unit_convert
        if abs(D_old - D) < D_step or count > 5:
            TPD_arr.append([T, P, D])
            T_old = T
            D_old = D
            T += T_step
            count = 0
        else:
            T = T - alpha*(T - T_old)
            count += 1
    return TPD_arr
    # TPD_arr = []
    # T = T_lo
    # while T <= T_hi:
    #     D = CP.PropsSI(Dataname, "T", T, "P", P, fluid)
    #     TPD_arr.append([T, P, D])
    #     T += T_step
    # return TPD_arr

def get_dataco2(fluid,P, T_lo, T_hi, T_step, T_min, Dataname):
    TPD_arr = []
    T = T_lo
    D = CP.PropsSI("D", "T", T, "P", P, fluid)
    T_old = T
    D_old = D
    alpha = 0.50
    # print(1)
    while T <= T_hi:
        D = CP.PropsSI(Dataname, "T", T, "P", P, fluid)
        if abs((D_old - D)/D_old) < 0.05 or T-T_old< T_min:
            TPD_arr.append([T, P, D])
            T_old = T
            D_old = D
            T += T_step
        else:
            T = T - alpha*(T - T_old)
    return TPD_arr

def equilSoundSpeeds(gas, rtol=1.0e-6, max_iter=5000):
    """
    Returns a tuple containing the equilibrium and frozen sound speeds for a
    gas with an equilibrium composition.  The gas is first set to an
    equilibrium state at the temperature and pressure of the gas, since
    otherwise the equilibrium sound speed is not defined.
    """

    # set the gas to equilibrium at its current T and P
    gas.equilibrate('TP', rtol=rtol, max_iter=max_iter)

    # save properties
    s0 = gas.s
    p0 = gas.P
    r0 = gas.density
    # print(p0)
    # perturb the pressure
    p1 = p0*1.0001

    # set the gas to a state with the same entropy and composition but
    # the perturbed pressure
    gas.SP = s0, p1

    # frozen sound speed
    afrozen = math.sqrt((p1 - p0)/(1.0001*gas.density - r0))

    # # now equilibrate the gas holding S and P constant
    # gas.equilibrate('SP', rtol=rtol, max_iter=max_iter)
    # # print(gas.density, r0)

    # # equilibrium sound speed
    # aequil = math.sqrt(abs(p1 - p0)/abs(gas.density - r0))

    # compute the frozen sound speed using the ideal gas expression as a check
    # gamma = gas.cp/gas.cv
    # afrozen2 = math.sqrt(gamma * ct.gas_constant * gas.T /
    #                      gas.mean_molecular_weight)

    return afrozen