"""Queue independent small-CPU and complete five-year saved-tensor checks for own seed10."""
from pathlib import Path
import sys,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    inputs=[Path(__file__),A/'neural_BF16_medium2048_seed10_e64_frontier_v1_20261009.json',A/'BF16TwoSeed79_round154_proposal_v1_20261009.json'];targets=[]
    for name in ['verify_BF16Medium153_independent_small_CPU_v1_20261009.py','verify_BF16Medium153_full5_independent_GPU_v1_20261009.py']:
        original=A/name;target=A/name.replace('BF16Medium153','BF16TwoSeed154_seed10')
        s=original.read_text(encoding='utf8').replace('BF16Medium153','BF16TwoSeed154_seed10').replace('seed09','seed10')
        if 'small_CPU' in name:
            needle='def main():\n';assert s.count(needle)==1
            gate="    service=A/'service_owned_workflows_20261006/actual_BF16_medium2048_seed10_restart_control_v1_20261009'\n    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)\n    assert read(service/'service_execution.json')['status']=='passed'\n"
            s=s.replace(needle,needle+gate)
        compile(s,str(target),'exec');assert 'seed09' not in s and 'BF16Medium153' not in s
        with target.open('x',encoding='utf8') as f:f.write(s)
        inputs.extend((original,target));targets.append(target)
    meta=A/'BF16TwoSeed154_seed10_independent_controls_preparation_v1_20261009.json'
    create(meta,{'status':'prepared_own_seed10_small32_CPU_and_full5_GPU_independent_controls_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},
        'expected_full_rows_days_stocks':[5635800,1212,4650],'expected_full5_cold_controls':10,'expected_small_prefix_controls':4,
        'actual_controls_not_yet_claimed':True,'native_fits_by_controls':0,'official_scores':0,'future_X_read':False,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(meta):sha(meta),**{str(p):sha(p) for p in targets}}
    rows={'small':start('BF16TwoSeed154_seed10_independent_small_CPU_v1_20261009',targets[0].name,[],pins),
        'full':start('BF16TwoSeed154_seed10_independent_full5_GPU_controls_v1_20261009',targets[1].name,[],pins)}
    create(A/'BF16TwoSeed154_seed10_independent_hidden_launches_v1_20261009.json',rows);print({k:v['owned_worker_pid'] for k,v in rows.items()},flush=True)
if __name__=='__main__':main()
