"""Publish new admitted sources and automatically publish all completed73 actual controls and scores."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    import prepare_protected163_full_registry_sources_v1_20261010 as routes
    names=[p.name for p in routes.source_paths()]
    names+=['run_Huber163_complete_family_admitted_v2_20261010.py','run_Huber163_full_registration_cleanup_v2_20261010.py','verify_Huber163_complete67_preflight_v1_20261010.py','protected163_full_family_preflight_v1_20261010.json','HuberProtected163_full67_ready_dispatch_v1_20261010.json','run_continuous_fast_reused_frontiers_v16_20261010.py','run_continuous_fast_reused_frontiers_v17_20261010.py','handoff_superior_Huber_priority_controller_v16_20261010.py','Huber163_admitted_controller17_actual_launch_v1_20261010.json','reconcile_completed162_post_publication_cleanup_v1_20261010.py','actual_complete162_post_publication_cleanup_reconciliation_v1_20261010.json','monitor_fast_optimization_v16_20261010.py','monitor_fast_optimization_v17_20261010.py','prepare_progress_observer17_Huber163_smoothing73_v1_20261010.py','causal_neural_rank_smoothing_v1_20261010.py','verify_causal_neural_rank_smoothing_v1_20261010.py','causal_neural_rank_smoothing_controls_v1_20261010.json','causal_neural_smoothing_synthetic_count_clarification_v1_20261010.json','prepare_causal_neural_smoothing73_screen_v1_20261010.py','run_causal_neural_smoothing73_screen_v1_20261010.py','causal_neural_smoothing73_screen_plan_v1_20261010.json','causal_neural_smoothing73_actual_hidden_launch_v1_20261010.json','high_impact_priority_huber65_main_receipt_v7_20261010.json','high_impact_priority_quant37_main_receipt_v8_20261010.json','high_impact_priority_budget37_main_receipt_v9_20261010.json','github_validation_sync_main_20261005/round162_receipt.json','optimization_20261003_r162/full_registration_execution.json','optimization_20261003_r162/full_registration_failure.json']
    text=(A/'publish_high_impact_priority_v9_20261010.py').read_text(encoding='utf8')
    start=text.index('    sources=[');end=text.index("    if phase in ('scores'",start)
    addition="    sources=[A/name for name in "+repr(list(dict.fromkeys(names)))+"]\n"
    addition+="    for tag in ('superior_Huber_priority_controller_handoff_v16_20261010','Huber163_smoothing73_observer_handoff_v17_20261010'):\n        sources.extend((A/tag).glob('*.json'))\n"
    addition+="    for tag in ('TailProtected162_round162_full_registration_v1_20261010_original_cleanup_failure_evidence_v1_20261010','TailProtected162_complete76_family_v1_20261010_original_cleanup_failure_evidence_v1_20261010','continuous_fast_reused_frontiers_v16_20261010','actual_complete162_post_publication_cleanup_reconciliation_v1_20261010'):\n        folder=A/'service_owned_workflows_20261006'/tag\n        sources.extend(folder.glob('*.json'));sources.extend(folder.glob('*.log'))\n"
    text=text[:start]+addition+text[end:]
    text=text.replace("{'protected':'protected_official_top", "{'temporal73':'causal_neural_smoothing73_screen_v1_20261010','protected':'protected_official_top")
    text=text.replace("{'protected':'actual_protected_official_top", "{'temporal73':'actual_causal_neural_smoothing73_screen_v1_20261010','protected':'actual_protected_official_top")
    text=text.replace("('scores','protected','valid','huber65','quant37','budget37')","('scores','protected','valid','huber65','quant37','budget37','temporal73')")
    text=text.replace("expected=65 if phase=='huber65'", "expected=73 if phase=='temporal73' else 65 if phase=='huber65'")
    text=text.replace("A/('actual_budgeted_neural_Top37_screen_location", "A/('actual_causal_neural_smoothing73_screen_location_v1_20261010.json' if phase=='temporal73' else 'actual_budgeted_neural_Top37_screen_location")
    text=text.replace("'huber65','quant37','budget37']);", "'huber65','quant37','budget37','temporal73']);")
    for old,new in [('main_v9_20261010','main_v10_20261010'),('main_receipt_v9_20261010','main_receipt_v10_20261010'),('priority_'+"'+phase+'_v9_20261010",'priority_'+"'+phase+'_v10_20261010")]:text=text.replace(old,new)
    # File names referring to previous receipts remain historical, never change their versions.
    text=text.replace('high_impact_priority_budget37_main_receipt_v10_20261010.json','high_impact_priority_budget37_main_receipt_v9_20261010.json')
    text=text.replace('优先验证更大提分方向：完整157之后96种互补融合与非涨停、大权重和新Huber训练计划','优先验证实测更高分Huber163并扩展73项因果神经信号平滑')
    driver=A/'publish_priority_Huber163_temporal73_v10_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    for phase in ('preparation','temporal73'):
        row=start_service('actual_priority_Huber163_temporal73_'+phase+'_main_v10_20261010',driver.name,[phase],{str(driver):sha(driver),str(Path(__file__)):sha(Path(__file__))})
        create(A/('priority_Huber163_temporal73_'+phase+'_main_launch_v10_20261010.json'),row)
    print('Actual hidden preparation publisher and73-completion publisher launched',flush=True)
if __name__=='__main__':main()
