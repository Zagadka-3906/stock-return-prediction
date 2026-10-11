"""Freeze a new postprocessing frontier on actual148; no future features or quality score."""
from pathlib import Path
import sys,time,hashlib,copy
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def exact(a,b):
 import numpy as np
 assert a.dtype==b.dtype==np.float64 and a.shape==b.shape and np.array_equal(a.view('u8'),b.view('u8'))
def main():
 import numpy as np
 import SparseAfter148_complete_parent_CDF_v1_20261009 as codec
 from run import fold_cutoff
 proposal=A/'SparseAfter14829_round152_proposal_v1_20261009.json';assert not proposal.exists()
 original_plan=A/'HuberSparse59_round150_proposal_v1_20261008.json';old=read(original_plan)
 heads={h:copy.deepcopy(old['heads'][h]) for h in codec.HEADS}
 cases=[{'group':0,'share':.5,'amplitude':0.}]
 cases.extend({'group':g,'share':.5,'amplitude':a} for g in range(6) for a in (.0005,.001,.002,.00325))
 assert len(cases)==25
 source=A/'HuberSparse_complete_parent_native_stage_v1_20261008.py';native=A/'SparseAfter148_complete_parent_native_stage_v1_20261009.py'
 text=source.read_text(encoding='utf8').replace('HuberSparse_complete_parent_CDF_v1_20261008','SparseAfter148_complete_parent_CDF_v1_20261009')
 text=text.replace("GRAPH_KEY='nonflag_CPU_HuberSparse_complete_parent_CDF'","GRAPH_KEY='nonflag_CPU_SparseAfter148_complete_parent_CDF'")
 text=text.replace("spec['share'] in (.25,.5,.75)","spec['share']==.5")
 # Explicitly retain the fully qualified148 graph before this final stage.
 needle="    assert context._whole_graph[GRAPH_KEY]==spec\n"
 assert text.count(needle)==1
 text=text.replace(needle,needle+"    assert spec['original_complete_parent_round']==148\n")
 compile(text,str(native),'exec')
 with native.open('x',encoding='utf8') as f:f.write(text)
 inputs=[Path(__file__),Path(codec.__file__),source,native,original_plan,ROOT/'run.py',ROOT/'后续选模标准.md',
  A/'nonflag_residual_SparseGram64_bank10_20261007/verification.json']
 metadata=[]
 for y in range(2021,2026):
  reference=None
  for h,r in heads.items():
   p=Path(r['infos'][str(y)]);v=read(p)
   assert v['year']==y and v['exclusive_cutoff']==fold_cutoff(y)
   assert v['last_training_label_date']<v['exclusive_cutoff'] and v['last_training_label_end']<=v['exclusive_cutoff']
   identity={k:v[k] for k in ('features','training_rows','exclusive_cutoff','last_training_label_date','last_training_label_end','training_matrix_numeric_sha256','training_target_numeric_sha256')}
   if reference is None:reference=identity
   assert identity==reference
   m=Path(v['native_model_path']);d=Path(v['independent_linear_state_path'])
   assert sha(m)==v['native_model_sha256'] and sha(d)==v['independent_linear_state_sha256']
   inputs.extend([p,m,d]);metadata.append({'head':h,'year':y,'native_sha256':sha(m),'independent_sha256':sha(d)})
 for r in heads.values():inputs.extend([Path(r['oof']),Path(r['folder'])/'oof_verification.json'])
 rng=np.random.default_rng(15220261009)
 dates=np.repeat(np.array([20201230,20210104,20230103,20241230,20250102,20260102]),47)
 parent=np.round(rng.normal(size=len(dates)),1).astype(np.float64);parent[0]=-0.
 flags=rng.integers(0,2,len(dates));valid=rng.random(len(dates))>.2
 raw={h:rng.normal(size=len(dates)).astype(np.float64) for h in codec.HEADS};records=[]
 for i,c in enumerate(cases):
  r=codec.mixture(raw,c['group'],c['share']);exact(r,codec.independent_mixture(raw,c['group'],c['share']))
  out=codec.transform(parent,r,dates,flags,valid,c['amplitude'])
  exact(out,codec.pandas_oracle(parent,r,dates,flags,valid,c['amplitude']))
  keep=(dates<20210101)|(flags==1)|~valid;exact(out[keep],parent[keep])
  cold=[]
  for n in (94,188,235):
   prefix=codec.transform(parent[:n],r[:n],dates[:n],flags[:n],valid[:n],c['amplitude']);exact(prefix,out[:n]);cold.append(n)
  poisoned=parent.copy();poisoned[dates>=20250101]=rng.normal(size=(dates>=20250101).sum())
  other=codec.transform(poisoned,r,dates,flags,valid,c['amplitude']);exact(other[dates<20250101],out[dates<20250101])
  if not c['amplitude']:exact(out,parent)
  records.append({'case':i,'configuration':c,'Pandas_arithmetic_exact':True,'cold_prefixes':cold,
   'future_parent_perturbation_preserves_past':True,'invalid_flag1_2020_bits_preserved':True,
   'synthetic_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(out)).cast('B')).hexdigest()})
 pins={str(p):sha(p) for p in dict.fromkeys(inputs)}
 create(proposal,{'status':'frozen_new_sparse_only_after_actual148_complete_graph_proposal_not_scored_or_admitted',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'target_round':152,'after_round':151,'fixed_scientific_stage_base_round':148,
  'anchor_rounds':[148,149,150,151],'teacher_round':106,'heads':heads,'groups':codec.GROUPS,'new_cases':cases,
  'expected_new_full_cases':25,'expected_cold_cases':75,'expected_official_cases':29,'existing_annual_states':10,
  'mixture_operation_order':'ordered mean within sparse family then sign, after full frozen148 CrossHuber graph',
  'new_direction':'sparse-only final CDF stage on complete148;150151 mixed residuals use134 and do not cover this parent',
  'requires_actual148_and151_full_completion_and_prior_full_forecast_duplicate_audit':True,
  'quality_selection':'highest_complete_connected2020_2024_official_S_then_physical_native_count_then_abs_amplitude_then_case',
  'required_remaining':['all5_annual_native_reload_independent_OOF_and_cold_controls','full25_training_Pandas_and75_prefix_controls',
   'complete32_prospective_sources_and_parent_routes','official29_scoring_and_main','complete_source_freeze_before_futureX',
   'selected_two_full_native_independent_CSV_replays_and_cold80','sealed_candidate_full_QA_six_views_and_main'],
  'input_sha256':pins,'new_native_fits':0,'new_official_scores':0,'actual_future_X_read':False,'test_labels_read':False,
  'all_training_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,'optimization_exhaustion_proven':False})
 create(A/'SparseAfter14829_synthetic25_and_state10_metadata_v1_20261009.json',{
  'status':'passed_actual25_synthetic75_prefixes_and10_saved_state_maturity_metadata_not_native_replay',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{**pins,str(proposal):sha(proposal)},'records':records,
  'actual_cases':25,'actual_cold_cases':75,'actual_existing_state_metadata':metadata,
  'actual_parent148_full_controls_and_native_new_stage_replays_still_required':True,
  'new_native_fits':0,'new_official_scores':0,'actual_future_X_read':False,'test_labels_read':False})
 print({'proposal_cases':29,'synthetic_cases':25,'synthetic_cold':75,'saved_state_metadata':10,'new_fits':0},flush=True)
if __name__=='__main__':main()
