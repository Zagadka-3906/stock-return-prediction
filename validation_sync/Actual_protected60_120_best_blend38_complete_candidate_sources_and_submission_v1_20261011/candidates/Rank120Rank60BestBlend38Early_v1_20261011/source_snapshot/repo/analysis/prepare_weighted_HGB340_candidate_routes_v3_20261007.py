"""Correct future candidate metadata and gates before admission, without altering V2."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    routes={f'{prefix}_flagged_HGB_weighted_quarters340_selected_candidate_v2_20261007':f'{prefix}_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007' for prefix in ('prepare','seal')}
    routes['weighted_flagged_HGB_full337_transform_preflight_v2']='weighted_flagged_HGB_full337_transform_preflight_v3'
    paths=[Path(__file__)]
    for prefix in ('prepare','seal'):
        old=A/f'{prefix}_flagged_HGB_weighted_quarters340_selected_candidate_v2_20261007.py'
        new=A/f'{prefix}_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007.py';assert not new.exists()
        text=substitute(old.read_text(encoding='utf8'),routes)
        if prefix=='prepare':
            assert text.count('expected_scored_records=88')==1
            text=text.replace('expected_scored_records=88','expected_scored_records=340').replace('best of66','best of340')
        compile(text,str(new),'exec')
        new.write_text(text,encoding='utf8',newline='\n');paths += [old,new]
    create(A/'weighted_HGB340_candidate_route_preparation_v3_20261007.json',{'status':'compiled_fresh_actual337_dependency_and340_complete_protocol',
        'input_sha256':{str(p):sha(p) for p in paths},'new_native_fits':0,'new_quality_scores':0})

if __name__=='__main__':main()
