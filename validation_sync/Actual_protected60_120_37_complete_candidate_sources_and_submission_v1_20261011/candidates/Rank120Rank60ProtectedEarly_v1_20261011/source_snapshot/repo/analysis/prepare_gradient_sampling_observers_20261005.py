"""Extend observed fit costs, coverage and monitoring through actual round76."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def main():
    cost = (A / 'refresh_factorization_machine_cost_evidence_20261005.py').read_text(encoding='utf-8-sig')
    cost = cost.replace('factorization_machine', 'gradient_sampling')
    cost = cost.replace('import refresh_linear_leaf_ensemble_cost_evidence_20261005 as previous',
        'import refresh_factorization_machine_cost_evidence_20261005 as previous')
    cost = cost.replace("operational_writes('refresh_linear_leaf_ensemble_cost_evidence_20261005')",
        "operational_writes('refresh_factorization_machine_cost_evidence_20261005')")
    cost = cost.replace("'kind': 'gradient_sampling'", "'kind': 'lightgbm_gradient_sampling'")
    cost = cost.replace('actual4_epoch_controls_not_counted_as_complete32_epoch_annual_fits',
        'actual48_round_controls_not_counted_as_complete300_round_annual_fits')
    cost = cost.replace("assert info['year'] == year and info['model'] == name", "assert info['year'] == year and info['model'] == name\n            assert info['leaf_summary']['tree_count'] == cfg['num_boost_round'] == 300")
    monitor = (A / 'monitor_actual_optimization_progress_v9_20261005.py').read_text(encoding='utf-8-sig')
    monitor = monitor.replace('monitor_actual_optimization_progress_v9_20261005', 'monitor_actual_optimization_progress_v10_20261005')
    monitor = monitor.replace('actual_optimization_monitor_run_v9_20261005', 'actual_optimization_monitor_run_v10_20261005')
    monitor = monitor.replace('refresh_factorization_machine_cost_evidence_20261005', 'refresh_gradient_sampling_cost_evidence_20261005')
    monitor = monitor.replace("'factorization_machine_actual_annual_fits' not in", "'gradient_sampling_actual_annual_fits' not in")
    monitor = monitor.replace('refresh_optimization_boundary_evidence_v8_20261005', 'refresh_optimization_boundary_evidence_v9_20261005')
    monitor = monitor.replace("state['latest_completed_round'] >= 74", "state['latest_completed_round'] >= 76")
    monitor = monitor.replace('proof_names = [', "proof_names = ['gradient_sampling_preflight_20261005/verification.json','gradient_sampling_direct_router_preflight_20261005/verification.json','gradient_sampling_search_generator_preflight_20261005/verification.json','gradient_sampling_future_qa_20261005/verification.json','gradient_sampling_bank_20261005/training_execution_scope.json',")
    for name, source in (('refresh_gradient_sampling_cost_evidence_20261005.py', cost),
                         ('monitor_actual_optimization_progress_v10_20261005.py', monitor)):
        compile(source, name, 'exec')
        with (A / name).open('x', encoding='utf-8', newline='') as stream:
            stream.write(source)


if __name__ == '__main__':
    main()
