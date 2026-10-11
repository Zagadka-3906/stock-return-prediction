"""Create an observer which retains unfinished earlier rounds after side comparisons."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'


def create(name,text):
    path=A/name
    compile(text,str(path),'exec')
    with path.open('x',encoding='utf-8',newline='\n') as stream:stream.write(text)


def main():
    source=(A/'refresh_continuous_progress_20261004.py').read_text(encoding='utf-8')
    old='latest,result=max(completed,key=lambda item:item[0]);active=latest+1'
    assert old in source
    source=source.replace(old,"from qualified_round_inventory_20261005 import assess\n    inventory=assess(completed,[row['round'] for row in entries],[int(p.stem.rsplit('_r',1)[1]) for p in (ROOT/'results').glob('optimization_20261003_r*.json')])\n    latest=inventory['latest_qualified_round'];result=inventory['best_result'];active=inventory['active_round']")
    source=source.replace("list(range(latest+1,latest_published+1))", "inventory['published_rounds_pending_scoped_completion']")
    source=source.replace("[r['round'] for r in entries if r['round']>active]", "[n for n in inventory['pending_rounds'] if n!=active]")
    source=source.replace("'latest_published_round':latest_published,", "'qualified_rounds':inventory['qualified_rounds'],'best_completed_round':inventory['best_round'],'last_contiguous_registered_completed_round':inventory['last_contiguous_registered_completed_round'],'pending_required_rounds':inventory['pending_rounds'],'latest_published_round':latest_published,")
    create('refresh_continuous_progress_v2_20261005.py',source)
    monitor=(A/'monitor_actual_optimization_progress_v14_20261005.py').read_text(encoding='utf-8')
    monitor=monitor.replace('refresh_continuous_progress_20261004','refresh_continuous_progress_v2_20261005')
    monitor=monitor.replace('refresh_optimization_boundary_evidence_v13_20261005','refresh_optimization_boundary_evidence_v14_20261005')
    monitor=monitor.replace('monitor_actual_optimization_progress_v14_20261005','monitor_actual_optimization_progress_v15_20261005')
    monitor=monitor.replace('actual_optimization_monitor_run_v14_20261005','actual_optimization_monitor_run_v15_20261005')
    monitor=monitor.replace("'active_round': value['active_round'],", "'qualified_rounds':value['qualified_rounds'],'best_completed_round':value['best_completed_round'],'last_contiguous_registered_completed_round':value['last_contiguous_registered_completed_round'],'pending_required_rounds':value['pending_required_rounds'],'active_round': value['active_round'],")
    monitor=monitor.replace("if once or state['latest_completed_round'] >= 80:", "if once or not state['pending_required_rounds']:")
    create('monitor_actual_optimization_progress_v15_20261005.py',monitor)
    print('Created progress V2 and monitor V15 with explicit pending inventory.')


if __name__=='__main__':main()
