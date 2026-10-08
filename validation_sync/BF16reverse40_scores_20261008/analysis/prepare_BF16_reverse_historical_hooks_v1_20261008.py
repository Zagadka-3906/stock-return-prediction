"""Queue actual saved-neural reverse native hooks after admitted complete-parent full controls."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    source=A/'verify_BF16_complete_parent_native_hook3_v1_20261008.py';target=A/'verify_BF16_reverse_complete_parent_native_hook3_v1_20261008.py'
    text=source.read_text(encoding='utf8')
    mapping={'BF16_complete_parent_native_hook3_v1_20261008':'BF16_reverse_complete_parent_native_hook3_v1_20261008',
        'BF16_rank_CDF_actual_full37_controls_v1_20261008':'BF16_reverse_rank_CDF_actual_full37_controls_v1_20261008',
        'BF16_complete_parent_native_stage_v1_20261008':'BF16_reverse_complete_parent_native_stage_v1_20261008',
        'BF16_complete_parent_rank_CDF_v1_20261008':'BF16_reverse_complete_parent_rank_CDF_v1_20261008',
        'actual_BF16_rank_CDF_full37_location_v1_20261008':'actual_BF16_reverse_rank_CDF_full37_location_v1_20261008',
        'passed_actual37_full5635800_BF16_rank_CDF_independent_and111_cold_controls':'passed_actual37_full5635800_reverse_BF16_CDF_independent_and111_cold_controls',
        'passed_actual3_historical_BF16_full_native_independent_CDF_and_whole_day_prefix_hooks':'passed_actual3_historical_reverse_BF16_native_independent_CDF_and_day_prefix_hooks',
        'actual_BF16_native_hook3_location_v1_20261008':'actual_BF16_reverse_native_hook3_location_v1_20261008'}
    for before,after in mapping.items():text=text.replace(before,after)
    needle="'first2020_active':True,'position':'after_complete_qualified_parent'}";assert text.count(needle)==1
    text=text.replace(needle,"'first2020_active':True,'position':'after_complete_qualified_parent',\n              'signal_sign_on_valid_rows':-1.,'invalid_signal_bits_preserved':True}")
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    paths=[Path(__file__),source,target,A/'BF16_reverse_native_receiver_preparation_v1_20261008.json',
        A/'BF16_reverse_complete_parent_native_stage_v1_20261008.py',A/'predict_BF16_reverse_complete_parent_scheme_v1_20261008.py',
        A/'BF16_reverse_complete_parent_rank_CDF_v1_20261008.py',A/'BF16reverse40_round138_plan_v1_20261008.json']
    pins={str(p):sha(p) for p in paths}
    row=start('BF16_reverse_complete_parent_actual_historical_native_hook3_v1_20261008',target.name,[],pins)
    create(A/'actual_BF16_reverse_historical_native_hook3_hidden_launch_v1_20261008.json',{
        'status':'queued_actual3_reverse_saved_native_historical_hooks_after_complete137_parent_and37_full111_cold_controls',
        'identity':row,'input_sha256':pins,'new_fits':0,'actual_quality_scores':0,'test_labels_read':False,
        'actual_future_inference_and_full138_source_admission_not_claimed':True})
    print('Actual3 historical reverse saved-neural hooks queued; GPU work remains serial.',flush=True)


if __name__=='__main__':main()
