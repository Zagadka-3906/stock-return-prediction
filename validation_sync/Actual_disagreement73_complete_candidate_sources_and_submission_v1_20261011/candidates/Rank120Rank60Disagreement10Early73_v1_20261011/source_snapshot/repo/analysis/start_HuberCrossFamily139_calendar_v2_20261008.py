"""Dispatch the unchanged calendar receiver; preserve the original missing-pins call."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    proof=A/'HuberCrossFamily139_native_receiver_preflight_v1_20261008.json'
    control=read(proof);assert len(control['adapter_controls'])==5
    for path,digest in control['input_sha256'].items():assert sha(path)==digest,path
    name='HuberCrossFamily_multiyear_native_calendar_v1_20261008'
    assert not (A/'service_owned_workflows_20261006'/name).exists()
    failure=A/'HuberCrossFamily139_calendar_dispatch_failure_v1_20261008.json'
    create(failure,{'status':'preserved_before_any_calendar_launch_or_quality',
        'failed_source_sha256':sha(A/'prepare_HuberCrossFamily139_native_preflight_v1_20261008.py'),
        'reason':'Dispatcher omitted the required source pins argument after all five adapter tests passed.',
        'scientific_receiver_and_plan_unchanged':True,'new_official_scores':0,'test_labels_read':False})
    pins={**control['input_sha256'],**{str(path):sha(path) for path in (Path(__file__),proof,failure)}}
    launch=start(name,'verify_HuberCrossFamily_multiyear_native_calendar_v1_20261008.py',[],pins)
    create(A/'actual_HuberCrossFamily139_calendar_hidden_launch_v2_20261008.json',{
        'status':'started_actual18_calendar_and36_day_controls_on_training_X_only',
        'input_sha256':pins,'launch':launch,'new_official_scores':0,'test_labels_read':False})
    print('Unchanged historical calendar receiver launched consoleless with pinned source bytes.',flush=True)


if __name__=='__main__':main()
