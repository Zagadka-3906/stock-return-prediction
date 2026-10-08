"""Admit only the additional exact full-registration inline wait; preserve all unused previous recovery sources."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def main():
    original=A/'recover_BF16wide135_D_scoring_receivers_v3_20261008.py';text=original.read_text(encoding='utf8')
    text=text.replace('actual_BF16wide135_D_scoring_receiver_recovery_v3_20261008.json','actual_BF16wide135_D_scoring_receiver_recovery_v4_20261008.json')
    before="        assert dump.returncode==0 and ('closed (' in dump.stdout or inline_seal),(name,dump.stdout,dump.stderr)"
    after="        inline_registration=(name=='BF16wide40_round135_full_registration_v1_20261008' and '    main (run_BF16wide40_round135_full_registration_v1_20261008.py:19)' in dump.stdout)\n        assert dump.returncode==0 and ('closed (' in dump.stdout or inline_seal or inline_registration),(name,dump.stdout,dump.stderr)"
    assert text.count(before)==1;text=text.replace(before,after)
    target=A/'recover_BF16wide135_D_scoring_receivers_v4_20261008.py';assert not target.exists();compile(text,str(target),'exec')
    rows=read(A/'BF16wide135_complete_hidden_launches_v1_20261008.json')['launches'];assert len(rows)==7 and all(owned(row) for row in rows.values())
    target.write_text(text,encoding='utf8',newline='\n')
    create(A/'BF16wide135_inline_registration_guard_preparation_v4_20261008.json',{
        'status':'recovery3_guard_stopped_before_retirement_and_fresh_exact_registration_wait_guard_prepared',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),original,target)},'all7_original_waiters_still_owned':True,
        'scientific_workers_untouched':True,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
