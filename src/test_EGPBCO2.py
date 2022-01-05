import numpy as np

from utils import *
from copy import deepcopy
np.random.seed(0)
# plt.ion()
# ================================================
# define covariance
def k0(X1, X2, 𝛾, σ):
    cov = np.zeros((len(X1), len(X2)))
    for i in range(len(X1)):
        for j in range(len(X2)):
            cov[i,j] = σ**2 * np.exp(-np.sqrt(np.sum((X1[i] - X2[j]))**2)/ 𝛾)
    return cov

# define basis function
def f(x, θ):
    return θ[0] + θ[1]*x[:,0]

def dfdθ(x, θ):
    if len(x.shape)<=1:
        return np.array([1, x[0]])
    else:
        N = len(x)
        return np.vstack([np.ones(N), x[:,0]]).T
        
def h(X1, X, θ, 𝛾, σ):
    K0x = k0(X1, X, 𝛾, σ)
    df = dfdθ(X1,θ)
    return df.T * np.mean(K0x, axis=1)

def k(X1, X2, X, H, θ, 𝛾, σ):
    return k0(X1,X2, 𝛾, σ) + h(X1,X,θ, 𝛾, σ).T @ np.linalg.pinv(H) @ h(X2,X,θ, 𝛾, σ)

## settings for C12
fluid = "CO2"
name1 = ['10']#, '10', '15', '20'
name2 = ['A', 'C', 'D', 'H','L', 'S', 'V']#'A', 'C', 'D', 'H',, 'S', 'V'
# ================================================
for i in range(len(name1)):
    for j in range(len(name2)):
        # load data
        data = np.loadtxt("mechco2/%s_%s.csv"%(name1[i],name2[j]), delimiter=',')
        para = np.loadtxt("mechco2/%s_%s_para.csv"%(name1[i],name2[j]), delimiter=',')

        X = []
        y = []
        dim = data.shape[1]-1
        yscale = para[4,0]
        X = data[:,:dim]
        print(np.shape(X))
        y = data[:,dim]/yscale
        N = len(y)-3

        Ntrain = int(N*0.8)
        Ntest = N - Ntrain
        idx = np.random.permutation(N)
        Xall = deepcopy(X)
        yall = deepcopy(y)
        X = Xall[idx[:Ntrain], :]
        y = yall[idx[:Ntrain]]
        Xtest = Xall[idx[Ntrain:N], :]
        ytest = yall[idx[Ntrain:N]]

        𝛾 = para[0,:dim] # kernel size
        σ = para[0,dim]  # kernel multiplier
        θ = para[1,:]    # basis function's parameters
        print("theta:", θ)

        AS = CP.AbstractState("HEOS", fluid)
        Tc = CP.PropsSI(fluid, 'Tcrit')
        Pc = CP.PropsSI(fluid, 'pcrit')
        omega = AS.acentric_factor()

        print(𝛾, σ)

        K0  = k0(X, X,𝛾, σ)
        print(len(K0))
        df = dfdθ(X,θ)
        Hm = [np.outer(df[i], df[j]) * K0[i,j] for i in range(len(X)) for j in range(len(X))]
        H = np.mean(Hm, axis=0)
        print(H)
        print(np.linalg.pinv(H))

        # ================================================
        # random queries
        M = 1000

        x1lim = [np.min(X[:,0]), np.max(X[:,0])]
        Xnew = np.random.rand(M, dim)
        Xnew[:,0] = Xnew[:,0] * (x1lim[1] - x1lim[0]) + x1lim[0]
        Xnew = Xnew[np.argsort(Xnew[:,0]),:]

        # ================================================
        # GP predict
        K = k(X, X, X, H, θ, 𝛾, σ)
        Ki = np.linalg.inv(K + 0*np.diag(np.ones(len(X))))
        Kxx = k(Xnew, Xnew, X, H, θ, 𝛾, σ)
        Kx = k(X, Xnew, X, H, θ, 𝛾, σ)

        mu = (f(Xnew,θ) + Kx.T @ Ki @ (y-f(X,θ))) * yscale
        cov = Kxx - Kx.T @ Ki @ Kx
        sigma = np.diag(cov)

        Ypred = f(X,θ) + K.T @ Ki @ (y-f(X,θ))

        # ================================================
        # 2d plot
        plt.figure()
        plt.plot(X[:,0], y*yscale, 'rv')
        plt.plot(Xnew[:,0], mu, 'gp', fillstyle='none')
        plt.xlabel("Tr")
        plt.ylabel(name2[j])
        plt.title(name1[i])
        plt.legend(['data', 'newset'])
        plt.savefig("figs/co2/fit_%s_%s.png"%(name1[i],name2[j]))

        # 2d plot
        plt.figure()
        plt.plot(y, y, 'k--')
        plt.plot(y, Ypred, 'gp', fillstyle='none')
        plt.xlabel("Groundtruth")
        plt.ylabel("Prediction")
        plt.title(name1[i])
        plt.legend(['data', 'predict'])
        plt.savefig("figs/co2/prediction_%s_%s.png"%(name1[i],name2[j]))
        # ================================================
        # Extra validation
        ypred_train = f(X,θ) + k(X, X, X, H, θ, 𝛾, σ).T @ Ki @ (y-f(X,θ))
        ypred_test = f(Xtest,θ) + k(X, Xtest, X, H, θ, 𝛾, σ).T @ Ki @ (y-f(X,θ))

        fig = plt.figure()
        plt.plot(y, y, 'k')
        # plt.plot(y, Ypred, 'gp', fillstyle='none')
        plt.plot(y, ypred_train, 'rs', fillstyle="none", label='Training Data')
        plt.plot(ytest, ypred_test, 'gv', fillstyle="none", label='Test Data')
        plt.xlabel("Groundtruth")
        plt.ylabel("Prediction")
        plt.legend(['data', 'training data', 'test data'])
        plt.title(name1[i])
        plt.savefig("figs/co2/Validation_%s_%s.png"%(name1[i],name2[j]))

        # plt.draw()
        # plt.pause(1e-6)
        del X, y, Xtest, ytest

plt.show()
# plt.pause(1e2)
