"""Publish actual153 route controls and the verified race/binding repairs through the serial main lock."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    old=A/'publish_medium153_fulltraining_main_v63_20261009.py';new=A/'publish_actual_serial_and153_prospective_main_v64_20261009.py'
    s=old.read_text(encoding='utf8').replace('medium153_fulltraining_main_v63','actual_serial_and153_prospective_main_v64').replace('medium153_fulltraining_v63','actual_serial_and153_prospective_v64').replace('medium153_fulltraining_safe_publication_v63','actual_serial_and153_prospective_safe_publication_v64')
    needle=" sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)";assert s.count(needle)==1
    addition=""" closed('HuberSparse59_controls_main_publication_v2_20261009')
 sources.extend(A/n for n in ('prepare_medium153_fulltraining_main_v63_20261009.py','medium153_fulltraining_main_v63_receipt_20261009.json',
  'github_validation_sync_main_20261005/round149_receipt.json','optimization_20261003_r149/full_registration_execution.json',
  'serial_main_publication_mutex_v1_20261009.py','serial_main_publication_mutex_v1_20261009.json',
  'verify_serial_main_publication_mutex_v1_20261009.py','HuberSparse150_serial_publication_recovery_v18_20261009.json',
  'HuberSparse150_data_path_bindings_v20_20261009.json','future151to153_serial_receiver_binding_v21_20261009.json',
  'future_service_and_data_namespaces_v22_20261009.json','BF16Medium78_prospective_routes_v1_20261009.json',
  'actual_serial_pipeline_progress_hidden_launch_v57_20261009.json','actual_serial_pipeline_progress_handoff_v57_20261009.json',
  'latest_actual_optimization_progress_pointer_v57_20261009.json','prepare_actual_serial_pipeline_progress_v57_20261009.py',
  'monitor_actual_chronological_optimization_progress_v57_20261009.py'))
 for n in ('serial_main_publication_mutex_v1_20261009.json','HuberSparse150_serial_publication_recovery_v18_20261009.json',
  'HuberSparse150_data_path_bindings_v20_20261009.json','future151to153_serial_receiver_binding_v21_20261009.json',
  'future_service_and_data_namespaces_v22_20261009.json','BF16Medium78_prospective_routes_v1_20261009.json'):
  for f,d in read(A/n)['input_sha256'].items():
   assert sha(f)==d,f
   if Path(f).suffix in ('.py','.json','.log','.md'):sources.append(Path(f))
 for pattern in ('*HuberSparse150*recovery*v18*20261009.json','*HuberSparse150*bindings*v20*20261009.json',
  'future*serial*20261009.json','future*namespace*20261009.json','*BF16Medium*20261009.json','*BF16Medium*20261009.py'):
  sources.extend(p for p in A.glob(pattern) if p.is_file())
 for version,date in ((1,'20261008'),(2,'20261009'),(3,'20261009')):
  for stem in ('controls_main_publication','official_comparison','scores_main_publication','selected_candidate_preparation','selected_candidate_sealing','round150_full_registration'):
   f=A/'service_owned_workflows_20261006'/f'HuberSparse59_{stem}_v{version}_{date}'
   if not f.is_dir():continue
   sources.extend(f/n for n in ('job_definition.json','native_launch.json','verified_hidden_launch.json'))
   if (f/'service_execution.json').exists():sources.extend(f/n for n in ('service_execution.json','stdout.log','stderr.log'))
 p=read(A/'serial_main_publication_mutex_v1_20261009.json');f=Path(p['output'])/'verification.json'
 assert sha(f)==p['verification_sha256'];sources.extend([f,*f.parent.glob('worker*.json')])
"""
    s=s.replace(needle,addition+needle)
    s=s.replace('actual_medium153_six_states_native42_full73_training_and219_prefixes_before_quality','actual153_40_prospective1500_graphs_and_serial_publication_recovery_with_unchanged_science')
    s=s.replace("'actual_medium153_full5_independent_rows':5635800", "'actual153_prospective_sources':40,'actual153_prospective_graph_controls':1500,'actual153_baseline_controls':15,'actual153_physical_model_tie_controls':10,'actual_serial_mutex_overlapping_processes':2,'actual_future_typed_namespace_checks':24,'failed150_publication_and_binding_records_retained':True,'actual_medium153_full5_independent_rows':5635800")
    s=s.replace('同步153完整训练73组合及219前缀验证，正式质量准入待完成','同步153的40程序1500图检查及串行发布和路径绑定修复，保留全部失败记录')
    needle="with safe(Path('E:/赛题五_本机临时/actual_serial_and153_prospective_safe_publication_v64_20261009')):main()";assert s.count(needle)==1
    s=s.replace(needle,"from serial_main_publication_mutex_v1_20261009 import installed as serial\n log=Path('E:/赛题五_本机临时/actual_serial_and153_prospective_safe_publication_v64_20261009')\n with safe(log),serial(log/'serial_publication_mutex.json'):main()")
    compile(s,str(new),'exec')
    with new.open('x',encoding='utf8') as f:f.write(s)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('actual_serial_and153_prospective_main_publication_v64_20261009',new.name,[],{str(new):sha(new),str(Path(__file__)):sha(__file__)})
    create(A/'actual_serial_and153_prospective_main_hidden_launch_v64_20261009.json',row);print(row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
