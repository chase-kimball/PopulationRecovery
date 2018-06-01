import numpy as np
from scipy import stats
import recoverPop
import matplotlib.pyplot as plt
import pdb
def fpop(x,params):
    
    return np.exp(-((x-params[0])**2)/(2*(params[1]**2)))/(np.sqrt(2*np.pi)*params[1])

mu_o = .4
sig_o = .1
f_o = stats.norm(mu_o,sig_o)

eventPosteriors = []
k_events = 20
N_points = 100
for k in range(k_events):
    sig = np.random.uniform(0,.2)#np.random.uniform(0,.2)
    mu=0
    while mu<=0 or mu>1:
        mu=f_o.rvs()

    #print mu

    fk = stats.norm(mu,sig)
    data=[]
    ii=0
    while ii<N_points:
        x=fk.rvs()
        if x>0 and x<1:
            data.append(x)
            ii+=1
    eventPosteriors.append(recoverPop.Posterior(data))
    
mc = recoverPop.PopEstimator(fpop,2,eventPosteriors)
mc.MCMC([[0,1],[.01,.5]],[np.random.uniform(0,1.),np.random.uniform(0.01,.5)],NumTrials=100000)
mu,sig = mc.param_dists

n,bins,patches=plt.hist(mc.param_dists[0])
print np.argmax(n)

plt.show()
plt.hist(mc.param_dists[1])
plt.show()


print np.mean(mu)
print np.mean(sig)
np.savetxt('TestPost200000.txt',mc.param_dists)
