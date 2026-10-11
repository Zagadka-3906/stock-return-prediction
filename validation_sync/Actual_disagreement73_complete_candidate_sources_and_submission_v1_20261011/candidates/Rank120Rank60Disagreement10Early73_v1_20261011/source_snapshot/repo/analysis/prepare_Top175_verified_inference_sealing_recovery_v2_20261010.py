"""Finish sealing the already verified candidate; preserve its frozen inference and partial evidence."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed();closed('StockTop10Embedding175_selected_candidate_preparation_v1_20261010')
    old=A/'seal_StockTop10Embedding175_selected_candidate_v1_20261010.py';new=A/'seal_StockTop10Embedding175_selected_candidate_recovery_v2_20261010.py'
    release=A/'StockTop10Embedding175_selected_release_v1_20261010';ready=read(release/'inference_ready.json');candidate=Path(ready['source_candidate'])
    assert ready['new_inference_claimed'] and not (candidate/'manifest.json').exists() and not (release/'selected_candidate_ready_for_registration.json').exists()
    failure=A/'service_owned_workflows_20261006/StockTop10Embedding175_selected_candidate_sealing_v1_20261010/service_execution.json';assert read(failure)['status']=='failed'
    text=old.read_text(encoding='utf8');needle="target.parent.mkdir(parents=True,exist_ok=True);os.link(source,target);assert sha(target)==info['sha256']";assert text.count(needle)==1
    text=text.replace(needle,"target.parent.mkdir(parents=True,exist_ok=True)\n        if target.exists():assert sha(target)==info['sha256']\n        else:os.link(source,target)\n        assert sha(target)==info['sha256']")
    needle="    create(candidate/'source_package_verification.json'";assert text.count(needle)==1
    text=text.replace(needle,"    recovery=A/'Top175_verified_inference_sealing_recovery_v2_20261010.json'\n    import shutil\n    target=candidate/'evidence/sealing_recovery_v2_20261010.json';assert not target.exists();shutil.copyfile(recovery,target);assert sha(target)==sha(recovery)\n"+needle)
    assert not new.exists();compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    partial={p.relative_to(candidate).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in (candidate/'source_snapshot').rglob('*') if p.is_file()}
    create(A/'Top175_verified_inference_sealing_recovery_v2_20261010.json',{'status':'verified_completed_new_candidate_inference_preserved_resuming_partial_evidence_sealing_only','input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,failure,release/'inference_ready.json',candidate/'verification.json',candidate/'submission.csv']},'verified_partial_source_snapshot':partial,'actual_csv_sha256':sha(candidate/'submission.csv'),'new_fits':0,'new_scores':0,'new_inference':0,'old_sealer_failure_preserved':True,'cross_drive_copy_inside_original_storage_scope':True})
    assert allowed();name='StockTop10Embedding175_selected_candidate_sealing_recovery_v2_20261010';row=start_service(name,new.name,[],{str(new):sha(new)});create(A/(name+'_activation.json'),row)
    print({'actual_new_candidate_inference_preserved':True,'partial_snapshot_files':len(partial),'sealing_only_started':name},flush=True)
if __name__=='__main__':main()
