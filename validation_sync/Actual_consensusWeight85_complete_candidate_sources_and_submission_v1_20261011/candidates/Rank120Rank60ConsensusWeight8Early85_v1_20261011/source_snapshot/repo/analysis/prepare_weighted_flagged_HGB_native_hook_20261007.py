"""Generate unique-native weighted replay; preserve the original immutable equal-mean helper."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    source=A/'predict_conditional_CPU_HGB_residual_CDF_scheme_20261007.py'
    target=A/'predict_flagged_CPU_HGB_weighted_quarters_scheme_20261007.py';assert not target.exists()
    plan=A/'flagged_HGB_weighted_quarters340_plan_20261007.json';assert len(read(plan)['ensembles'])==28
    text=source.read_text(encoding='utf8')
    changes={
        'from cpu_conditional_residual_hgb_codec_20261007 import predict_native, predict_decoded':'from cpu_numerical_HGB_large_batch_codec_v2_20261007 import predict_native, predict_decoded',
        "assert [c['name'] for c in components] == spec['ordered_equal_mean_components']":"ordered = spec['ordered_equal_mean_components']\n    assert len(ordered) == 4 and len(set(ordered)) == len(components)\n    assert [c['name'] for c in components] == list(dict.fromkeys(ordered))\n    assert 2 <= len(components) <= 3",
        '        controls = []':'        controls = []\n        native_heads, decoded_heads = {}, {}',
        '                combined += primary\n                decoded_combined += decoded':"                native_heads[component['name']] = primary\n                decoded_heads[component['name']] = decoded",
        '        combined /= len(components)\n        decoded_combined /= len(components)':"        for name in ordered:\n            combined += native_heads[name]\n            decoded_combined += decoded_heads[name]\n        combined /= len(ordered)\n        decoded_combined /= len(ordered)",
        "'fixed_padded_inference_batch': 256":"'fixed_padded_inference_batch': 8192",
        "'CPU_HGB_residual_CDF_native_replay_verification.json'":"'weighted_quarters_HGB_native_replay_verification.json'",
        'passed_actual_parent15_and_selected_CPU_HGB_full_two_replays_independent_decoder_and_cold80':'passed_actual_parent15_and_unique_weighted_quarters_HGB_full_two_replays_independent_decoder_and_cold80',
    }
    for before,after in changes.items():
        assert text.count(before)==1,before
        text=text.replace(before,after)
    compile(text,str(target),'exec')
    with target.open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    lower_source=A/'predict_protected_upper_pool_CPU_HGB_scheme_20261007.py'
    lower_target=A/'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_20261007.py';assert not lower_target.exists()
    text=lower_source.read_text(encoding='utf8')
    before="'conditional_flag_CPU_HGB_residual_CDF': 'predict_conditional_CPU_HGB_residual_CDF_scheme_20261007.py'"
    assert text.count(before)==1
    text=text.replace(before,"'conditional_flag_CPU_HGB_residual_CDF': 'predict_flagged_CPU_HGB_weighted_quarters_scheme_20261007.py'")
    compile(text,str(lower_target),'exec')
    with lower_target.open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    create(A/'weighted_flagged_HGB_native_hook_source_preparation_20261007.json',{'status':'compiled_two_unique_native_weighted_hooks_not_actual_future_execution',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),source,target,lower_source,lower_target,plan)},
        'ordered_sum_denominator':4,'native_components_unique':True,'large_batch8192_already_passed_original20_model_benchmark':True,
        'old_equal_mean_helper_unchanged':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'compiled_two_weighted_native_helpers'},flush=True)

if __name__=='__main__':main()
