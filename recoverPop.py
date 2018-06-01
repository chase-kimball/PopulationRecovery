import numpy as np
import pdb
class Posterior():
    """
    Probably overkill, but just in case we want to start storing
    meta-information on the event posteriors. Example case:
    draws from some underlying gaussian with true mu* and sig*,
    which we want to figure out.

    """
    def __init__(self,data, joint=False):
        self.data=np.asarray(data)
        if joint: self.Nsamps,self.Mdim = self.data.shape[0],self.data.shape[1]
        else: self.Nsamps,self.Mdim = self.data.shape[0],1.

class PopEstimator():
    """
    fpop: Parametrized population  function. If your posteriors are over q variables, and your function is parametrized by p parameters, must be of the form f([qxanything array],[px1 array])

    fprior: Defaults to flat. This is pi(f(lambda)) in eqs 4 and 10. of https://arxiv.org/pdf/0912.5531
    "should include any a priori astrophysical understanding"

    MCMC algorithm is Metropolis Hastings

    """
    def __init__(self,fpop, nparams, posteriors, fprior = lambda x: 1.):
        self.fpop = fpop
        self.nparams = nparams
        self.posteriors = posteriors
        print [post.Nsamps for post in posteriors]
        self.fprior = fprior
        if False in [post.Mdim==posteriors[0].Mdim for post in posteriors]:
            raise Exception("Joint posteriors must be over the same number of parameters")
        else: self.Mdim = posteriors[0].Mdim
            
    def postPop(self,p_i):
        """
        Equation 10. Proportional to P(f_i|p1,...,pk) where f_i is the proposed population distribution  and p1,...,pk are the event posteriors
        
        """
         sum = np.asarray([np.sum(self.fpop(post.data,p_i))/post.Nsamps for post in self.posteriors])
        return np.product(sum)
        
    def MCMC(self,paramlims,seed,NumTrials=100000,burn=.2):

        def jump_proposal(): 
            return [np.random.uniform(low,high) for (low,high) in paramlims]
        
        p_i = seed
        self.samples=[seed]
        limtest=np.linspace(0.001,.2,100)
        ytest = np.array([self.postPop([.4,muu]) for muu in limtest])
        maxy = np.max(ytest)
        print np.where(ytest==maxy)
        print limtest[np.where(ytest==maxy)[0]]
        for i in range(NumTrials):
            p_prime = jump_proposal()
            alpha = self.postPop(p_prime)/self.postPop(p_i)
            if np.random.uniform() < alpha: p_i = p_prime[:]
            self.samples.append(p_i)
        self.samples=self.samples[int(burn*NumTrials):]
        self.param_dists = np.transpose(self.samples)







          
 
       
