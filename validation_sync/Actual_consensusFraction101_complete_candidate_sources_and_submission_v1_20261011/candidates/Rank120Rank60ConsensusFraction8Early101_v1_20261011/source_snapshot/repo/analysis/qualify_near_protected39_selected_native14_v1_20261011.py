"""Reuse verified identical37 native14 controls, or execute changed39 selection."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from compute_near_protected39_selected_native14_v1_20261011 import OUT

def main():
    assert allowed();closed('actual_near_protected39_after189_normalization_v1_20261011')
    pointer=A/'actual_near_protected_complete39_after189_location_v1_20261011.json'
    pilot_path=Path(read(pointer)['output'])/'pilot39.json';pilot=read(pilot_path);best=pilot['best'];cfg=best['configuration']
    assert len(pilot['records'])==39
    if cfg['model'] is None:
        from compute_near_protected39_selected_native14_v1_20261011 import main as compute
        compute();return
    closed('actual_rank5_rank20_near_protected_selected_native14_v1_20261011')
    source=Path('E:/赛题五_本机临时/rank5_rank20_near_protected_selected_native14_v1_20261011/verification.json')
    previous=read(source);old=previous['best']['configuration']
    keys=('role','weight','sign','protect_fraction','rank5_weight')
    identical=old['kind']==cfg['codec'] and all(old[k]==cfg[k] for k in keys)
    if not identical:
        from compute_near_protected39_selected_native14_v1_20261011 import main as compute
        compute();return
    assert (previous['actual_native_cases'],previous['actual_cold_cases'],len(previous['prefit_rejections']))==(14,14,7)
    assert previous['actual_saved_states']==12
    for row in previous['records']:
        spec=row['configuration']
        assert spec['codec']==cfg['codec'] and spec['recipe']==cfg['recipe']
        assert all(spec[k]==cfg[k] for k in keys if k!='sign')
        assert spec['sign'] in (-1.,1.) and spec['original_complete_parent_round']==175
        assert row['native_independent_and_cold_bits_exact']
    pins={**pilot['input_sha256'],**previous['input_sha256'],str(source):sha(source),str(pointer):sha(pointer),str(pilot_path):sha(pilot_path),str(Path(__file__)):sha(__file__)}
    for p,d in pins.items():assert sha(p)==d,p
    assert allowed();OUT.mkdir(exist_ok=False)
    create(OUT/'pilot39.json',{**pilot,'input_sha256':pins,'normalization_source':str(pilot_path)})
    create(OUT/'verification.json',{'status':'passed_selected_near_protected39_six_pairs14_native14_cold7_prefit_refusals','best':best,'input_sha256':pins,'records':previous['records'],'prefit_rejections':previous['prefit_rejections'],'actual_saved_states':12,'actual_native_cases':14,'actual_cold_cases':14,'new_native_cases_by_this_qualifier':0,'qualification_mode':'verified_existing_identical_spec_parent175_native14','verified_native_source':str(source),'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,'full190_candidate_and_registration_pending':True})
    create(A/'actual_near_protected39_selected_native14_location_v1_20261011.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()
