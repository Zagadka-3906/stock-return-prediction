"""Publish the independent81 verification and keep live155 progress in the current observer."""
from pathlib import Path
import ast,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
def write(name,text):
    ast.parse(text);p=A/name
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    return p
def main():
    src=A/'monitor_actual_chronological_optimization_progress_v67_20261009.py';s=src.read_text(encoding='utf8').replace('v67_20261009','v68_20261009')
    old="state['current_turn_evidence_main']=status('actual154_full_import_and155_dependencies_main_publication_v81_20261009')"
    assert s.count(old)==1;s=s.replace(old,"state['current_turn_evidence_main']=status('actual155_progress_and_main81_reconciliation_main_publication_v83_20261009')\n    state['original81_receipt_collision_preserved']=status('actual154_full_import_and155_dependencies_main_publication_v81_20261009')\n    state['actual81_all_blobs_and_remote_main_reconciliation']=status('main81_published_receipt_collision_reconciliation_v82_20261009')")
    observer=write('monitor_actual_chronological_optimization_progress_v68_20261009.py',s)
    starter_src=A/'start_actual_recovered_progress_v67_20261009.py';s=starter_src.read_text(encoding='utf8').replace('v67_20261009','v68_20261009').replace('observer_v66_20261009','observer_v67_20261009')
    starter=write('start_actual_recovered_progress_v68_20261009.py',s)
    pub_src=A/'publish_actual154_full_import_and155_dependencies_main_v81_20261009.py';s=pub_src.read_text(encoding='utf8').replace('v81_20261009','v83_20261009')
    old="create(A/'actual154_corrected_receivers_cache_cleanup_main_v79_receipt_20261009.json',value)"
    assert s.count(old)==1;s=s.replace(old,"create(A/'actual155_progress_and_main81_reconciliation_main_v83_receipt_20261009.json',value)")
    old='def main():';assert s.count(old)==1
    s=s.replace(old,"def main():\n    import time\n    service=A/'service_owned_workflows_20261006/main81_published_receipt_collision_reconciliation_v82_20261009'\n    while not (service/'service_execution.json').exists() or owned(read(service/'native_launch.json')):time.sleep(5)\n    assert read(service/'service_execution.json')['status']=='passed'")
    old='    sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)';assert s.count(old)==1
    extra="""    sources.extend([A/'reconcile_main81_published_receipt_collision_v82_20261009.py',
        A/'main81_published_receipt_reconciliation_v82_20261009.json',
        A/'actual154_full_import_and155_dependencies_main_v81_reconciled_receipt_20261009.json',
        A/'prepare_main81_reconciliation_and_actual155_progress_v54_20261009.py'])
    for pattern in ('*progress*v68_20261009.py','*progress*v68_20261009.json','*progress*v68_20261009.md'):
        sources.extend(A.glob(pattern))
    for name in ('actual154_full_import_and155_dependencies_main_publication_v81_20261009','main81_published_receipt_collision_reconciliation_v82_20261009'):
        sources.extend(p for p in (A/'service_owned_workflows_20261006'/name).glob('*') if p.is_file() and p.suffix in ('.json','.log'))
"""
    s=s.replace(old,extra+old)
    s=s.replace('同步154实际完整榜接收入口修复和155连续依赖及保留失败记录','同步已提交main81全部字节及远端复核和155实际连续评分进度')
    pub=write('publish_actual155_progress_and_main81_reconciliation_main_v83_20261009.py',s)
    create(A/'main81_reconciliation_and_actual155_progress_preparation_v54_20261009.json',{'status':'prepared_actual155_observer68_and_main83_with_unique_receipt','input_sha256':{str(p):sha(p) for p in (Path(__file__),src,observer,starter_src,starter,pub_src,pub)},'new_quality_scores':0})
if __name__=='__main__':main()
