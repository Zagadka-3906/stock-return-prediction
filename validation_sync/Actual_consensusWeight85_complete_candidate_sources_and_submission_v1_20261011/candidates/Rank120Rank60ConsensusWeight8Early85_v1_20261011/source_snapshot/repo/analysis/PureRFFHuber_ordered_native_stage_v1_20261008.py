"""Compose the two independently checked saved-model stages in an explicit frozen order."""
from copy import copy
import hashlib
import numpy as np
import PureRFFHuber_ordered_CDF_v1_20261008 as codec
import PureRFFMean_complete_parent_native_stage_v1_20261008 as cross
import HuberCrossFamilyFine_complete_parent_native_stage_v1_20261008 as huber
GRAPH_KEY=codec.GRAPH_KEY
def exact(x,y):
 assert x.dtype==y.dtype==np.float64 and x.shape==y.shape and np.array_equal(x.view('u8'),y.view('u8'))
def after_parent(ns,context,teacher,parent,spec,components):
 case=spec['configuration'];codec.check(case)
 assert context._whole_graph[GRAPH_KEY]==spec
 assert spec['original_complete_parent_round']==134 and spec['universe']=='all_current_raw_forecasts'
 assert spec['position']=='ordered_composite_after_complete_qualified134_parent'
 assert spec['teacher_feature']=='qualified106_current_forecast_average_rank_over_N'
 heads=codec.required(case);assert [c['head'] for c in components]==heads
 indexed={c['head']:c for c in components};assert len(indexed)==len(components)
 result=np.array(parent,dtype=np.float64,copy=True);reports=[]
 for name in case['order']:
  cfg=case[name]
  if not cfg['amplitude']:continue
  module=cross if name=='cross' else huber
  # The adapter records the whole composite relative to qualified134, while each original kernel sees its existing contract.
  single={**cfg,'universe':spec['universe'],'position':'after_complete_qualified_parent','teacher_feature':spec['teacher_feature']}
  current=copy(context);current._whole_graph={**context._whole_graph,module.GRAPH_KEY:single}
  names=list(dict.fromkeys(h for members,sign in codec.CODECS[name].GROUPS[4] for h in members))
  result,report=module.after_parent(ns,current,teacher,result,single,[indexed[h] for h in names])
  reports.append({'stage':name,'configuration':cfg,'actual_stage_index':len(reports),'original_kernel_contract_adapter':single,
   'parent_is_previous_composite_output_after_qualified134':True,'native_reload_independent_and_Pandas_report':report})
 preserved=(context.dates<20210101)|(context.flags==1)|~context.valid
 exact(result[preserved],np.asarray(parent,dtype=np.float64)[preserved])
 return result,{'rows':len(result),'explicit_order':case['order'],'configuration':case,'ordered_heads':heads,'stage_reports':reports,
  'all_nonzero_stages_use_same_original_teacher106':True,'actual_complete_qualified_base_round':134,
  'no_separate_qualification_claim_for_intermediate_composite_output':True,
  'complete_parent2020_flag1_invalid_bits_preserved':True,'all_stage_native_reload_independent_and_Pandas_bits_checked':True,
  'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(result)).cast('B')).hexdigest()}
