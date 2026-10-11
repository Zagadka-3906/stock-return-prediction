"""Pointwise horizon agreement/disagreement fusion; no fitted state or date lookahead."""
def combine(first,second,penalty):
 import numpy as np
 a=np.asarray(first,dtype=np.float64);b=np.asarray(second,dtype=np.float64);k=float(penalty)
 assert a.ndim==b.ndim==1 and a.shape==b.shape and np.isfinite(a).all() and np.isfinite(b).all()
 assert k in (.5,.75,1.,2.)
 mean=.5*a+.5*b
 return mean if k==0. else mean-k*np.abs(a-b)
def scalar_oracle(first,second,penalty):
 import numpy as np
 k=float(penalty);assert len(first)==len(second) and k in (.5,.75,1.,2.)
 return np.fromiter((.5*float(a)+.5*float(b) if k==0. else .5*float(a)+.5*float(b)-k*abs(float(a)-float(b)) for a,b in zip(first,second)),dtype=np.float64,count=len(first))
