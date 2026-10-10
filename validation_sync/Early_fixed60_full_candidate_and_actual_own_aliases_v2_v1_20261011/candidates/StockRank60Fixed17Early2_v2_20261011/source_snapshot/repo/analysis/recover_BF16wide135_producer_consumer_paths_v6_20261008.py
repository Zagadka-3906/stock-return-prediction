"""Correct fresh receiver4 paths; retire only eight verified lazy helpers before any scoring."""
from pathlib import Path
import ast,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute


def main():
    proof_path=A/'actual_BF16wide135_producer_consumer_recovery_v6_20261008.json';assert not proof_path.exists()
    old_plan=A/'BF16wide135_complete_dependency_plan_v3_20261008.json';jobs=read(old_plan)['jobs']
    from BF16wide135_storage_v1_20261008 import OUTPUTS,empty
    for path in OUTPUTS:empty(path)
    for name in ('BF16wide40_controls_github_v1_20261008','BF16wide40_scores_github_v1_20261008'):
        assert not (A/name).exists(),name
    assert not (A/'BF16wide135_D_scoring_v2_20261008').exists()
    train_path=A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json';train=read(train_path);assert owned(train)
    names=[name for name,_,_ in jobs]+['BF16wide135_completed_scoring_CSV_archivist_v3_20261008']
    audited={};pairs=[]
    for name in names:
        folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json');assert owned(row)
        dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
        assert dump.returncode==0
        if 'sealing' in name:guard='    main (seal_BF16wide40_selected_candidate_v3_20261008.py:13)'
        elif 'full_registration' in name:guard='    main (run_BF16wide40_round135_full_registration_v3_20261008.py:19)'
        else:guard='    closed ('
        assert guard in dump.stdout,(name,dump.stdout)
        worker,parent=psutil.Process(row['owned_worker_pid']),psutil.Process(row['pid'])
        assert worker.memory_info().rss<256*2**20 and not worker.children()
        assert parent.create_time()==row['owned_parent_creation_time'] and worker.parent().pid==parent.pid
        pairs.append((parent,worker));audited[name]={'identity':row,'actual_lazy_dependency_stack':dump.stdout}
    stems=['prepare_BF16wide40_round135_sources','run_BF16wide40_official_comparison','prepare_BF16wide40_selected_candidate',
        'seal_BF16wide40_selected_candidate','run_BF16wide40_round135_full_registration','verify_BF16wide40_round135_sources',
        'publish_BF16wide40_evidence','queue_BF16wide135_complete_pipeline','record_BF16wide135_receiver_preparation',
        'monitor_BF16wide135_progress','archive_BF16wide135_completed_scoring_CSV','publish_actual_BF16wide135_receiver_preflight']
    files={stem+'_v3_20261008.py':stem+'_v4_20261008.py' for stem in stems}
    files['verify_BF16wide40_prospective_routes_v4_20261008.py']='verify_BF16wide40_prospective_routes_v5_20261008.py'
    mapping={**files,**{old.removesuffix('.py'):new.removesuffix('.py') for old,new in files.items()}}
    for name,_,_ in jobs:mapping[name]=name.replace('_v3_20261008','_v4_20261008')
    for stem in ('BF16wide40_prospective_routes','BF16wide135_receiver_preparation','BF16wide40_round135_source_admission',
        'BF16wide40_round135_source_preparation','BF16wide135_complete_dependency_plan','BF16wide135_complete_hidden_launches',
        'actual_BF16wide135_complete_pipeline_dispatch','BF16wide135_complete_pipeline_dispatch','actual_BF16wide135_receiver_preflight_main',
        'actual_BF16wide135_progress'):
        mapping[stem+'_v3_20261008']=stem+'_v4_20261008'
    outputs={}
    for previous,new in files.items():
        text=substitute((A/previous).read_text(encoding='utf8'),mapping)
        # Physical data and publication folders are deliberately version1; driver/service names are version4.
        for phase in ('controls','scores'):text=text.replace('BF16wide40_'+phase+'_github_v3_20261008','BF16wide40_'+phase+'_github_v1_20261008')
        if previous.startswith('prepare_BF16wide40_round135_sources'):
            text=text.replace("'BF16wide40_official_comparison_v1_20261007','BF16wide40_official_comparison_v4_20261008'", "'BF16wide40_official_comparison_v1_20261007','BF16wide40_official_comparison_v1_20261008'")
            text=text.replace("A/'BF16wide40_official_comparison_v4_20261008'):","A/'BF16wide40_official_comparison_v1_20261008'):")
            text=text.replace("names=[Path(__file__).name,","names=[Path(__file__).name,'actual_BF16wide135_producer_consumer_recovery_v6_20261008.json','verify_BF16wide135_actual_output_contract_v4_20261008.py','BF16wide135_actual_output_contract_v4_20261008.json',")
        if previous.startswith('verify_BF16wide40_prospective'):
            text=text.replace('BF16wide135_transfer_probe_v3_20261008.bin','BF16wide135_transfer_probe_v4_20261008.bin').replace('/transfer_probe_v3.bin','/transfer_probe_v4.bin')
            marker="    create(proof_path,{'status':"
            assert text.count(marker)==1
            text=text.replace(marker,"    contract_path=A/'BF16wide135_actual_output_contract_v4_20261008.json'\n    contract=read(contract_path);assert contract['status']=='passed_actual135_producer_consumer_output_paths_for_all24_generated_receivers'\n    for p,d in contract['input_sha256'].items():assert sha(p)==d,p\n    names += [contract_path,A/'verify_BF16wide135_actual_output_contract_v4_20261008.py',A/'actual_BF16wide135_producer_consumer_recovery_v6_20261008.json']\n"+marker)
        if previous.startswith('run_BF16wide40_round135_full_registration'):
            text=text.replace('BF16wide40_round135_actual_registration_v3_20261008','BF16wide40_round135_actual_registration_v4_20261008')
            text=text.replace('run_BF16wide40_round135_full_registration_v3_file_IO_20261008','run_BF16wide40_round135_full_registration_v4_file_IO_20261008')
        if previous.startswith('archive_'):
            text=text.replace('scoring_CSV_archive_v3_20261008','scoring_CSV_archive_v4_20261008')
            text=text.replace('    archive.mkdir()','    if archive.exists():assert archive.is_dir() and not any(archive.iterdir())\n    else:archive.mkdir()')
        if previous.startswith('publish_actual_'):
            text=text.replace('validation_sync/actual_BF16wide135_receiver_preflight_v3_20261008','validation_sync/actual_BF16wide135_receiver_preflight_v4_20261008')
            marker='    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}'
            assert text.count(marker)==1
            text=text.replace(marker,"    sources += [A/'actual_BF16wide135_producer_consumer_recovery_v6_20261008.json',A/'recover_BF16wide135_producer_consumer_paths_v6_20261008.py',A/'verify_BF16wide135_actual_output_contract_v4_20261008.py',A/'BF16wide135_actual_output_contract_v4_20261008.json']\n"+marker)
        assert not (A/new).exists();compile(text,str(A/new),'exec');outputs[A/new]=text
    # Validate the fresh physical publication/CDF paths before any administrative retirement.
    for text in outputs.values():
        assert 'BF16wide40_controls_github_v3_20261008' not in text and 'BF16wide40_scores_github_v3_20261008' not in text
        assert "A/'BF16wide40_official_comparison_v4_20261008')" not in text
    for name,(parent,worker) in zip(names,pairs):
        assert owned(audited[name]['identity'])
        worker.terminate();worker.wait(timeout=10);parent.terminate();parent.wait(timeout=10)
        create(A/'service_owned_workflows_20261006'/name/'administrative_supersession_for_actual_output_paths_20261008.json',{
            'status':'retired_only_verified_lazy_waiter_before_any_quality_or_future_X','original_identity':audited[name]['identity'],
            'reason':'Fresh4 uses actual physical version1 producer folders; immutable original3 inputs are retained.',
            'new_quality_scores':0,'scientific_workers_stopped':0})
    assert owned(train)
    for path in OUTPUTS:empty(path)
    for path,text in outputs.items():path.write_text(text,encoding='utf8',newline='\n')
    create(proof_path,{'status':'retired_exact8_lazy_helpers_and_prepared_fresh4_actual_producer_consumer_paths',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'audited_old_jobs':audited,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old_plan,train_path,*outputs]},
        'actual_retired_lazy_waiters':8,'annual_fitter_unchanged_live':train,'original_quality_scores':0,'original_future_X_calls':0,
        'physical_comparison_release_folders_still_version1':True,'physical_publication_folders_still_version1':True,
        'driver_and_service_names_fresh4':True,'new_actual_output_contract_and24_receiver_checks_required':True,'test_labels_read':False})
    print('Exact8 lazy helpers retired; fresh4 sources use true physical version1 output folders.',flush=True)


if __name__=='__main__':main()
