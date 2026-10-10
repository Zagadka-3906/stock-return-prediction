"""Prepare independent full-training oracle and cold-prefix controls for quantile refinements."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    native=A/'quantile_HGB_native_hook7_preflight_20261007/verification.json'
    assert read(native)['status']=='passed_actual7_historical603_quantile_HGB_native_independent_and_whole_day_prefix_controls'
    old=A/'verify_flagged_HGB_small_amplitude88_transform_20261007.py';text=old.read_text(encoding='utf8')
    text=text.replace('flagged_HGB_small_amplitude88_transform_preflight_20261007','quantile_HGB88_transform_preflight_20261007')
    text=text.replace('flagged_HGB_small_amplitude88_plan_20261007.json','quantile_HGB88_plan_20261007.json')
    needle="            if name=='flagged_residual_hgb7_absolute' and weight==.01:assert np.array_equal(values.view('u8'),parent.view('u8'))\n"
    assert needle in text;text=text.replace(needle,'')
    text=text.replace('passed_actual85_full5635800_flagged_HGB_small_amplitude_independent_oracle_and_cold80_260_975_controls','passed_actual85_full5635800_quantile_HGB_independent_oracle_and_cold80_260_975_controls')
    text=text.replace("'actual_qualified_parent112_original_branch_reproduced_bits_exact':True", "'actual_qualified_parent112_nonflag_and2020_preserved_bits_exact':True")
    text=text.replace("'parent115_not_complete_or_tested_by_this_preflight':True", "'parent117_118_graphs_not_used_by_reference112_preflight':True")
    text=text.replace("'actual_future_inference_or_full116_QA27_not_claimed':True", "'actual_future_inference_or_full119_QA30_not_claimed':True")
    needle="    out=A/'quantile_HGB88_transform_preflight_20261007';"
    assert needle in text
    text=text.replace(needle,"    assert read(A/'quantile_HGB_native_hook7_preflight_20261007/verification.json')['status']=='passed_actual7_historical603_quantile_HGB_native_independent_and_whole_day_prefix_controls'\n"+needle)
    target=A/'verify_quantile_HGB88_transform_20261007.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8')
    paths=[Path(__file__),old,target,native,A/'quantile_HGB88_plan_20261007.json',A/'quantile_HGB_native_bank20_v2_20261007/verification.json']
    create(A/'quantile_HGB85_full_controls_source_preparation_20261007.json',{'status':'compiled_actual85_full_independent_and255_cold_controls_not_yet_run','input_sha256':{str(p):sha(p) for p in paths}})
if __name__=='__main__':main()
