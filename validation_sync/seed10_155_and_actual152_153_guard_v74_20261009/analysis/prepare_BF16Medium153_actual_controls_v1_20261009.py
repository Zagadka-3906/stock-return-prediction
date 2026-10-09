"""Prepare real medium neural controls; science waits for six own fits, never future X."""
from pathlib import Path
import sys, ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def save(name,text):
    path=A/name;compile(text,str(path),'exec')
    with path.open('x',encoding='utf8') as f:f.write(text)
    return path

def replace(s,old,new):
    assert old in s,old
    return s.replace(old,new)

def main():
    stage=(A/'BF16_complete_parent_native_stage_v1_20261008.py').read_text(encoding='utf8')
    for old,new in [('BF16_complete_parent_rank_CDF','BF16_medium2048_seed09_complete_parent_rank_CDF'),
      ('neural_BF16_micro8192_native_v1_20261008','neural_BF16_medium2048_seed09_e64_native_v1_20261009'),
      ('neural_BF16_independent_forward_v1_20261008','neural_BF16_medium2048_seed09_independent_forward_v1_20261009'),
      ('BF16_medium2048_seed09_complete_parent_rank_CDF_v1_20261008','BF16Medium153_complete_parent_rank_CDF_v1_20261009'),
      ("('model','role','weight','rank_universe','first2020_active')","('model','role','weight','sign','rank_universe','first2020_active')"),
      ("len(original['training_losses'])==32","len(original['training_losses'])==64"),
      ("spec['role'],spec['weight'])","spec['role'],spec['weight'],spec['sign'])"),
      ("'BF16_wide_full_'","'BF16_medium2048_seed09_full_'"),
      ("'role':spec['role'],'weight':spec['weight'],","'role':spec['role'],'weight':spec['weight'],'sign':spec['sign'],")]:stage=replace(stage,old,new)
    stage=replace(stage,"    assert spec['first2020_active']", "    assert spec['sign'] in (-1.,1.)\n    assert spec['first2020_active']")
    stage_path=save('BF16Medium153_complete_parent_native_stage_v1_20261009.py',stage)
    small=(A/'verify_BF16_independent_small_CPU_v1_20261008.py').read_text(encoding='utf8')
    for old,new in [('neural_BF16_micro8192_native_v1_20261008','neural_BF16_medium2048_seed09_e64_native_v1_20261009'),
      ('neural_BF16_independent_forward_v1_20261008','neural_BF16_medium2048_seed09_independent_forward_v1_20261009'),
      ("A / 'BF16_independent_small_CPU_preflight_v1_20261008'","Path('E:/赛题五_本机临时/BF16Medium153_independent_small_CPU_v1_20261009')"),
      ('actual_BF16_micro_restart_location_20261008','actual_BF16_medium2048_seed09_restart_location_v1_20261009')]:small=replace(small,old,new)
    small_path=save('verify_BF16Medium153_independent_small_CPU_v1_20261009.py',small)
    full=(A/'verify_BF16_full5_independent_GPU_v2_20261008.py').read_text(encoding='utf8')
    for old,new in [('neural_BF16_full5_independent_controls_v2_20261008','BF16Medium153_full5_independent_controls_v1_20261009'),
      ('actual_neural_BF16_micro8192_bank6_v2_20261008','actual_BF16_medium2048_seed09_e64_bank6_v1_20261009'),
      ('BF16_independent_small_CPU_preflight_v1_20261008','BF16Medium153_independent_small_CPU_v1_20261009'),
      ("A / 'BF16Medium153_independent_small_CPU_v1_20261009/verification.json'","Path('E:/赛题五_本机临时/BF16Medium153_independent_small_CPU_v1_20261009/verification.json')"),
      ('neural_BF16_independent_forward_v1_20261008','neural_BF16_medium2048_seed09_independent_forward_v1_20261009'),
      ('neural_BF16_micro8192_native_v1_20261008','neural_BF16_medium2048_seed09_e64_native_v1_20261009'),
      ('actual_BF16_micro8192_bank6_location_v2_20261008','actual_BF16_medium2048_seed09_e64_bank6_location_v1_20261009'),
      ('[16384, 8192, 4096]','[2048, 1024, 512]'),("len(bundle['training_losses']) == 32","len(bundle['training_losses']) == 64"),
      ('actual_BF16_full5_independent_location_v2_20261008','actual_BF16Medium153_full5_independent_location_v1_20261009'),
      ('passed_actual_full5_5635800_BF16_native_and_independent_GPU_forecasts_and10_cold_prefixes','passed_actual_full5_5635800_medium2048_BF16_native_and_independent_GPU_forecasts_and10_cold_prefixes')]:full=replace(full,old,new)
    full=replace(full,'Actual independent wide annual','Actual independent medium2048 annual')
    full_path=save('verify_BF16Medium153_full5_independent_GPU_v1_20261009.py',full)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in (Path(__file__),stage_path,small_path,full_path,A/'BF16Medium78_round153_proposal_v1_20261009.json')}
    create(A/'BF16Medium153_actual_controls_preparation_v1_20261009.json',{'status':'prepared_own_medium153_actual_decoder_and_all5_annual_controls_before_quality',
      'input_sha256':pins,'complete_six_native_states_not_yet_claimed':True,'actual_future_X_read':False,'test_labels_read':False})
    rows={}
    for name,path in [('BF16Medium153_independent_small_CPU_v1_20261009',small_path),('BF16Medium153_independent_full5_GPU_controls_v1_20261009',full_path)]:
        rows[name]=start(name,path.name,[],pins)
    create(A/'BF16Medium153_actual_independent_hidden_launches_v1_20261009.json',rows)
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)

if __name__=='__main__':main()
