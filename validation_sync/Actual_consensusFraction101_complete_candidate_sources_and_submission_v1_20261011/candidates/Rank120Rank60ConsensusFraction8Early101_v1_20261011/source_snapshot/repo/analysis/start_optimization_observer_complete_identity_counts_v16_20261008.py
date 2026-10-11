"""Count completed zero-identity controls from terminal proof as well as numbered files."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    source=A/'monitor_actual_optimization135_to144_v15_20261008.py';text=source.read_text(encoding='utf8')
    needle="q=read(out/'verification.json');result.update(actual_passed=q['status'].startswith('passed'),verification=q)"
    assert text.count(needle)==1
    text=text.replace(needle,needle+";result['completed_items']=q.get('actual_full_cases',q.get('actual_hooks',q.get('actual_calendar_cases',result['completed_items'])))")
    text=text.replace('observer_version=15','observer_version=16').replace('progress_v15_','progress_v16_')
    target=A/'monitor_actual_optimization135_to144_v16_20261008.py';assert not target.exists()
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('actual_optimization135_to144_live_progress_v16_20261008',target.name,[],{str(target):sha(target)})
    create(A/'actual_optimization135_to144_observer_hidden_launch_v16_20261008.json',row)
    print('Actual progress16 includes passed zero-identity controls from terminal proof.',flush=True)
if __name__=='__main__':main()
