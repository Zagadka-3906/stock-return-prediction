"""Launch all seven frozen155 phases after complete154 and its whole-forecast hash audit."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(name):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(15)
    assert read(f/'service_execution.json')['status']=='passed',name
def main():
    meta=A/'BF16Drop05_156_complete_pipeline_preparation_v3_20261009.json';m=read(meta)
    for name in ('BF16Drop05_156_complete_prospective_controls_v1_20261009','BF16Seed10_80_round155_full_registration_v1_20261009',
        'BF16Drop05_156_prior_complete_forecast_duplicate_audit_v1_20261009'):closed(name)
    for f,d in m['input_sha256'].items():assert sha(f)==d,f
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(meta):sha(meta),str(Path(__file__)):sha(__file__)};rows={}
    for name,driver,args in m['receiver_specs']:rows[name]=start(name,driver,args,{**pins,str(A/driver):sha(A/driver)})
    create(A/'BF16Drop05_156_complete_hidden_launches_v3_20261009.json',{'status':'started_seven_verified155_receivers_after_actual155_and_duplicate_audit',
        'launches':rows,'input_sha256':pins,'stage_base_round':148,'expected_quality_cases':81,'QA_version':67,
        'new_quality_scores_by_dispatch':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'started_receivers':list(rows)},flush=True)
if __name__=='__main__':main()
