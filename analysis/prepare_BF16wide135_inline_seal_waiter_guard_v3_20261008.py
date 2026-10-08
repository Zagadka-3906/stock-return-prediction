"""Preserve the unused recovery2 source; admit only the exact original seal's inline dependency wait."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def main():
    original=A/'recover_BF16wide135_D_scoring_receivers_v2_20261008.py'
    text=original.read_text(encoding='utf8')
    text=text.replace('actual_BF16wide135_D_scoring_receiver_recovery_v2_20261008.json','actual_BF16wide135_D_scoring_receiver_recovery_v3_20261008.json')
    before="        assert dump.returncode==0 and 'closed (' in dump.stdout,(name,dump.stdout,dump.stderr)"
    after="        inline_seal=(name=='BF16wide40_selected_candidate_sealing_v1_20261008' and '    main (seal_BF16wide40_selected_candidate_v1_20261008.py:13)' in dump.stdout)\n        assert dump.returncode==0 and ('closed (' in dump.stdout or inline_seal),(name,dump.stdout,dump.stderr)"
    assert text.count(before)==1;text=text.replace(before,after)
    target=A/'recover_BF16wide135_D_scoring_receivers_v3_20261008.py';assert not target.exists();compile(text,str(target),'exec')
    launch=read(A/'BF16wide135_complete_hidden_launches_v1_20261008.json')['launches']
    assert len(launch)==7 and all(owned(row) for row in launch.values())
    assert not (A/'actual_BF16wide135_D_scoring_receiver_recovery_v2_20261008.json').exists()
    target.write_text(text,encoding='utf8',newline='\n')
    create(A/'BF16wide135_inline_seal_waiter_guard_preparation_v3_20261008.json',{
        'status':'recovery2_guard_stopped_before_any_retirement_or_receiver_write_and_fresh_exact_inline_wait_guard_prepared',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),original,target)},'all7_original_waiters_still_owned':True,
        'scientific_workers_untouched':True,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
