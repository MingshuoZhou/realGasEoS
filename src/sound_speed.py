from utils import *
# test program
if __name__ == "__main__":
    gas = ct.Solution('mech/nDodecane_AlphaGP.yaml')
    gas.X = 'c12h26:1'
    for n in range(27):
        T = 300.0 + 100.0 * n
        gas.TP = T, ct.one_atm*100
        print(T, equilSoundSpeeds(gas))
