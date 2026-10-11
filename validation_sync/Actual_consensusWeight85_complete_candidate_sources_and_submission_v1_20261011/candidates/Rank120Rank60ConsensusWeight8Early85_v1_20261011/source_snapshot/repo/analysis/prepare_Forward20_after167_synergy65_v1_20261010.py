"""Reuse qualified mean20 native bank to test cumulative167 interactions without refitting."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    receipt=read(A/'github_validation_sync_main_20261005/round167_receipt.json')
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==67
    assert read(A/'high_impact_priority_huber65_main_receipt_v18_20261010.json')['status']=='pushed_and_remote_head_verified'
    screenname='run_Forward20_after167_high_impact65_screen_v1_20261010.py'
    original=A/'run_Forward20_after163_high_impact65_screen_v1_20261010.py'
    s=original.read_text(encoding='utf8').replace('163','167')
    needle='    assert allowed()\n'
    replacement=needle+"    release=read(A/'github_validation_sync_main_20261005/round167_receipt.json')\n    assert release['status']=='pushed_and_remote_head_verified' and release['scored_records']==67\n"
    s=s.replace(needle,replacement,1)
    oldtree=ast.parse(original.read_text(encoding='utf8'));newtree=ast.parse(s)
    for fn in ('transformed',):
        old=next(n for n in ast.walk(oldtree) if isinstance(n,ast.FunctionDef) and n.name==fn)
        new=next(n for n in ast.walk(newtree) if isinstance(n,ast.FunctionDef) and n.name==fn)
        assert ast.dump(new)==ast.dump(ast.parse(ast.unparse(old).replace('163','167')).body[0])
    pubname='publish_Forward20_after167_65_completion_v20_20261010.py'
    puboriginal=A/'publish_Forward20_after163_65_completion_v18_20261010.py'
    pub=puboriginal.read_text(encoding='utf8').replace('Forward20_after163','Forward20_after167').replace('v18_20261010','v20_20261010')
    pub=pub.replace("A/'continuous_fast_reused_frontiers_v22_20261010/round166_fully_qualified_reconciliation.json',A/'github_validation_sync_main_20261005/round166_receipt.json'", "A/'latest_verified_submission_delivery_v2_20261008.json',A/'github_validation_sync_main_20261005/round167_receipt.json',A/'Forward20_after167_synergy65_source_admission_v1_20261010.json',Path('E:/赛题五_本机临时/Forward20_after163_high_impact65_screen_v1_20261010/verification.json'),A/'high_impact_priority_huber65_main_receipt_v18_20261010.json',A/'qualified_Return167_prior_screen_csv_cleanup_v1_20261010/verification.json',A/'cleanup_qualified_Return167_prior_screen_csv_v1_20261010.py'")
    pub=pub.replace('当前最佳完整163方案','当前最佳完整167方案')
    for n,text in ((screenname,s),(pubname,pub)):
        assert not (A/n).exists();compile(text,str(A/n),'exec')
        (A/n).write_text(text,encoding='utf8',newline='\n')
    create(A/'Forward20_after167_synergy65_source_admission_v1_20261010.json',{'status':'compiled_and_exact_transformation_AST_preserved_training_only65_hypotheses','input_sha256':{str(p):sha(p) for p in (Path(__file__),original,puboriginal,A/screenname,A/pubname)},'qualified_parent_round':167,'qualified_parent_main':receipt['commit'],'new_native_fits':0,'new_quality_scores':0,'test_X_read':False,'test_labels_read':False,'purpose':'Test whether direct1day+mean20 signals improve over either independently.'})
    from handoff_ready_goss_full_execution_20261006 import start_service
    for service,driver,args in (('actual_Forward20_after167_high_impact65_screen_v1_20261010',screenname,[]),('actual_Forward20_after167_65_completion_main_v20_20261010',pubname,['huber65'])):
        assert allowed()
        row=start_service(service,driver,args,{str(A/driver):sha(A/driver)})
        create(A/(service+'_activation.json'),row)
        print({'name':service,'worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
