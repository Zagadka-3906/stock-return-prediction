"""Bind actual forecast duplicate evidence into128 source admission, scoring, publication and full registration before any quality execution."""
from pathlib import Path
import sys,time,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
META=A/'Pure149_duplicate_bound_receiver_preparation_v3_20261008.json'
DRIVERS={'verify_PureRFFHuber128_round149_sources_v2_20261008.py':'verify_PureRFFHuber128_round149_sources_v3_20261008.py','publish_PureRFFHuber128_evidence_v2_20261008.py':'publish_PureRFFHuber128_evidence_v3_20261008.py','run_PureRFFHuber128_round149_full_registration_v2_20261008.py':'run_PureRFFHuber128_round149_full_registration_v3_20261008.py'}
def execute(original,phase=None):
 for p,d in read(META)['input_sha256'].items():assert sha(p)==d,p
 import prepare_PureRFFHuber128_round149_sources_v2_20261008 as g
 paths=g.source_paths
 extras=[Path(__file__),META,*(A/n for n in DRIVERS.values()),A/'run_PureRFFHuber128_official_comparison_v2_20261008.py',A/'verify_Pure149_prior_complete_forecast_duplicate_audit_v1_20261008.py',A/'actual_Pure149_prior_complete_forecast_duplicate_audit_v1_20261008.json',A/'Pure149_prior_complete_forecast_duplicate_audit_raw_v1_20261008.json',A/'dispatch_PureRFFHuber149_complete_pipeline_v3_20261008.py']
 g.source_paths=lambda:list(dict.fromkeys([*(A/'run_PureRFFHuber128_official_comparison_v2_20261008.py' if p.name=='run_PureRFFHuber128_official_comparison_v1_20261008.py' else p for p in paths()),*[p for p in extras if p.exists()]]))
 p=A/original;ns={'__file__':str(A/DRIVERS[original]),'__name__':'actual_Pure149_duplicate_bound_receiver'};exec(compile(p.read_text(encoding='utf8'),str(p),'exec'),ns)
 if original.startswith('verify_'):
  ns['closed']('Pure149_prior_complete_forecast_duplicate_audit_v1_20261008')
  pointer=A/'actual_Pure149_prior_complete_forecast_duplicate_audit_v1_20261008.json';proof=Path(read(pointer)['output'])/'verification.json'
  assert sha(proof)==read(pointer)['verification_sha256'];target=A/'Pure149_prior_complete_forecast_duplicate_audit_raw_v1_20261008.json'
  assert not target.exists()
  with proof.open('rb') as src,target.open('xb') as dst:shutil.copyfileobj(src,dst)
  assert sha(target)==sha(proof)
  old_create=ns['create']
  def extended_create(path,value):
   if Path(path).name=='PureRFFHuber128_round149_source_admission_v1_20261008.json':
    value={**value,'input_sha256':{**value['input_sha256'],**{str(p):sha(p) for p in extras if p.exists()}},'actual_prior_complete_forecast_duplicate_audit':str(pointer),'actual128_scoring_receiver':str(A/'run_PureRFFHuber128_official_comparison_v2_20261008.py')}
   old_create(path,value)
  ns['create']=extended_create
 from PureRFFHuber149_storage_v1_20261008 import installed_transfer
 from verified_TLS_Git_retry_runtime_v2_20261008 import installed
 with installed(A/'Pure149_duplicate_bound_file_IO_v3_20261008'/DRIVERS[original].removesuffix('.py')),installed_transfer():
  if phase is None:ns['main']()
  else:ns['main'](phase)
def main():
 proof=A/'PureRFFHuber128_prospective_routes_v2_20261008.json';v=read(proof)
 assert v['actual_prospective_sources']==32 and v['actual_graph_controls']==992
 for p,d in v['input_sha256'].items():assert sha(p)==d,p
 originals=[];products=[]
 old=A/'run_PureRFFHuber128_official_comparison_v1_20261008.py';originals.append(old);s=old.read_text(encoding='utf8')
 needle=" empty(OUT);planpath=";assert s.count(needle)==1
 s=s.replace(needle," duplicate_path=A/'Pure149_prior_complete_forecast_duplicate_audit_raw_v1_20261008.json';duplicate=read(duplicate_path)\n assert duplicate['actual_current_cases']==124 and duplicate['known_semantic_control_count']==10\n duplicate_rows={r['control_case']:r for r in duplicate['records']}\n empty(OUT);planpath=")
 s=s.replace(' sources=[Path(__file__),',' sources=[Path(__file__),duplicate_path,A/\'prepare_Pure149_duplicate_bound_receivers_v3_20261008.py\',A/\'Pure149_duplicate_bound_receiver_preparation_v3_20261008.json\',')
 needle="   if known is not None:assert metrics==baselines[known]\n";assert s.count(needle)==1
 s=s.replace(needle,needle+"   if cfg['model'] is not None:\n    duplicate_row=duplicate_rows[cfg['joint_control_case']];assert duplicate_row['numeric_sha256']==numeric\n    for previous in duplicate_row['explicit147_148_semantic_matches']:assert metrics==previous['metrics']\n    for previous in duplicate_row['prior_full_board_matches']:\n     assert all(metrics[k]==value for k,value in previous['metrics'].items())\n     if previous['all8_metrics'] is not None:assert metrics==previous['all8_metrics']\n")
 s=s.replace('all181_full_and543_cold_and80_native_controls_passed','all124_full_and372_cold_and80_native_controls_passed')
 products.append(save('run_PureRFFHuber128_official_comparison_v2_20261008.py',s))
 for old,new in DRIVERS.items():
  originals.append(A/old);s="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom prepare_Pure149_duplicate_bound_receivers_v3_20261008 import execute\n"
  if old.startswith('publish_'):s+=f"if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute({old!r},p.parse_args().phase)\n"
  else:s+=f"if __name__=='__main__':execute({old!r})\n"
  products.append(save(new,s))
 old=A/'dispatch_PureRFFHuber149_complete_pipeline_v2_20261008.py';originals.append(old);s=old.read_text(encoding='utf8')
 for before,after in DRIVERS.items():s=s.replace(before,after)
 s=s.replace('run_PureRFFHuber128_official_comparison_v1_20261008.py','run_PureRFFHuber128_official_comparison_v2_20261008.py')
 s=s.replace(" for n in ('AdaptiveJoint", " for n in ('Pure149_prior_complete_forecast_duplicate_audit_v1_20261008','AdaptiveJoint",1)
 s=s.replace("('AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008','run_PureRFFHuber128_round149_full_registration_v3_20261008.py'","('PureRFFHuber128_round149_full_registration_v1_20261008','run_PureRFFHuber128_round149_full_registration_v3_20261008.py'")
 assert "('PureRFFHuber128_round149_full_registration_v1_20261008'" in s
 s=s.replace('complete_hidden_launches_v2','complete_hidden_launches_v3');products.append(save('dispatch_PureRFFHuber149_complete_pipeline_v3_20261008.py',s))
 create(META,{'status':'prepared128_actual_duplicate_metric_crosschecks_source_admission_and_all_full_QA60_receivers_before_any_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),proof,*originals,*products]},'all32_original_generated_routes_and992_graphs_and_selection_parameters_unchanged':True,'all_duplicate_numeric_bits_and_available_all8_official_metrics_must_match_prior':True,'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 p=products[-1];row=start('PureRFFHuber149_complete_chronological_dispatch_v3_20261008',p.name,[],{str(p):sha(p),str(META):sha(META),str(Path(__file__)):sha(__file__)})
 create(A/'Pure149_duplicate_bound_complete_hidden_launch_v3_20261008.json',row);print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
