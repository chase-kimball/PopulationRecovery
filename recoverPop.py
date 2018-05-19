import numpy as np

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
    fgenerator: Takes in guesses of population parameters (e.g. mu, sig)
    returns an analytic pdf f(x) that can be evaluated anywhere in parameter space.
    e.g. f(mu,sig)=gaussian(x;mu,sig) to be evaluated at x. f() is the distribution
    that we want a distribution over. It must be vectorized

    fprior: Defaults to flat. This is pi(f(lambda)) in eqs 4 and 10. of https://arxiv.org/pdf/0912.5531
    "should include any a priori astrophysical understanding"

    Fitting algorithm is Metropolis Hastings

    posterior instances: an array of posterior instances. Each event posterior can have any
    number of data points, but they need to be over the same number of parameters

    """
    def __init__(self,fgenerator, nparams, posteriors, fprior = lambda x: 1.):
        self.fgenerator = fgenerator
        self.nparams = nparams
        self.posteriors = posteriors
        self.fprior = fprior
        if False in [post.Mdim==posteriors[0].Mdim for post in posteriors]:
            raise Exception("Joint posteriors must be over the same number of parameters")
        else: self.Mdim = posteriors[0].Mdim
            
    def postPop(self,f):
        """
        Equation 10. Proportional to P(f_i|p1,...,pk) where f_i is the proposed population distribution
        and p1,...,pk are the event posteriors

        """
        sum = np.asarray([np.sum(f(post.data))/post.Nsamps for post in self.posteriors])
        return self.fprior(f)*np.product(sum)
    
    def MCMC(self,paramlims,seed,NumTrials=100000,burn=.2):

        def jump_proposal(): 
            return [np.random.uniform(low,high) for (low,high) in paramlims]
        
        
        p_i = seed
        f_i = self.fgenerator(p_i)
        self.samples=[seed]
        for i in range(NumTrials):
            p_prime = jump_proposal()
            f_prime = self.fgenerator(p_prime)
            alpha = self.postPop(f_prime)/self.postPop(f_i)
            if np.random.uniform()<alpha: p_i, f_i = p_prime[:], f_prime
            self.samples.append(p_i)
        self.samples=self.samples[int(burn*NumTrials):]
        self.param_dists = np.transpose(self.samples)







          
 
       
