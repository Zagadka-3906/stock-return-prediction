"""Track the actual current150 dispatch3 and151 dispatch2 with20 annual native states and source closure."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def main():
    original=A/'monitor_actual_chronological_optimization_progress_v49_20261009.py';source=original.read_text(encoding='utf8')
    source=source.replace('optimization_live_progress_v49_20261009','optimization_live_progress_v50_20261009')
    source=source.replace("150:('HuberSparse59',59,1)}","150:('HuberSparse59',59,1),151:('RFFSparse59',59,1)}")
    source=source.replace("        folder=A/f'{prefix}_official_comparison_v1_20261008'", "        date='20261009' if number==151 else '20261008'\n        folder=A/f'{prefix}_official_comparison_v1_{date}'")
    for role in ('official_comparison','controls_main_publication','scores_main_publication','selected_candidate_preparation','selected_candidate_sealing'):
        source=source.replace(f"{{prefix}}_{role}_v{{version}}_20261008",f"{{prefix}}_{role}_v{{version}}_{{date}}")
    source=source.replace("{prefix}_round{number}_full_registration_v{6 if number==136 else version}_20261008","{prefix}_round{number}_full_registration_v{6 if number==136 else version}_{date}")
    source=source.replace('HuberSparse150_complete_chronological_dispatch_v2_20261009','HuberSparse150_complete_chronological_dispatch_v3_20261009')
    marker="    write(A/'optimization_live_progress_v50_20261009.json'"
    addition="""    coverage=read(A/'sparse150151_all20_annual_native_coverage_v1_20261009.json')
    for row in coverage['records']:
        frontier=state['huber_sparse150_frontier' if row['round']==150 else 'rff_sparse151_frontier']
        frontier.update(actual_annual_native_states_replayed=row['actual_head_year_states'],actual_native_stage_cases=row['actual_native_cases'],actual_cold_native_cases=row['actual_cold_cases'],all5_model_years_replayed=True)
    state['rff_sparse151_frontier'].update(complete_quality_receivers_and_duplicate_audit_still_required=False,
        inherited_full150_status_labels_require_normalization_before_admission=False,
        complete_prospective_controls=status('RFFSparse151_complete_prospective_controls_v1_20261009'),
        duplicate_audit=status('RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009'),
        chronological_dispatch=status('RFFSparse151_complete_chronological_dispatch_v2_20261009'),
        actual_project_import_sources=read(A/'RFFSparse151_project_source_closure_v1_20261009.json')['project_source_count'],
        actual151_official_scores=pipeline['151']['completed_cases'],source_admission=status('RFFSparse59_round151_source_admission_v1_20261009'))
    state['all5_annual150151_complete_prospective_main_publication']=status('sparse150151_full_prospective_main_publication_v50_20261009')
"""
    assert source.count(marker)==1;source=source.replace(marker,addition+marker)
    before='六份评分与推理草稿及55项控制绑定已检查，还需完整32代码检查与去重，尚无质量分或测试推理。'
    after="完整32代码/440图及五个年度全部20状态90原生/90冷检查已通过，已接入连续派发；去重{state['rff_sparse151_frontier']['duplicate_audit']['status']}，等待150轮完整合格后准入，实际评分见上表。"
    assert before in source;source=source.replace(before,after)
    save('monitor_actual_chronological_optimization_progress_v50_20261009.py',source)
if __name__=='__main__':main()
