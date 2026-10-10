"""Preserve immutable receipts; supersede only waiting136/137 helpers with calendar-admitted versions."""
from pathlib import Path
import ast,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

CROSS=('prepare_CrossFamily94_round136_sources','run_CrossFamily94_official_comparison','prepare_CrossFamily94_selected_candidate',
    'seal_CrossFamily94_selected_candidate','run_CrossFamily94_round136_full_registration','verify_CrossFamily94_round136_sources',
    'publish_CrossFamily94_evidence','queue_CrossFamily136_complete_pipeline','verify_CrossFamily94_prospective_routes')
HUBER=('prepare_Huber52_round137_sources','run_Huber52_official_comparison','prepare_Huber52_selected_candidate',
    'seal_Huber52_selected_candidate','run_Huber52_round137_full_registration','verify_Huber52_round137_sources',
    'publish_Huber52_evidence','queue_Huber137_complete_pipeline','verify_Huber52_prospective_routes','record_Huber137_receiver_preparation')


def main():
    from CrossFamily136_storage_v1_20261008 import OUTPUTS as CO,empty
    from Huber137_storage_v1_20261008 import OUTPUTS as HO,empty as huber_empty
    for path in CO:empty(path)
    for path in HO:huber_empty(path)
    preparation=A/'multiyear_residual_native_preparation_v1_20261008.json';proof=read(preparation)
    for p,d in {**proof['old_source_sha256'],**proof['new_source_sha256']}.items():assert sha(p)==d,p
    files={stem+'_v3_20261008.py':stem+'_v4_20261008.py' for stem in CROSS}
    files.update({stem+'_v2_20261008.py':stem+'_v3_20261008.py' for stem in HUBER})
    files['verify_HuberIRLS64_49_current_parent_v3_20261008.py']='verify_HuberIRLS64_49_current_parent_v4_20261008.py'
    mapping={**proof['mapping'],**{Path(old).stem:Path(new).stem for old,new in files.items()}}
    for family,oldversion,newversion in (('CrossFamily94',3,4),('Huber52',2,3)):
        for stem in (family+'_round'+('136' if family=='CrossFamily94' else '137')+'_source_admission',
            family+'_round'+('136' if family=='CrossFamily94' else '137')+'_source_preparation',
            family+'_controls_main_publication',family+'_scores_main_publication',family+'_official_comparison',
            family+'_selected_candidate_preparation',family+'_selected_candidate_sealing',
            family+'_round'+('136' if family=='CrossFamily94' else '137')+'_full_registration',family+'_prospective_routes'):
            mapping[stem+f'_v{oldversion}_20261008']=stem+f'_v{newversion}_20261008'
    for stem,ov,nv in (('CrossFamily136_receiver_preparation',3,4),('CrossFamily136_complete_dependency_plan',3,4),
        ('CrossFamily136_complete_hidden_launches',3,4),('Huber137_receiver_preparation',2,3),
        ('Huber137_complete_dependency_plan',2,3),('Huber137_complete_hidden_launches',2,3),
        ('HuberIRLS64_49_current_parent_controls',3,4),('HuberIRLS64_49_current_parent',3,4),
        ('HuberIRLS64_49_current_parent_full',3,4),('actual_HuberIRLS64_49_current_parent_location',3,4),
        ('actual_HuberIRLS64_49_current_parent_full_location',3,4),('CrossFamily94_actual_controls_index',2,3),('Huber52_actual_controls_index',2,3)):
        mapping[stem+f'_v{ov}_20261008']=stem+f'_v{nv}_20261008'
    mapping['multiyear136137_recovery_main_publication_v1_20261008']='multiyear136137_recovery_main_publication_v2_20261008'
    output={};old_sources=[]
    for old,new in files.items():
        source=A/old;old_sources.append(source);text=substitute(source.read_text(encoding='utf8'),mapping)
        # Scientific output directories and original D scoring scopes remain their exact, empty version1 locations.
        for family,nv in (('CrossFamily94',4),('Huber52',3)):
            bad=family+f'_official_comparison_v{nv}_20261008';good=family+'_official_comparison_v1_20261008'
            text=text.replace("A/'"+bad+"'","A/'"+good+"'")
            text=text.replace(bad+'/verification.json',good+'/verification.json').replace(bad+'/frozen_before',good+'/frozen_before')
        if old.startswith('run_CrossFamily94_round136_full_registration'):
            text=text.replace('actual_registration_v3_20261008','actual_registration_v4_20261008').replace('registration_v3_file_IO_20261008','registration_v4_file_IO_20261008')
        if old.startswith('run_Huber52_round137_full_registration'):
            text=text.replace('actual_registration_v2_20261008','actual_registration_v3_20261008').replace('registration_v2_file_IO_20261008','registration_v3_file_IO_20261008')
        if old.startswith('verify_CrossFamily94_prospective'):
            text=text.replace('transfer_probe_v3','transfer_probe_v4')
        if old.startswith('verify_Huber52_prospective'):
            text=text.replace('transfer_probe_v2','transfer_probe_v3')
        if old.startswith('prepare_') and 'round1' in old and '_sources_' in old:
            marker='names=[Path(__file__).name,';assert text.count(marker)==1
            text=text.replace(marker,marker+"'recover_multiyear_136137_queues_v3_20261008.py','multiyear136137_queue_recovery_v2_20261008.json','verify_multiyear_residual_native_calendar_v1_20261008.py','multiyear_residual_native_preparation_v1_20261008.json','actual_multiyear_residual_calendar_location_v1_20261008.json',")
        if old.startswith('archive_'):
            text=text.replace('    archive.mkdir()',"    if archive.exists():assert archive.is_dir() and not any(archive.iterdir())\n    else:archive.mkdir()")
        if old.startswith('prepare_Huber52_round137_sources'):
            # This immutable source generator deliberately still consumes the original ancestor as a template.
            text=text.replace('import prepare_CrossFamily94_round136_sources_v3_20261008 as original','import prepare_CrossFamily94_round136_sources_v2_20261008 as original')
            text=text.replace('from prepare_Huber137_complete_receivers_v2_20261008 import adapt','from prepare_Huber137_complete_receivers_v3_20261008 import adapt')
        target=A/new;assert not target.exists();compile(text,str(target),'exec');output[target]=text
    # Re-export the original scientific conversion, then update only downstream names and calendar-native modules.
    adapter=A/'prepare_Huber137_complete_receivers_v3_20261008.py';assert not adapter.exists()
    adapter_text="from prepare_Huber137_complete_receivers_v2_20261008 import adapt as original_adapt\nfrom prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute\nMAPPING="+repr(mapping)+"\ndef adapt(text):\n    value=substitute(original_adapt(text),MAPPING)\n    value=value.replace(\"A/'Huber52_official_comparison_v3_20261008'\",\"A/'Huber52_official_comparison_v1_20261008'\").replace('Huber52_official_comparison_v3_20261008/verification.json','Huber52_official_comparison_v1_20261008/verification.json').replace('Huber52_official_comparison_v3_20261008/frozen_before','Huber52_official_comparison_v1_20261008/frozen_before')\n    return value\n"
    compile(adapter_text,str(adapter),'exec');output[adapter]=adapter_text
    retired_names=[]
    for family,ov in (('CrossFamily136',3),('Huber137',2)):
        launches=read(A/(family+f'_complete_hidden_launches_v{ov}_20261008.json'))['launches']
        retired_names += [name for name in launches if name!='CrossFamily91_current_parent_controls_v1_20261008']
    assert len(retired_names)==15 and len(set(retired_names))==15
    audited={};pairs=[]
    fitter=read(A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json');assert owned(fitter)
    for name in retired_names:
        folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json')
        if not owned(row):
            assert read(folder/'service_execution.json')['status']=='failed',name
            audited[name]={'identity':row,'already_closed_failed_dependency':True,'terminal':read(folder/'service_execution.json')}
            continue
        dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
        assert dump.returncode==0
        allowed='    closed (' in dump.stdout or ('    main (seal_' in dump.stdout) or ('    main (run_' in dump.stdout and '_full_registration_' in dump.stdout)
        assert allowed,(name,dump.stdout)
        worker,parent=psutil.Process(row['owned_worker_pid']),psutil.Process(row['pid'])
        assert worker.memory_info().rss<256*2**20 and not worker.children()
        assert parent.create_time()==row['owned_parent_creation_time'] and worker.parent().pid==parent.pid
        audited[name]={'identity':row,'actual_dependency_wait_stack':dump.stdout};pairs.append((name,parent,worker))
    for name,parent,worker in pairs:
        assert owned(audited[name]['identity']);worker.terminate();worker.wait(timeout=10);parent.terminate();parent.wait(timeout=10)
        create(A/'service_owned_workflows_20261006'/name/'administrative_calendar_supersession_v1_20261008.json',{
            'status':'retired_only_owned_low_memory_dependency_waiter_before_quality',
            'reason':'Predict dates span2025 and2026; fresh frozen2025 native stages admit both years without refitting.',
            'original_identity':audited[name]['identity'],'new_quality_scores':0,'scientific_training_workers_stopped':0})
    assert owned(fitter)
    for p in CO:empty(p)
    for p in HO:huber_empty(p)
    for p,text in output.items():p.write_text(text,encoding='utf8',newline='\n')
    create(A/'multiyear136137_queue_recovery_v2_20261008.json',{
        'status':'prepared_fresh136v4_and137v3_after_exact15_dependency_waiter_supersession',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'audited_retired_jobs':audited,
        'preserved_old_source_sha256':{str(p):sha(p) for p in old_sources},'generated_source_sha256':{str(p):sha(p) for p in output},
        'original_CDF_math_grid_fit_models_and_official_scoring_unchanged':True,'fitter_still_owned':fitter,
        'new_official_scores':0,'new_fits':0,'new_future_X_calls':0,'test_labels_read':False})
    # Record136 preparation before its new prospective control references the proof.
    create(A/'CrossFamily136_receiver_preparation_v4_20261008.json',{
        'status':'prepared_complete94_calendar_safe_receivers_before_quality',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),preparation,*output]},
        'new_quality_scores':0,'actual_future_X_calls':0,'actual24_new_prospective_controls_still_required':True})
    print('15 exact dependency waiters superseded; fresh136v4 and137v3 compiled, scientific fits preserved.',flush=True)


if __name__=='__main__':main()
