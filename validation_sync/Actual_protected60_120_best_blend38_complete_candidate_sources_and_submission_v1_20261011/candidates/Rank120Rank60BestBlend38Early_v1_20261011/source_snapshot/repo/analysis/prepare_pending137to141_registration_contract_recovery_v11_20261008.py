"""Fresh imported helper initializes its own configuration before generated calls."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    old=A/'recover_pending137to141_registration_contracts_v10_20261008.py';target=A/'recover_pending137to141_registration_contracts_v11_20261008.py'
    assert not target.exists();text=old.read_text(encoding='utf8').replace('_v10','_v11').replace('version10','version11').replace('Fresh10','Fresh11').replace('fresh10','fresh11').replace('collector10','collector11')
    text=text.replace("cfg=next(c for c in CONFIG if c['round']==number);out={}","initialize();cfg=next(c for c in CONFIG if c['round']==number);out={}")
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'pending137to141_control10_failure_preserved_20261008.json',{'status':'failed_before_any_prospective_scoring_or_worker_actions',
        'source_sha256':sha(old),'failure':'Imported collector helper CONFIG was empty although __main__ helper CONFIG was initialized; StopIteration.',
        'all_frozen10_sources_preserved':True,'recovery_source_sha256':sha(target),'new_quality_scores':0,'training_workers_stopped':0})
if __name__=='__main__':main()
