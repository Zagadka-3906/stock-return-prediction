from pathlib import Path
import sys,re,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_SparseAfter148152_core_drafts_v1_20261009 import route
def normalize(s):
 s=s.replace('SparseAfter14872','SparseAfter14860').replace('actual20_','actual10_').replace('states55','states25')
 s=s.replace('actual_declared55','actual_declared25').replace('all55_nonanchors_full_and165','all25_nonanchors_full_and75')
 s=s.replace('states25_fixed_base_CDF165cold72','states25_fixed_base_CDF75cold60')
 s=s.replace('states55_CDF165cold72','states25_CDF75cold60').replace('saved_states','saved_states')
 s=s.replace('synthetic55_and_state20','synthetic25_and_state10')
 s=s.replace("hooks['actual_historical_cases']==24","hooks['actual_historical_cases']==48")
 s=s.replace("hooks['actual_calendar_cases']==18","hooks['actual_calendar_cases']==12")
 s=s.replace("hooks['actual_cold_cases']==72","hooks['actual_cold_cases']==60")
 s=s.replace("'actual_historical_native_hooks':24","'actual_historical_native_hooks':48")
 s=s.replace("'actual_final_calendar_native_hooks':18","'actual_final_calendar_native_hooks':12")
 s=s.replace("'actual_cold_native_hooks':72","'actual_cold_native_hooks':60")
 s=s.replace('SparseAfter148150','SparseAfter148152')
 return s
pairs=[('run_SparseAfter14829_official_comparison_v1_20261009.py','run_SparseAfter14829_official_comparison_v2_20261009.py',False),
 ('prepare_SparseAfter14829_selected_candidate_v1_20261009.py','prepare_SparseAfter14829_selected_candidate_v2_20261009.py',False),
 ('seal_SparseAfter14829_selected_candidate_v1_20261009.py','seal_SparseAfter14829_selected_candidate_v2_20261009.py',False),
 ('run_SparseAfter14829_round152_full_registration_v1_20261009.py','run_SparseAfter14829_round152_full_registration_v2_20261009.py',False),
 ('publish_HuberSparse59_evidence_v1_20261009.py','publish_SparseAfter14829_evidence_v1_20261009.py',True),
 ('verify_HuberSparse59_round150_sources_v1_20261009.py','verify_SparseAfter14829_round152_sources_v1_20261009.py',True),
 ('verify_HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009.py','verify_SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009.py',True),
 ('verify_HuberSparse59_prospective_routes_v1_20261009.py','verify_SparseAfter14829_prospective_routes_v1_20261009.py',True),
 ('dispatch_HuberSparse150_complete_pipeline_v1_20261009.py','dispatch_SparseAfter148152_complete_pipeline_v1_20261009.py',True)]
mapping={old:new for old,new,_ in pairs[:4]}
for old,new,converted in pairs:
 s=(A/old).read_text(encoding='utf8');s=route(s) if converted else s;s=normalize(s)
 for k,v in mapping.items():s=s.replace(k,v)
 s=s.replace('prepare_SparseAfter14829_round152_sources_v2_20261009','prepare_SparseAfter14829_round152_sources_v1_20261009')
 if old.startswith('run_SparseAfter14829_round'):
  s=s.replace('actual_registration_v2_20261009','actual_registration_receiver_v2_20261009').replace('full_registration_v2_file_IO','full_registration_receiver_v2_file_IO')
 compile(s,str(A/new),'exec')
 with (A/new).open('x',encoding='utf8') as f:f.write(s)
inputs=[Path(__file__),A/'prepare_SparseAfter148152_core_drafts_v1_20261009.py',*(A/o for o,_,_ in pairs),*(A/n for _,n,_ in pairs)]
create(A/'SparseAfter148152_complete_receiver_refinement_v3_20261009.json',{'status':'prepared_unadmitted152_complete_receiver_prototypes_with25_full75_cold60_native10_states',
 'input_sha256':{str(p):sha(p) for p in inputs},'quality_admitted':False,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
print({'prototypes':len(pairs),'quality_admitted':False})
