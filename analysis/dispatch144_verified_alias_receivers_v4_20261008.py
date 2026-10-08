from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
def main():
    names=[('ConeRidgeAlpha100_selected_candidate_preparation_v9_20261008','prepare_ConeRidgeAlpha100_selected_candidate_v9_20261008.py'),('ConeRidgeAlpha100_selected_candidate_sealing_v9_20261008','seal_ConeRidgeAlpha100_selected_candidate_v9_20261008.py'),('ConeRidgeAlpha100_round144_full_registration_v10_20261008','run_ConeRidgeAlpha100_round144_full_registration_v10_20261008.py')]
    rows={};events=[]
    for name,driver in names:
        folder=A/'service_owned_workflows_20261006'/name
        if not (folder/'native_launch.json').exists():
            try:start(name,driver,[],{str(A/driver):sha(A/driver)})
            except AssertionError as error:events.append({'service':name,'launch_initial_identity_check':str(error)})
        row=read(folder/'native_launch.json')
        for attempt in range(20):
            if owned(row) or (folder/'service_execution.json').exists():break
            time.sleep(.25)
        assert row['actual_native_console_handle']==0 and not row['independent_launch_root_in_any_job'];assert Path(row['original_driver'])==A/driver
        assert owned(row) or read(folder/'service_execution.json')['status']=='passed',name
        rows[name]=row
    create(A/'actual144_verified_alias_receivers_dispatch_v4_20261008.json',{'status':'verified_three_actual_live_hidden_receivers_after_transient_launch_identity_race','launches':rows,'events':events,'actual_alias_nested_copy_control':str(A/'actual_short_parent_alias_nested_copy_v2_20261008.json'),'new_quality_scores':0})
    print(json.dumps({'started_or_verified':list(rows)},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
