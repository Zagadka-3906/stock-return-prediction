"""Version the operational observer to80 and count only complete actual classifiers."""
from pathlib import Path
A=Path(__file__).resolve().parent


def main():
    source=(A/'monitor_actual_optimization_progress_v13_20261005.py').read_text(encoding='utf-8')
    source=source.replace('monitor_actual_optimization_progress_v13_', 'monitor_actual_optimization_progress_v14_')
    source=source.replace('actual_optimization_monitor_run_v13_', 'actual_optimization_monitor_run_v14_')
    source=source.replace('refresh_optimization_boundary_evidence_v12_', 'refresh_optimization_boundary_evidence_v13_')
    source=source.replace('refresh_memory_efficient_neural_cost_evidence_20261005', 'refresh_streaming_rank_classifier_cost_evidence_20261005')
    source=source.replace("'memory_efficient_neural_actual_annual_fits' not in", "'streaming_rank_classifier_actual_annual_fits' not in")
    source=source.replace("state['latest_completed_round'] >= 78", "state['latest_completed_round'] >= 80")
    source=source.replace('proof_names = [', "proof_names = ['streaming_rank_classification_preflight_v3_20261005/verification.json','streaming_rank_classifier_direct_router_preflight_20261005/verification.json','streaming_rank_classifier_search_generator_preflight_v4_20261005/verification.json','streaming_rank_classifier_execution_source_preflight_v4_20261005/verification.json','streaming_rank_classification_bank_v3_20261005/training_execution_scope.json','streaming_rank_classifier_future_qa_v3_20261005/verification.json',")
    target=A/'monitor_actual_optimization_progress_v14_20261005.py'
    compile(source,str(target),'exec')
    with target.open('x',encoding='utf-8',newline='\n') as stream:stream.write(source)
    print('Observer14 prepared through80 with full native classifier accounting.',flush=True)


if __name__=='__main__':main()
