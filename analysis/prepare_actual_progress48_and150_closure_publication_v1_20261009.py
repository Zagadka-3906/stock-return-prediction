"""Prepare the actual second150 dispatcher monitor and publication of its additional inherited import proof."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def main():
    s=(A/'monitor_actual_chronological_optimization_progress_v47_20261009.py').read_text(encoding='utf8')
    s=s.replace('optimization_live_progress_v47_20261009','optimization_live_progress_v48_20261009')
    s=s.replace('HuberSparse150_complete_chronological_dispatch_v1_20261009','HuberSparse150_complete_chronological_dispatch_v2_20261009')
    s=s.replace('HuberSparse150_prospective_main_publication_v1_20261009','HuberSparse150_prospective_main_publication_v2_20261009')
    save('monitor_actual_chronological_optimization_progress_v48_20261009.py',s)
    s=(A/'publish_HuberSparse150_prospective_main_v1_20261009.py').read_text(encoding='utf8')
    s=s.replace("    closed('HuberSparse150_complete_prospective_controls_v1_20261009')", "    closed('HuberSparse150_prospective_main_publication_v1_20261009')\n    closed('HuberSparse150_complete_prospective_controls_v1_20261009')")
    s=s.replace('HuberSparse150_prospective_main_v1_20261009','HuberSparse150_prospective_main_v2_20261009')
    s=s.replace('validation_sync/HuberSparse150_prospective_v1_20261009','validation_sync/HuberSparse150_prospective_v2_20261009')
    s=s.replace('HuberSparse150_prospective_main_v1_receipt_20261009','HuberSparse150_prospective_main_v2_receipt_20261009')
    marker='    sources=list(dict.fromkeys(sources));'
    assert s.count(marker)==1
    extra="""    from HuberSparse150_import_dependency_closure_v1_20261009 import EXTRAS,META,PROOF
    closure=read(META)
    for path,digest in closure['input_sha256'].items():assert sha(path)==digest,path
    sources.extend([*(A/n for n in EXTRAS),META,PROOF,A/'actual_HuberSparse150_dispatch_import_closure_recovery_v2_20261009.json',
        A/'prepare_actual_progress47_for150_v1_20261009.py',A/'monitor_actual_chronological_optimization_progress_v47_20261009.py',
        A/'monitor_actual_chronological_optimization_progress_v48_20261009.py',A/'prepare_actual_progress48_and150_closure_publication_v1_20261009.py',
        A/'actual_old_progress46_retired_after47_v1_20261009.json'])
    folder=A/'service_owned_workflows_20261006/HuberSparse150_complete_chronological_dispatch_v2_20261009'
    sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.log'))
"""
    s=s.replace(marker,extra+marker)
    s=s.replace("'own_actual149_dependent_duplicate_audit_and_chronological_dispatch_started':True", "'own_actual149_dependent_duplicate_audit_and_chronological_dispatch_started':True,'actual_inherited_best_key_import_AST_identity_and_raw_source_frozen':True,'current_live_dispatcher_version':2,'retired_child_free_dispatcher1_preserved':True")
    s=s.replace('同步第150轮32生成代码440方案图实际预检查及保留失败记录','同步第150轮继承排序函数字节冻结及实际连续派发更新')
    save('publish_HuberSparse150_prospective_main_v2_20261009.py',s)
if __name__=='__main__':main()
