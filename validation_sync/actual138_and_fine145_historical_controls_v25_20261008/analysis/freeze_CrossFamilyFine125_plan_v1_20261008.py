"""Freeze an uncovered grid and distinct fixed stage/comparison parents; never claim complete receiver admission."""
from pathlib import Path
import sys,json,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    source=A/'CrossFamilyFine125_round145_proposal_v1_20261008.json';p=read(source)
    assert p['anchor_rounds']==[134,136,141,144] and p['scientific_stage_base_round']==134 and len(p['new_cases'])==120
    previous=read(A/'CrossFamily94_round136_plan_v1_20261008.json')
    old={(r['group'],r['share'],r['amplitude']) for r in previous['new_cases']}
    assert not old & {(r['group'],r['share'],r['amplitude']) for r in p['new_cases']}
    infos=[]
    for h,r in p['heads'].items():
        for year,path in r['infos'].items():
            info=read(path);assert info['year']==int(year) and info['last_training_label_date']<info['exclusive_cutoff'] and info['last_training_label_end']<=info['exclusive_cutoff']
            infos.append(Path(path))
    inputs=[Path(__file__),source,A/'CrossFamily94_round136_plan_v1_20261008.json',A/'CrossFamilyFine_complete_parent_CDF_v1_20261008.py',A/'CrossFamilyFine_complete_parent_native_stage_v1_20261008.py',ROOT/'evaluate.py',ROOT/'后续选模标准.md',*infos]
    assert len(infos)==20 and sha(ROOT/'evaluate.py')=='72dc59987e92ba8ae6b506e114dfe8591b5608c9beccd0769d5d1f778f9189c2'
    plan={**p,'status':'frozen_uncovered125_case_grid_with_complete145_receiver_admission_still_required','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'QA_version':56,'wave':428,'existing_saved_native_heads':20,'actual_full_OOF_heads':4,
        'fixed_scientific_stage_base_round':134,'comparison_parent_rule':'maximum_official_S_then_unique_physical_model_SHA_count_then_round_among_all_four_qualified_anchors',
        'new_stage_first2020_identity':True,'graph_key':'nonflag_CPU_CrossFamily_complete_parent_CDF',
        'retune_existing_stage_requires_reconstructing_134_then_replace_stage_once':True,
        'retuning_must_not_append_a_second_stage_over_136_or_141_or_144':True,
        'score_gain_baseline_is_current_best_qualified_anchor_not_fixed_stage_base':True,
        'candidate_anchor_reuse_or_new_native_inference_chosen_only_after_all125_scores':True,
        'original_proposal_sha256':sha(source),'input_sha256':{**p['input_sha256'],**{str(f):sha(f) for f in inputs}},
        'quality_scoring_not_admitted_or_dispatched':True,'new_official_scores':0,'actual_test_labels_read':False}
    out=A/'CrossFamilyFine125_round145_plan_v1_20261008.json';create(out,plan)
    print(json.dumps({'frozen_plan':str(out),'new_cases':120,'existing_native_models':20,'complete_receivers_and_source_preflight_still_required':True}),flush=True)
if __name__=='__main__':main()
