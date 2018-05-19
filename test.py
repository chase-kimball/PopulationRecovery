import numpy as np
from scipy import stats
import recoverPop
import matplotlib.pyplot as plt
def fgen(params):

    return stats.norm(params[0],params[1]).pdf

mu_o = .4
sig_o = .1
f_o = stats.norm(.4,.1)

eventPosteriors = []
k_events = 40
N_points = 100
for k in range(k_events):
    sig = np.random.uniform(0,.2)
    mu = f_o.rvs()

    print mu

    fk = stats.norm(mu,sig)
    data=[]
    ii=0
    while ii<N_points:
        x=fk.rvs()
        if x>0 and x<1:
            data.append(x)
            ii+=1
    eventPosteriors.append(recoverPop.Posterior(data))

mc = recoverPop.PopEstimator(fgen,2,eventPosteriors)
mc.MCMC([[0,1],[0,.5]],[np.random.uniform(0,1.),np.random.uniform(0,.5)],NumTrials=200000)
mu,sig = mc.param_dists

plt.hist(mc.param_dists[0])
plt.show()
plt.hist(mc.param_dists[1])
plt.show()


print np.mean(mu)
print np.mean(sig)
np.savetxt('TestPost200000.txt',mc.param_dists)
