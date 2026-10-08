"""Preserve passed8 probes and failed bank1; correct only the accidental400k pointer in fresh2."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    service=A/'service_owned_workflows_20261006/nonflag_ConeRidgeAlpha8_64_bank40_v1_20261008'
    assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='failed'
    assert 'actual400k_location' in (service/'stderr.log').read_text(encoding='utf8')
    old=A/'train_nonflag_ConeRidgeAlpha8_64_bank40_v1_20261008.py';target=A/'train_nonflag_ConeRidgeAlpha8_64_bank40_v2_20261008.py'
    text=old.read_text(encoding='utf8').replace('actual400k','actual200k').replace('bank40_v1_20261008','bank40_v2_20261008').replace('bank40_plan_v1_20261008','bank40_plan_v2_20261008').replace('bank40_location_v1_20261008','bank40_location_v2_20261008')
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    causal1=A/'verify_ConeRidgeAlpha40_causal_refit_v1_20261008.py';causal2=A/'verify_ConeRidgeAlpha40_causal_refit_v2_20261008.py'
    value=causal1.read_text(encoding='utf8').replace('bank40_v1_20261008','bank40_v2_20261008').replace('bank40_location_v1_20261008','bank40_location_v2_20261008').replace('causal_refit_v1_20261008','causal_refit_v2_20261008').replace('causal_refit_location_v1_20261008','causal_refit_location_v2_20261008')
    assert not causal2.exists();compile(value,str(causal2),'exec');causal2.write_text(value,encoding='utf8',newline='\n')
    small=A/'actual_nonflag_ConeRidgeAlpha8_64_small_location_v1_20261008.json';pointer=A/'actual_nonflag_ConeRidgeAlpha8_64_actual200k_location_v1_20261008.json'
    small_proof=Path(read(small)['output'])/'verification.json';probe=Path(read(pointer)['output'])/'verification.json'
    p=read(probe);assert p['actual_probe_native_fits']==8 and p['actual_official_scores']==0
    assert all(r['actual_dense_BVLS_coefficients_and_intercept_close'] and r['native_reload_decoder_six_prefixes_bits_exact'] for r in p['records'])
    assert read(small_proof)['actual_synthetic_native_fits']==24
    for path,digest in p['input_sha256'].items():assert sha(path)==digest,path
    sources=[Path(__file__),old,target,causal1,causal2,small,small_proof,pointer,probe,service/'native_launch.json',service/'service_execution.json',service/'stderr.log']
    old_plan=A/'nonflag_ConeRidgeAlpha8_64_bank40_plan_v1_20261008.json';plan=read(old_plan)
    plan.update(status='frozen_actual_passed8_200003_probes_before_fresh40_annual_fits',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),input_sha256={**plan['input_sha256'],**{str(p):sha(p) for p in [*sources,old_plan]}},
        original_failed_bank1_preserved=True,actual_synthetic24_and_actual200003_eight_native_BVLS_controls_passed=True,
        probe_pointer_correction_only_not_native_fit_math_change=True)
    plan2=A/'nonflag_ConeRidgeAlpha8_64_bank40_plan_v2_20261008.json';create(plan2,plan)
    driver=A/'run_ConeRidgeAlpha8_actual_bank_after143_preparation_v2_20261008.py'
    body='''"""Avoid competing with ongoing143 full candidate inference; then execute fresh40 own-window fits."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
def main():
    service=A/'service_owned_workflows_20261006/ConeRidgeFine68_selected_candidate_preparation_v1_20261008'
    while owned(read(service/'native_launch.json')):time.sleep(10)
    assert read(service/'service_execution.json')['status']=='passed'
    from train_nonflag_ConeRidgeAlpha8_64_bank40_v2_20261008 import main as bank
    bank()
if __name__=='__main__':main()
'''
    assert not driver.exists();compile(body,str(driver),'exec');driver.write_text(body,encoding='utf8',newline='\n')
    create(A/'ConeRidgeAlpha8_probe_pointer_recovery_v2_20261008.json',{
        'status':'passed_eight_actual200003_probes_preserved_and_fresh40_bank2_prepared',
        'input_sha256':{str(p):sha(p) for p in [*sources,old_plan,plan2,driver]},
        'original_failure':'bulk actual20->actual40 replacement changed actual200k pointer to nonexistent actual400k',
        'native_solver_and_all_dense_comparison_tolerances_unchanged':True,'actual_annual_fits_before_recovery':0,
        'new_official_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in [*sources,plan2,driver]};rows={}
    for name,path in (('nonflag_ConeRidgeAlpha8_64_bank40_v2_20261008',driver),('ConeRidgeAlpha40_causal_refit_v2_20261008',causal2)):
        rows[name]=start(name,path.name,[],pins)
    create(A/'ConeRidgeAlpha8_actual_controls_hidden_launches_v2_20261008.json',{
        'status':'started_fresh40_fits_after_passed8_probes_and143_candidate_preparation_then40_causal_controls',
        'input_sha256':pins,'launches':rows,'training_workers_changed':0,'new_quality_scores':0})
    print('Fresh alpha bank2 and causal2 queued after143 candidate; real8 probe evidence retained.',flush=True)
if __name__=='__main__':main()
