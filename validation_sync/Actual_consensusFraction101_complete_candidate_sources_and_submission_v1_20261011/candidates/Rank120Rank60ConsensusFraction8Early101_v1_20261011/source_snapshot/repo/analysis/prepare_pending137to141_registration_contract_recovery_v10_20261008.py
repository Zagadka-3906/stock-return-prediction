"""Keep failed9 intact; use actual seven-stage reverse queue and two owned auxiliary controls."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    old=A/'recover_pending137to141_registration_contracts_v9_20261008.py';target=A/'recover_pending137to141_registration_contracts_v10_20261008.py'
    assert not target.exists();text=old.read_text(encoding='utf8').replace('_v9','_v10').replace('version9','version10').replace('Fresh9','Fresh10').replace('fresh9','fresh10').replace('collector9','collector10')
    before="launches=read(A/index)['launches'];assert len(launches)==8"
    after="""launches=dict(read(A/index)['launches']);assert len(launches)==(7 if n==138 else 8)
        if n==138:
            for service in ('BF16_reverse_rank_CDF_actual_full37_controls_v1_20261008','BF16_reverse_complete_parent_actual_historical_native_hook3_v1_20261008'):
                launches[service]=read(A/'service_owned_workflows_20261006'/service/'native_launch.json')"""
    assert text.count(before)==1;text=text.replace(before,after)
    text=text.replace('assert len(pairs)==39','assert len(pairs)==40').replace('passed39_owned','passed40_owned').replace('passed39_idle_replacements_and40_owned_future_steps','passed40_idle_replacements_and41_owned_future_steps')
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'pending137to141_preparer9_failure_preserved_20261008.json',{'status':'failed_before_any_new_files_or_worker_actions',
      'source_sha256':sha(old),'failure':'Reverse138 index correctly has seven main stages plus two separately launched controls; old9 assumed eight.',
      'recovery_source_sha256':sha(target),'new_quality_scores':0,'training_workers_stopped':0})
    print('Fresh10 constructor prepared with actual reverse auxiliary controls.',flush=True)
if __name__=='__main__':main()
