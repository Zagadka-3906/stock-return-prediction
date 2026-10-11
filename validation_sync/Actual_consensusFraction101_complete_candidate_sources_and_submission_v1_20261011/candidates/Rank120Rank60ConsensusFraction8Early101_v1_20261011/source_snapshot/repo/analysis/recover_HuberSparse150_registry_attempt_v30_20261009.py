"""Retain the failed registry preflight and give the resumed attempt its own evidence file."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'HuberSparse150_registry_attempt_v30_20261009.json'
DRIVER='run_HuberSparse59_round150_full_registration_recovery_v30_20261009.py'
def routed(s):
    return BASE_ROUTE(s).replace('HuberSparse59_round150_full_registration_v7_20261009','HuberSparse59_round150_full_registration_v8_20261009').replace('actual_registration_recovery_v29','actual_registration_recovery_v30').replace('recovery_v29_file_IO','recovery_v30_file_IO').replace('HuberSparse59_actual_source_paths_before_registration_20261008.json','HuberSparse59_actual_source_paths_before_registration_retry30_20261009.json')
def execute():
    global BASE_ROUTE
    m=read(META)
    for f,d in m['input_sha256'].items():assert sha(f)==d,f
    import recover_HuberSparse150_partial_registry_v29_20261009 as previous
    BASE_ROUTE=previous.routed;previous.routed=routed;oldread=previous.read;olddriver=previous.DRIVER;previous.DRIVER=DRIVER
    def bound(p):
        v=oldread(p)
        if Path(p)==previous.META:v={**v,'input_sha256':{**v['input_sha256'],**m['input_sha256'],str(META):sha(META)}}
        return v
    previous.read=bound
    try:previous.execute()
    finally:previous.read=oldread;previous.routed=BASE_ROUTE;previous.DRIVER=olddriver
def main():
    folder=A/'service_owned_workflows_20261006/HuberSparse59_round150_full_registration_v7_20261009'
    assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='failed'
    target=A/DRIVER
    with target.open('x',encoding='utf8') as f:f.write("from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_HuberSparse150_registry_attempt_v30_20261009 import execute\nif __name__=='__main__':execute()\n")
    inputs=[Path(__file__),target,A/'HuberSparse150_partial_registry_v29_20261009.json',A/'recover_HuberSparse150_partial_registry_v29_20261009.py',
        A/'HuberSparse59_actual_source_paths_before_registration_20261008.json',*(folder/n for n in ('job_definition.json','native_launch.json','service_execution.json','stderr.log'))]
    create(META,{'status':'prepared_new_registry_attempt_evidence_without_overwriting_original_failure','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':{str(p):sha(p) for p in inputs},'quality_scores_repeated':0,'native_fits_repeated':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('HuberSparse59_round150_full_registration_v8_20261009',DRIVER,[],{str(META):sha(META),str(target):sha(target)})
    create(A/'HuberSparse150_registry_attempt_hidden_launch_v30_20261009.json',row);print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
