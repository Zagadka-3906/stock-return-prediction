"""Prepare fresh4/3 before scoring; preserve failed startup attempts and immutable source versions."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha


def main():
    source=A/'recover_multiyear_136137_queues_v2_20261008.py';target=A/'recover_multiyear_136137_queues_v3_20261008.py'
    text=source.read_text(encoding='utf8')
    text=text.replace("stem+'_v2_20261008.py':stem+'_v3_20261008.py' for stem in CROSS","stem+'_v3_20261008.py':stem+'_v4_20261008.py' for stem in CROSS")
    text=text.replace("stem+'_v1_20261008.py':stem+'_v2_20261008.py' for stem in HUBER","stem+'_v2_20261008.py':stem+'_v3_20261008.py' for stem in HUBER")
    text=text.replace("files['verify_HuberIRLS64_49_current_parent_v2_20261008.py']='verify_HuberIRLS64_49_current_parent_v3_20261008.py'","files['verify_HuberIRLS64_49_current_parent_v3_20261008.py']='verify_HuberIRLS64_49_current_parent_v4_20261008.py'")
    start=text.index("    files['archive_CrossFamily");end=text.index("    mapping=",start);text=text[:start]+text[end:]
    text=text.replace("('CrossFamily94',2,3),('Huber52',1,2)","('CrossFamily94',3,4),('Huber52',2,3)")
    text=text.replace("('CrossFamily94',3),('Huber52',2)","('CrossFamily94',4),('Huber52',3)")
    start=text.index("    for stem,ov,nv in (");end=text.index("    output={}",start)
    text=text[:start]+'''    for stem,ov,nv in (('CrossFamily136_receiver_preparation',3,4),('CrossFamily136_complete_dependency_plan',3,4),
        ('CrossFamily136_complete_hidden_launches',3,4),('Huber137_receiver_preparation',2,3),
        ('Huber137_complete_dependency_plan',2,3),('Huber137_complete_hidden_launches',2,3),
        ('HuberIRLS64_49_current_parent_controls',3,4),('HuberIRLS64_49_current_parent',3,4),
        ('HuberIRLS64_49_current_parent_full',3,4),('actual_HuberIRLS64_49_current_parent_location',3,4),
        ('actual_HuberIRLS64_49_current_parent_full_location',3,4),('CrossFamily94_actual_controls_index',2,3),('Huber52_actual_controls_index',2,3)):
        mapping[stem+f'_v{ov}_20261008']=stem+f'_v{nv}_20261008'
    mapping['multiyear136137_recovery_main_publication_v1_20261008']='multiyear136137_recovery_main_publication_v2_20261008'
''' +text[end:]
    text=text.replace("text.replace('actual_registration_v2_20261008','actual_registration_v3_20261008').replace('registration_v2_file_IO_20261008','registration_v3_file_IO_20261008')","text.replace('actual_registration_v3_20261008','actual_registration_v4_20261008').replace('registration_v3_file_IO_20261008','registration_v4_file_IO_20261008')")
    text=text.replace("text.replace('actual_registration_v1_20261008','actual_registration_v2_20261008').replace('registration_v1_file_IO_20261008','registration_v2_file_IO_20261008')","text.replace('actual_registration_v2_20261008','actual_registration_v3_20261008').replace('registration_v2_file_IO_20261008','registration_v3_file_IO_20261008')")
    text=text.replace("text.replace('transfer_probe_v2','transfer_probe_v3').replace('Transfer_probe_v2','Transfer_probe_v3')","text.replace('transfer_probe_v3','transfer_probe_v4')")
    text=text.replace("text.replace('transfer_probe_v1','transfer_probe_v2')","text.replace('transfer_probe_v2','transfer_probe_v3')")
    start=text.index("        if old.startswith('verify_') and 'round1'");end=text.index("        if old.startswith('prepare_')",start);text=text[:start]+text[end:]
    text=text.replace("'recover_multiyear_136137_queues_v1_20261008.py','multiyear136137_queue_recovery_v1_20261008.json'","'recover_multiyear_136137_queues_v3_20261008.py','multiyear136137_queue_recovery_v2_20261008.json'")
    start=text.index("        if old.startswith('queue_CrossFamily'):");end=text.index("        if old.startswith('prepare_Huber52",start);text=text[:start]+text[end:]
    text=text.replace("from prepare_Huber137_complete_receivers_v1_20261008 import adapt','from prepare_Huber137_complete_receivers_v2_20261008 import adapt","from prepare_Huber137_complete_receivers_v2_20261008 import adapt','from prepare_Huber137_complete_receivers_v3_20261008 import adapt")
    text=text.replace("prepare_Huber137_complete_receivers_v2_20261008.py';assert not adapter.exists()","prepare_Huber137_complete_receivers_v3_20261008.py';assert not adapter.exists()")
    text=text.replace('from prepare_Huber137_complete_receivers_v1_20261008 import adapt as original_adapt','from prepare_Huber137_complete_receivers_v2_20261008 import adapt as original_adapt')
    text=text.replace("Huber52_official_comparison_v2_20261008'\\\",\\\"A/'Huber52_official_comparison_v1_20261008", "Huber52_official_comparison_v3_20261008'\\\",\\\"A/'Huber52_official_comparison_v1_20261008")
    text=text.replace(".replace('Huber52_official_comparison_v2_20261008/", ".replace('Huber52_official_comparison_v3_20261008/")
    text=text.replace("('CrossFamily136',2),('Huber137',1)","('CrossFamily136',3),('Huber137',2)")
    start=text.index("    retired_names += ['CrossFamily136_completed");end=text.index("    audited={}",start)
    text=text[:start]+"    assert len(retired_names)==15 and len(set(retired_names))==15\n"+text[end:]
    text=text.replace("multiyear136137_queue_recovery_v1_20261008.json',","multiyear136137_queue_recovery_v2_20261008.json',")
    text=text.replace("CrossFamily136_receiver_preparation_v3_20261008.json',","CrossFamily136_receiver_preparation_v4_20261008.json',")
    text=text.replace('prepared_fresh136v3_and137v2_after_exact17_dependency_waiter_supersession','prepared_fresh136v4_and137v3_after_exact15_dependency_waiter_supersession')
    text=text.replace('17 exact dependency waiters superseded; fresh136v3 and137v2','15 exact dependency waiters superseded; fresh136v4 and137v3')
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    # Fresh archive names; exact existing E scratch archive is required empty and is safely reused.
    for family in ('CrossFamily136','Huber137'):
        old=A/f'archive_{family}_completed_scoring_CSV_v2_20261008.py';new=A/f'archive_{family}_completed_scoring_CSV_v3_20261008.py'
        body=old.read_text(encoding='utf8')
        needle="assert archive.resolve().is_relative_to(base.resolve());assert not archive.exists();archive.mkdir()";assert body.count(needle)==1
        body=body.replace(needle,"assert archive.resolve().is_relative_to(base.resolve())\n    if archive.exists():assert archive.is_dir() and not any(archive.iterdir())\n    else:archive.mkdir()")
        if family=='CrossFamily136':body=body.replace('CrossFamily94_official_comparison_v3_','CrossFamily94_official_comparison_v4_').replace('CrossFamily94_selected_candidate_preparation_v3_','CrossFamily94_selected_candidate_preparation_v4_')
        else:body=body.replace('Huber52_official_comparison_v2_','Huber52_official_comparison_v3_').replace('Huber52_selected_candidate_preparation_v2_','Huber52_selected_candidate_preparation_v3_')
        assert not new.exists();compile(body,str(new),'exec');new.write_text(body,encoding='utf8',newline='\n')
    create(A/'multiyear136137_startup_failures_v1_20261008.json',{'status':'preserved_before_any_quality',
        'failed_start_reason':'First recovery dispatcher hit an existing empty archive directory, then publisher required its not-yet-written launch record.',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,A/'start_multiyear_136137_recovered_queues_v1_20261008.py',
            A/'publish_multiyear136137_recovery_v1_20261008.py',
            A/'service_owned_workflows_20261006/CrossFamily136_completed_scoring_CSV_archivist_v2_20261008/stderr.log',
            A/'service_owned_workflows_20261006/multiyear136137_recovery_main_publication_v1_20261008/stderr.log']},
        'native_calendar_and_historical_controls_already_passed':True,'new_official_scores':0,'scientific_training_workers_unchanged':True})


if __name__=='__main__':main()
