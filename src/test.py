import numpy as np
T = np.linspace(np.log(250),np.log(1250),100)
T = np.exp(T)
P = np.linspace(np.log(7.38),np.log(20),20)
P = np.exp(P)
print(T)
print(P)