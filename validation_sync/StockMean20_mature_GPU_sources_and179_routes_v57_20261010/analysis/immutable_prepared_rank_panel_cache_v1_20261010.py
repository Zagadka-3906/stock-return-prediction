"""Reuse native same-date rank preparation for a fixed owned panel; keep cold prefix preparation separate."""
import numpy as np
import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as cdf
import protected_upper_tail_rank_permutation_v1_20261010 as valid_tail
import protected_official_top_rank_permutation_v2_20261010 as top_tail

class Panel:
    def __init__(self,parent,raw,dates,flags,valid):
        self.parent=np.array(parent,dtype=np.float64,copy=True)
        self.raw=np.array(raw,dtype=np.float64,copy=True)
        self.dates=np.array(dates,copy=True);self.flags=np.array(flags,copy=True)
        self.valid=np.array(valid,dtype=bool,copy=True);self.prepared={}
        arrays=(self.parent,self.raw,self.dates,self.flags,self.valid)
        assert all(x.ndim==1 and len(x)==len(self.parent) for x in arrays)
        assert len(self.parent)>0 and np.isfinite(self.parent).all() and np.isfinite(self.raw).all()
        assert np.all(self.dates[1:]>=self.dates[:-1])
        for x in arrays:x.flags.writeable=False

    def transform(self,configuration,n=None):
        n=len(self.parent) if n is None else n
        assert isinstance(n,(int,np.integer)) and 0<n<=len(self.parent)
        assert n==len(self.parent) or self.dates[n-1]!=self.dates[n],'Prefix must end at a complete date'
        sign=float(configuration['sign']);assert sign in (-1.,1.)
        key=(int(n),sign)
        if key not in self.prepared:
            prepared=cdf.prepare(self.parent[:n],self.raw[:n],self.dates[:n],self.flags[:n],self.valid[:n],sign)
            for row in prepared:
                for x in row[2:]:x.flags.writeable=False
            self.prepared[key]=prepared
        codec={'CDF':cdf,'valid_pool_protection_v1':valid_tail,'official_Top_protection_v2':top_tail}[configuration['kind']]
        args=(configuration['role'],configuration['weight']) if configuration['kind']=='CDF' else (configuration['weight'],configuration['protect_fraction'])
        return codec.apply_prepared(self.parent[:n],self.flags[:n],self.valid[:n],*args,self.prepared[key])
