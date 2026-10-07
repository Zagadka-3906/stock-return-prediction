"""Fresh340 workflow sources use passed unique-nativeV2 and gated equivalent percentile runtime."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    preparation=A/'weighted_flagged_HGB340_workflow_source_preparation_20261007.json';old=read(preparation)
    routes={
        'run_flagged_HGB_weighted_quarters340_official_comparison_20261007':'run_flagged_HGB_weighted_quarters340_official_comparison_v2_20261007',
        'prepare_flagged_HGB_weighted_quarters340_selected_candidate_20261007':'prepare_flagged_HGB_weighted_quarters340_selected_candidate_v2_20261007',
        'seal_flagged_HGB_weighted_quarters340_selected_candidate_20261007':'seal_flagged_HGB_weighted_quarters340_selected_candidate_v2_20261007',
        'predict_refined_weighted_flagged_CPU_HGB_scheme_20261007':'predict_refined_weighted_flagged_CPU_HGB_scheme_v2_20261007',
        'predict_flagged_CPU_HGB_weighted_quarters_scheme_20261007':'predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007',
        'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_20261007':'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007',
        'weighted_flagged_HGB_full337_transform_preflight':'weighted_flagged_HGB_full337_transform_preflight_v2',
    }
    names=['predict_refined_weighted_flagged_CPU_HGB_scheme_20261007.py',*[job['driver'] for job in old['jobs']]]
    sources=[Path(__file__),preparation,A/'all_forecast_percentile_runtime_20261007.py'];jobs=[]
    for name in names:
        original=A/name;new=routes[name[:-3]]+'.py';target=A/new;assert not target.exists()
        text=substitute(original.read_text(encoding='utf8'),routes)
        if name.startswith('run_'):
            text=text.replace("    bank=A/plan['existing_native_bank'];bank_proof=read(bank/'verification.json')", "    closed('all_forecast_percentiles_full_scoring_benchmark')\n    bank=A/plan['existing_native_bank'];bank_proof=read(bank/'verification.json')")
            before="            with installed(scoring/'submission.csv') as date_index:metrics=score(ctx,values)";assert text.count(before)==1
            text=text.replace(before,"            from all_forecast_percentile_runtime_20261007 import installed as percentile_runtime\n            with percentile_runtime() as percentile_events:\n                with installed(scoring/'submission.csv') as date_index:metrics=score(ctx,values)")
            text=text.replace("'official_date_index_runtime':dict(date_index)","'official_date_index_runtime':dict(date_index),'all_row_percentile_runtime':dict(percentile_events)")
            needle="ROOT/'evaluate.py',ROOT/'后续选模标准.md',frame_path,reference_path,reference_candidate/'verification.json',bank/'verification.json']"
            assert text.count(needle)==1
            text=text.replace(needle,"ROOT/'evaluate.py',ROOT/'后续选模标准.md',frame_path,reference_path,reference_candidate/'verification.json',bank/'verification.json',\n        A/'exact_numpy_all_forecast_percentiles_20261007.py',A/'all_forecast_percentile_runtime_20261007.py',\n        A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json']")
        compile(text,str(target),'exec')
        with target.open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
        sources += [original,target]
        if name!='predict_refined_weighted_flagged_CPU_HGB_scheme_20261007.py':
            job=next(j for j in old['jobs'] if j['driver']==name);jobs.append({**job,'driver':new})
    create(A/'weighted_flagged_HGB340_workflow_source_preparation_v2_20261007.json',{'status':'compiled_four_fresh340_workflows_with_unique_nativeV2_and_gated_percentile_equivalence_before_admission',
        'input_sha256':{str(p):sha(p) for p in sources},'routes':routes,'jobs':jobs,
        'original_compiled_V1_prototypes_and_actual_failed_native_diagnostic_preserved':True,
        'actual28_native_hook_V2_already_passed':True,'full337_and12_uncached_official_controls_required_before_admission':True,
        'full117_registry_and_QA28_pipeline_still_to_be_prepared':True,'new_quality_scores':0,'new_native_fits':0})
    print({'status':'compiled_four_fresh340_sources','new_quality_scores':0},flush=True)

if __name__=='__main__':main()
