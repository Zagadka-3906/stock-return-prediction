"""Reuse the full independentCDF harness on new28 declared mixtures, without scoring."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    source=A/'verify_flagged_HGB_small_amplitude88_transform_20261007.py'
    target=A/'verify_flagged_HGB_weighted_quarters340_transform_20261007.py';assert not target.exists()
    text=source.read_text(encoding='utf8')
    changes={
        'flagged_HGB_small_amplitude88_transform_preflight_20261007':'flagged_HGB_weighted_quarters340_transform_preflight_20261007',
        'flagged_HGB_small_amplitude88_plan_20261007.json':'flagged_HGB_weighted_quarters340_plan_20261007.json',
        "for name in [*plan['single_native_heads'],*plan['ensembles']]":"for name in plan['ensembles']",
        'assert len(cases)==85':'assert len(cases)==337',
        "            if name=='flagged_residual_hgb7_absolute' and weight==.01:assert np.array_equal(values.view('u8'),parent.view('u8'))\n":"",
        'passed_actual85_full5635800_flagged_HGB_small_amplitude_independent_oracle_and_cold80_260_975_controls':'passed_actual337_full5635800_weighted_flagged_HGB_independent_oracle_and_cold80_260_975_controls',
        "'actual_qualified_parent112_original_branch_reproduced_bits_exact':True":"'all337_weighted_and_ablation_forecasts_independent_CDF_and_prefix_controls':True",
        "'parent115_not_complete_or_tested_by_this_preflight':True":"'parent116_not_complete_or_tested_by_this_preflight':True",
        "'full5635800_cases':85":"'full5635800_cases':337",
        "'cold_prefix_cases':255":"'cold_prefix_cases':1011",
    }
    for before,after in changes.items():
        assert text.count(before)==1,before
        text=text.replace(before,after)
    # Validate ordered means independently using ufunc accumulation including the initial zero.
    needle='        head[\'remove_flagged_HGB\']=np.zeros(len(reference),dtype=np.float64)'
    assert text.count(needle)==1
    extra="""        for name,names in plan['ensembles'].items():
            stack=np.stack([np.zeros(len(reference),dtype=np.float64),*[head[n] for n in names]])
            oracle_mean=np.add.accumulate(stack,axis=0)[-1]/4.
            assert np.array_equal(head[name].view('u8'),oracle_mean.view('u8'))
            del stack,oracle_mean
"""
    text=text.replace(needle,extra+needle)
    compile(text,str(target),'exec')
    with target.open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    create(A/'weighted_flagged_HGB_full337_controls_source_preparation_20261007.json',{'status':'compiled_full337_independentCDF_and1011_prefix_controls_before_execution',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),source,target)},'new_quality_scores':0,'new_native_fits':0})
    print({'status':'compiled_full337_control_harness'},flush=True)

if __name__=='__main__':main()
