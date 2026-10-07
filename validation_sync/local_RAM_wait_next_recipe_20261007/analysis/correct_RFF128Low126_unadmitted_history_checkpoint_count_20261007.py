"""Preserve pre-admission source history and use the actual saved fit count in publication."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    assert not (A/'nonflag_RFF128Low76_round126_source_admission_v1_20261007.json').exists()
    assert not (A/'nonflag_RFF128Low76_official_comparison_v1_20261007').exists()
    saved=read(A/'RFF128Low_checkpoint_resume_snapshot_20261007.json')['saved_native_fit_count']
    assert saved==read(A/'nonflag_residual_RFF128Low_bank10_20261007/verification.json')['reused_saved_native_fits']
    out=A/'RFF128Low126_unadmitted_publication_source_correction_20261007';assert not out.exists();out.mkdir()
    pub=A/'publish_RFF128Low_actual_history_after125_20261007.py'
    newpub=A/'publish_RFF128Low_actual_history_after125_v2_20261007.py';assert not newpub.exists()
    text=pub.read_text(encoding='utf8')
    text=text.replace("assert native['actual_native_fits']==10 and native['reused_saved_native_fits']==2 and native['actual_new_native_fits_by_resume']==8",
        "saved=read(A/'RFF128Low_checkpoint_resume_snapshot_20261007.json')['saved_native_fit_count']\n    assert native['actual_native_fits']==10 and native['reused_saved_native_fits']==saved and native['actual_new_native_fits_by_resume']==10-saved")
    text=text.replace("handoff['saved_native_fits_preserved']==2", "handoff['saved_native_fits_preserved']==saved")
    text=text.replace("'saved_fits_reused':2", "'saved_fits_reused':saved").replace("'new_fits_by_resume':8", "'new_fits_by_resume':10-saved")
    compile(text,str(newpub),'exec');newpub.write_text(text,encoding='utf8',newline='\n')
    phase=A/'publish_nonflag_RFF128Low76_evidence_v1_20261007.py'
    oldbytes=phase.read_bytes();(out/phase.name).write_bytes(oldbytes)
    text=oldbytes.decode('utf8');assert text.count('RFF128Low_actual_history_main_after125')==1
    text=text.replace('RFF128Low_actual_history_main_after125','RFF128Low_actual_history_main_after125_v2')
    compile(text,str(phase),'exec');phase.write_text(text,encoding='utf8',newline='\n')
    admit=A/'start_nonflag_RFF128Low76_actual_admission_20261007.py'
    newadmit=A/'start_nonflag_RFF128Low76_actual_admission_v2_20261007.py';assert not newadmit.exists()
    text=admit.read_text(encoding='utf8').replace('science_route_preparation_v1_20261007.json','science_route_preparation_v2_20261007.json')
    compile(text,str(newadmit),'exec');newadmit.write_text(text,encoding='utf8',newline='\n')
    controller=A/'continue_nonflag_RFF128Low76_after_actual_admission_v1_20261007.py'
    newcontroller=A/'continue_nonflag_RFF128Low76_after_actual_admission_v2_20261007.py';assert not newcontroller.exists()
    text=controller.read_text(encoding='utf8').replace('from start_nonflag_RFF128Low76_actual_admission_20261007 import start',
        'from start_nonflag_RFF128Low76_actual_admission_v2_20261007 import start')
    compile(text,str(newcontroller),'exec');newcontroller.write_text(text,encoding='utf8',newline='\n')
    queue=A/'queue_nonflag_RFF128Low76_actual_admission_and_pipeline_20261007.py'
    newqueue=A/'queue_nonflag_RFF128Low76_actual_admission_and_pipeline_v2_20261007.py';assert not newqueue.exists()
    text=queue.read_text(encoding='utf8').replace('RFF128Low_actual_history_main_after125','RFF128Low_actual_history_main_after125_v2')
    text=text.replace('from start_nonflag_RFF128Low76_actual_admission_20261007 import main',
        'from start_nonflag_RFF128Low76_actual_admission_v2_20261007 import main')
    text=text.replace('from continue_nonflag_RFF128Low76_after_actual_admission_v1_20261007 import main',
        'from continue_nonflag_RFF128Low76_after_actual_admission_v2_20261007 import main')
    compile(text,str(newqueue),'exec');newqueue.write_text(text,encoding='utf8',newline='\n')
    oldprep=A/'nonflag_RFF128Low76_science_route_preparation_v1_20261007.json'
    paths=list(dict.fromkeys([Path(p) for p in read(oldprep)['input_sha256']]+[Path(__file__),oldprep,
        newpub,newqueue,newadmit,newcontroller,out/phase.name,
        A/'verify_nonflag_RFF128Low76_prospective_routes_v2_20261007.py']))
    pins={str(p):sha(p) for p in paths}
    prep=A/'nonflag_RFF128Low76_science_route_preparation_v2_20261007.json'
    create(prep,{'status':'compiled_actual_checkpoint_count_corrected_before126_admission_or_scores',
        'input_sha256':pins,'actual_checkpointed_native_fits':saved,'actual_official_scores':0,
        'preserved_prior_unadmitted_source':str(out/phase.name),'test_labels_read':False})
    create(out/'correction_record.json',{'status':'actual_saved_checkpoint_count_correction_before_any126_admission_or_official_scores',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_saved_native_fits':saved,
        'incorrect_prior_publication_literal_saved_count':2,'original_scientific_models_or_score_math_changed':False,
        'original_publication_and_queue_must_preserve_their_real_failure':True,'actual_official_scores':0,'input_sha256':pins})
    from handoff_ready_goss_full_execution_20261006 import start_service
    publisher=start_service('RFF128Low_actual_history_main_after125_v2',newpub.name,[],{str(newpub):sha(newpub)})
    queued=start_service('nonflag_RFF128Low76_actual_admission_dependency_queue_v2',newqueue.name,[],{**pins,str(prep):sha(prep)})
    create(A/'nonflag_RFF128Low76_corrected_dependency_queue_hidden_launch_20261007.json',
        {'publisher':publisher,'admission_queue':queued,'actual_saved_native_fits':saved,'new_quality_scores_by_launcher':0})
if __name__=='__main__':main()
