"""Keep dynamic gap-aware progress and add complete ready-FM boundary evidence."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'


def main():
    source=(A/'monitor_actual_optimization_progress_v15_20261005.py').read_text(encoding='utf-8')
    source=source.replace('refresh_optimization_boundary_evidence_v14_20261005','refresh_optimization_boundary_evidence_v15_20261005')
    source=source.replace('monitor_actual_optimization_progress_v15_20261005','monitor_actual_optimization_progress_v16_20261005')
    source=source.replace('actual_optimization_monitor_run_v15_20261005','actual_optimization_monitor_run_v16_20261005')
    source=source.replace("proof_names = [", "proof_names = ['ready_fm_reference_generator_preflight_20261005/verification.json','ready_fm_reference_execution_preflight_20261005/verification.json',")
    path=A/'monitor_actual_optimization_progress_v16_20261005.py'
    compile(source,str(path),'exec')
    with path.open('x',encoding='utf-8',newline='\n') as stream:stream.write(source)
    print('Created monitor V16 retaining every earlier required round.')


if __name__=='__main__':main()
