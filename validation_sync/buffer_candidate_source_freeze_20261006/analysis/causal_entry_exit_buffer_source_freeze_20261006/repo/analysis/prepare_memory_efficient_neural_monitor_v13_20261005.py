"""Extend the existing observer to78 and include its E-drive native info inventory."""
from pathlib import Path

A=Path(__file__).resolve().parent


def main():
    path=A/'monitor_actual_optimization_progress_v13_20261005.py'
    source=(A/'monitor_actual_optimization_progress_v12_20261005.py').read_text(encoding='utf-8')
    source=source.replace('monitor_actual_optimization_progress_v12_', 'monitor_actual_optimization_progress_v13_')
    source=source.replace('actual_optimization_monitor_run_v12_', 'actual_optimization_monitor_run_v13_')
    source=source.replace('refresh_optimization_boundary_evidence_v11_', 'refresh_optimization_boundary_evidence_v12_')
    source=source.replace('refresh_gradient_sampling_cost_evidence_20261005', 'refresh_memory_efficient_neural_cost_evidence_20261005')
    source=source.replace("'gradient_sampling_actual_annual_fits' not in", "'memory_efficient_neural_actual_annual_fits' not in")
    source=source.replace("state['latest_completed_round'] >= 76", "state['latest_completed_round'] >= 78")
    old="    inventory = sorted((str(p.relative_to(ROOT)), p.stat().st_size, p.stat().st_mtime_ns)\n        for bank in (ROOT / 'analysis').glob('*bank_*') if bank.is_dir()\n        for p in bank.glob('*/info_*.json'))"
    assert source.count(old)==1
    new="    native_banks = [bank for bank in (ROOT/'analysis').glob('*bank_*') if bank.is_dir()]\n    external_bank = Path(read(ROOT/'analysis/memory_efficient_neural_storage_20261005.json')['output_directory'])\n    if external_bank not in native_banks:\n        native_banks.append(external_bank)\n    inventory = sorted((str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p), p.stat().st_size, p.stat().st_mtime_ns)\n        for bank in native_banks for p in bank.glob('*/info_*.json'))"
    source=source.replace(old,new)
    source=source.replace("proof_names = [", "proof_names = ['memory_efficient_neural_direct_router_preflight_20261005/verification.json','memory_efficient_neural_search_generator_preflight_20261005/verification.json','memory_efficient_neural_workflow_preflight_20261005/verification.json','memory_efficient_neural_future_qa_20261005/verification.json','memory_efficient_mlp_gpu_recovery_v2_20261005/verification.json',")
    source=source.replace("    boundary_key = [latest, [(str(p.relative_to(ROOT)), p.stat().st_size, p.stat().st_mtime_ns) for p in proof_paths if p.exists()]]", "    proof_paths.append(external_bank/'training_execution_scope.json')\n    GPU=Path(read(ROOT/'analysis/memory_efficient_mlp_storage_20261005.json')['GPU_control_directory'])\n    proof_paths.extend((GPU/'verification.json',GPU/'execution_scope.json'))\n    boundary_key = [latest, [(str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p), p.stat().st_size, p.stat().st_mtime_ns) for p in proof_paths if p.exists()]]")
    compile(source,str(path),'exec')
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(source)
    print('Prepared observer through78 with E-drive inventory and actual complete-fit costs',flush=True)


if __name__=='__main__':
    main()
