"""Bound optional benchmark RAM waiting; replace only proved idle benchmark/dispatch processes before any146 score."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def save(n,s):
 p=A/n;compile(s,str(p),'exec')
 with p.open('x',encoding='utf8',newline='') as f:f.write(s)
 return p
def main():
 originals=[];products=[]
 source=A/'verify_deferred_full_board_QA_v1_20261008.py';originals.append(source)
 products.append(save('verify_deferred_full_board_QA_v2_20261008.py',source.read_text(encoding='utf8').replace('serialization_benchmark_v1_20261008','serialization_benchmark_v2_20261008').replace('full_board_deferred_QA_v1_20261008','full_board_deferred_QA_v2_20261008')))
 source=A/'benchmark_deferred_full_board_serialization_v1_20261008.py';originals.append(source);s=source.read_text(encoding='utf8')
 s=s.replace('serialization_benchmark_v1_20261008','serialization_benchmark_v2_20261008').replace('verify_deferred_full_board_QA_v1_20261008','verify_deferred_full_board_QA_v2_20261008')
 first=s.index('    # New full-board encodes need ample RAM.');last=s.index('\n\ndef load_report',first)
 s=s[:first]+'''    # Preserve the24GiB start threshold; give optional RAM waiting a finite300second budget.
    resource=Path('E:/赛题五_本机临时/full_board_deferred_resource_budget_v2_20261008')
    resource.mkdir(exist_ok=False)
    tick=time.monotonic();samples=[]
    while True:
        available=psutil.virtual_memory().available
        samples.append({'elapsed_seconds':time.monotonic()-tick,'available_bytes':available,'total_bytes':psutil.virtual_memory().total})
        if available>=24*2**30:break
        if time.monotonic()-tick>=300:
            create(resource/'verification.json',{'status':'actual_optional_benchmark_not_admitted_due_to300second_24GiB_RAM_boundary',
                'samples':samples,'minimum_required_available_bytes':24*2**30,'benchmark_encodes_executed':0,
                'new_model_fits':0,'new_quality_scores':0,'new_runtime_adopted':False,'test_labels_read':False})
            raise RuntimeError('Actual24GiB start resource unavailable throughout300seconds; optional speed benchmark withdrawn; model146 may continue unchanged.')
        time.sleep(15)
    create(resource/'verification.json',{'status':'actual_optional_benchmark_admitted_at_original24GiB_threshold','samples':samples,'new_quality_scores':0})
    assert psutil.disk_usage('E:/').free>30*2**30
''' + s[last:]
 products.append(save('benchmark_deferred_full_board_serialization_v2_20261008.py',s))
 source=A/'dispatch_HuberCrossFamilyFine146_complete_pipeline_v3_20261008.py';originals.append(source);s=source.read_text(encoding='utf8')
 s=s.replace('actual_full_board_deferred_serialization_benchmark_v1_20261008','actual_full_board_deferred_serialization_benchmark_v2_20261008')
 s=s.replace('execution_cost_slot_handoff_v1_20261008','execution_cost_slot_handoff_v2_20261008').replace('complete_hidden_launches_v1_20261008','complete_hidden_launches_v2_20261008')
 needle="    pins={str(Path(__file__)):sha(__file__),str(p):sha(p)};rows={}"
 assert s.count(needle)==1;s=s.replace(needle,"    recovery=A/'actual_idle_optional_benchmark_handoff_v2_20261008.json'\n    pins={str(Path(__file__)):sha(__file__),str(p):sha(p),str(recovery):sha(recovery)};rows={}")
 products.append(save('dispatch_HuberCrossFamilyFine146_complete_pipeline_v4_20261008.py',s))
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 rows=[]
 try:
  for name,needle in [('actual_full_board_deferred_serialization_benchmark_v1_20261008','    gate (benchmark_deferred_full_board_serialization_v1_20261008.py:'),
                      ('HuberCrossFamilyFine146_complete_chronological_dispatch_v3_20261008','    closed (dispatch_HuberCrossFamilyFine146_complete_pipeline_v3_20261008.py:')]:
   row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json');assert owned(row)
   parent,worker,proof=suspended_idle(row,needle)
   rows.append({'launch':row,'idle_stack':proof,'parent':parent,'worker':worker})
  assert not (A/'service_owned_workflows_20261006/HuberCrossFamilyFine125_official_comparison_v2_20261008').exists()
  for row in rows:
   row['worker'].terminate();row['parent'].terminate()
  import psutil
  _,alive=psutil.wait_procs([p for r in rows for p in (r['worker'],r['parent'])],timeout=10);assert not alive
  for row in rows:assert not owned(row['launch'])
  record=A/'actual_idle_optional_benchmark_handoff_v2_20261008.json'
  pins={str(p):sha(p) for p in [Path(__file__),*originals,*products]}
  create(record,{'status':'cancelled_only_unstarted_proved_idle_benchmark1_and_dispatch3_before_replacing_with_finite_resource_wait',
   'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'cancelled':[{'launch':r['launch'],'idle_stack':r['idle_stack']} for r in rows],
   'old_benchmark_data_encodes':0,'all_original_sources_and_old_logs_preserved':True,'scientific_fit_scoring_or_inference_processes_stopped':0,
   'resource_threshold_bytes':24*2**30,'optional_memory_wait_budget_seconds':300,'new_quality_scores':0,'test_labels_read':False})
  pins[str(record)]=sha(record)
  from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
  b=start('actual_full_board_deferred_serialization_benchmark_v2_20261008',products[1].name,[],pins)
  d=start('HuberCrossFamilyFine146_complete_chronological_dispatch_v4_20261008',products[2].name,[],pins)
  create(A/'actual_resource_bounded_serialization_handoff_hidden_launches_v2_20261008.json',{'benchmark':b,'dispatch':d,'input_sha256':pins})
  print(json.dumps({'benchmark':b['owned_worker_pid'],'dispatch':d['owned_worker_pid']}),flush=True)
 finally:
  for row in rows:
   for proc in (row['worker'],row['parent']):
    if proc.is_running():proc.resume()
if __name__=='__main__':main()
