"""Finalize actual admission service identity before any130 scoring; preserve unused V4 sources."""
from pathlib import Path
import sys,time,psutil
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    original=A/'run_nonflag_EmpiricalBayes40_admitted_comparison_v4_20261007.py';fresh=A/'run_nonflag_EmpiricalBayes40_admitted_comparison_v5_20261007.py'
    text=original.read_text(encoding='utf8');before="('nonflag_EmpiricalBayes40_round130_source_admission_v1','nonflag_EmpiricalBayes40_full37_controls_main_publication_v1')"
    assert text.count(before)==1
    text=text.replace(before,"('nonflag_EmpiricalBayes40_round130_source_admission_v4','nonflag_EmpiricalBayes40_full37_controls_main_publication_v1')")
    compile(text,str(fresh),'exec');assert not fresh.exists();fresh.write_text(text,encoding='utf8',newline='\n')
    oldqueue=A/'queue_nonflag_EmpiricalBayes130_after_actual129_v4_20261007.py';newqueue=A/'queue_nonflag_EmpiricalBayes130_after_actual129_v5_20261007.py'
    text=oldqueue.read_text(encoding='utf8').replace(repr(original.name),repr(fresh.name))
    needle='    for p,d in pins.items():assert sha(p)==d,p';assert text.count(needle)==2
    text=text.replace(needle,"    final=A/'nonflag_EmpiricalBayes130_actual_admission_gate_finalization_v5_20261007.json'\n    pins.update({**read(final)['input_sha256'],str(final):sha(final)})\n"+needle,1)
    compile(text,str(newqueue),'exec');assert not newqueue.exists();newqueue.write_text(text,encoding='utf8',newline='\n')
    assert not (A/'service_owned_workflows_20261006/nonflag_EmpiricalBayes40_round130_source_admission_v4').exists()
    assert not (A/'nonflag_EmpiricalBayes40_official_comparison_v1_20261007').exists()
    folder=A/'service_owned_workflows_20261006/nonflag_EmpiricalBayes40_actual130_after129_dependency_queue_v4';row=read(folder/'native_launch.json');assert owned(row)
    identities=[]
    for key,birth in [('owned_worker_pid','owned_worker_creation_time'),('pid','owned_parent_creation_time')]:
        proc=psutil.Process(row[key]);assert abs(proc.create_time()-row[birth])<.03;identities.append({'pid':proc.pid,'creation_time':proc.create_time(),'cmdline':proc.cmdline()})
    assert all('run_service_owned_windows_workflow_20261006.py' in ' '.join(p['cmdline']) for p in identities)
    for p in identities:psutil.Process(p['pid']).terminate()
    for p in identities:
        try:psutil.Process(p['pid']).wait(timeout=10)
        except psutil.NoSuchProcess:pass
    assert not owned(row)
    proof=A/'nonflag_EmpiricalBayes130_actual_admission_gate_finalization_v5_20261007.json'
    create(proof,{'status':'corrected_exact_actual_admission_service_tuple_before_any130_quality_scores','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,fresh,oldqueue,newqueue,*folder.glob('*.json'),*folder.glob('*.log')]},
      'administratively_superseded_waiting_V4_controller':identities,'V4_source_bytes_retained':True,'only_waiting_controller_terminated':True,
      'official_comparison_directory_absent_before_correction':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    pins={**read(proof)['input_sha256'],str(proof):sha(proof)}
    row=start('nonflag_EmpiricalBayes40_actual130_after129_dependency_queue_v5',newqueue.name,[],pins)
    create(A/'nonflag_EmpiricalBayes130_admission_gate_v5_hidden_launch_20261007.json',{'status':'started_actual130_finalized_admission_gate_dependency_queue','identity':row,'input_sha256':pins})

if __name__=='__main__':main()
