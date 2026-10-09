"""Explicit ordered two-stage CDF over an unchanged complete base; independent Pandas oracle."""
import numpy as np
import PureRFFMean_complete_parent_CDF_v1_20261008 as cross
import HuberCrossFamilyFine_complete_parent_CDF_v1_20261008 as huber
CODECS={'cross':cross,'huber':huber}
GRAPH_KEY='nonflag_CPU_PureRFF_Huber_ordered_complete_parent_CDF'
def check(case):
 assert case['order'] in (['cross','huber'],['huber','cross'])
 for name in ('cross','huber'):
  spec=case[name];assert spec['group']==4
  assert spec['share']==0. if name=='cross' else spec['share'] in (.375,.5,.625)
  assert spec['amplitude'] in ((0.,.001,.0015,.002,.0025,.003,.00325) if name=='cross' else (0.,.001,.0025,.00325))
def required(case):
 check(case);heads=[]
 for name in case['order']:
  if case[name]['amplitude']:
   for members,sign in CODECS[name].GROUPS[4]:heads.extend(members)
 return list(dict.fromkeys(heads))
def transform(parent,raw,dates,flags,valid,case):
 check(case);value=np.array(parent,dtype=np.float64,copy=True)
 for name in case['order']:
  spec=case[name]
  if spec['amplitude']:
   codec=CODECS[name];r=codec.mixture(raw,4,spec['share'])
   value=codec.transform(value,r,dates,flags,valid,spec['amplitude'])
 return value
def pandas_oracle(parent,raw,dates,flags,valid,case):
 check(case);value=np.array(parent,dtype=np.float64,copy=True)
 for name in case['order']:
  spec=case[name]
  if spec['amplitude']:
   codec=CODECS[name];r=codec.independent_mixture(raw,4,spec['share'])
   value=codec.pandas_oracle(value,r,dates,flags,valid,spec['amplitude'])
 return value
