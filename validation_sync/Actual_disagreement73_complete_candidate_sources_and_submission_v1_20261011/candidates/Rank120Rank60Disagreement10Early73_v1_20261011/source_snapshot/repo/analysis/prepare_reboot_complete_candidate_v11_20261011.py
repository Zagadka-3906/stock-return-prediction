"""Evidence-based reboot recovery of idle dispatchers and already-completed37 scores."""
from pathlib import Path
import sys,importlib,re,time,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_actual_candidate_closed180_continuation_v10_20261011 import DESCRIPTORS
PROOF=A/'reboot_complete_candidate_routes_v11_20261011.json'
def save(name,text):
    path=A/name;assert not path.exists(),path;compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return path
def main():
    assert allowed();old=read(A/'actual_candidate_closed180_continuation_routes_v10_20261011.json')
    assert psutil.boot_time()>1791648000
    aliases={}
    for name in ['Dual25_verified_recovery_exact_dependency_aliases_v7_20261010.json','actual_PairRank_native42_admission_routes_v8_20261010.json','PairTop184185_complete_reference_routes_v9_20261010.json','actual_candidate_closed180_continuation_routes_v10_20261011.json']:
        aliases.update(read(A/name)['service_aliases'])
    originals=dict(aliases);factories=[];drivers=[];tasks=[];pinsources=[Path(__file__),A/'route_reboot_complete_candidate_v11_20261011.py',A/'resume180_completed_candidate_reboot_v11_20261011.py',A/'adopt_completed_two_seed_protected37_pointer_v2_20261011.py',A/'actual_candidate_closed180_continuation_routes_v10_20261011.json']
    for n,d in old['remaining_tasks']:
        f=A/'service_owned_workflows_20261006'/n;assert not owned(read(f/'native_launch.json')),n
    def setalias(canonical,actual):
        previous=aliases.get(canonical,canonical)
        for key,value in list(aliases.items()):
            if value==previous or key==previous:aliases[key]=actual
        aliases[canonical]=actual;aliases[previous]=actual
    setalias('main_publisher_v11_20261010','main_publisher_reboot_v12_20261011')
    root='StockRank20Embedding180_complete48_family_v6_20261010'
    setalias(root,'StockRank20Embedding180_complete48_reboot_v11_20261011')
    tasks.append((aliases[root],'resume180_completed_candidate_reboot_v11_20261011.py'))
    for n,factoryname,norm,qual,family in DESCRIPTORS:
        f=importlib.import_module(factoryname);factories.append(factoryname)
        for canonical,driver in [(norm,f.EXTRAS[0]),(qual,f.EXTRAS[1]),(family,f.EXTRAS[5])]:
            setalias(canonical,'reboot11_'+canonical);tasks.append((aliases[canonical],driver))
        text=(A/f.EXTRAS[5]).read_text(encoding='utf8')
        for service in re.findall(r"['\"]([A-Za-z0-9_]+)['\"]",text):
            if service.startswith(('Stock','Rank20')) and any(x in service for x in ('_selected_candidate_preparation_','_selected_candidate_sealing_',f'_round{n}_full_registration_')):
                setalias(service,'reboot11_'+service)
        drivers.extend([*f.EXTRAS[:2],*f.EXTRAS[3:9]])
        for driver in f.EXTRAS[:2]:
            module=importlib.import_module(Path(driver).stem)
            if module.OUT.exists():
                # Some import-time TEMP settings left empty scratch directories, never a scientific record.
                assert module.OUT.resolve().is_relative_to(Path('E:/赛题五_本机临时').resolve())
                assert all(p.is_dir() for p in module.OUT.rglob('*')),module.OUT
                for p in sorted(module.OUT.rglob('*'),key=lambda p:len(p.parts),reverse=True):p.rmdir()
                module.OUT.rmdir()
            assert not module.OUT.exists(),module.OUT
        storage=importlib.import_module(Path(f.EXTRAS[2]).stem)
        assert all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items()),n
    for service in ['StockRank20Embedding180_selected_candidate_sealing_v1_20261010','StockRank20Embedding180_round180_full_registration_v1_20261010']:
        setalias(service,'reboot11_'+service)
    drivers+=['seal_StockRank20Embedding180_selected_candidate_v2_20261010.py','run_StockRank20Embedding180_full_registration_v5_20261010.py']
    factories.insert(0,'prepare_StockRank20Embedding180_complete48_pipeline_v1_20261010')
    setalias('actual_rank20_two_seed_after175_protected_tail37_screen_v1_20261011','actual_rank20_two_seed_protected37_completed_admission_v2_20261011')
    setalias('actual_rank20_two_seed_protected_selected_native14_v1_20261011','actual_rank20_two_seed_protected_selected_native14_reboot_v2_20261011')
    drivers.append('verify_rank20_two_seed_protected_selected_native14_v1_20261011.py')
    tasks.insert(0,(aliases['actual_rank20_two_seed_after175_protected_tail37_screen_v1_20261011'],'adopt_completed_two_seed_protected37_pointer_v2_20261011.py'))
    tasks.append((aliases['actual_rank20_two_seed_protected_selected_native14_v1_20261011'],'verify_rank20_two_seed_protected_selected_native14_v1_20261011.py'))
    wrappers={};replacements=dict(aliases)
    pattern=re.compile(r'(?<![A-Za-z0-9_])('+ '|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
    for driver in dict.fromkeys(drivers):
        original=A/driver;pinsources.append(original);executed=driver
        if driver.startswith('seal_') or '_full_registration_' in driver:
            text=pattern.sub(lambda m:replacements[m.group()],original.read_text(encoding='utf8'))
            executed=Path(driver).stem+'_reboot_services_v11.py';pinsources.append(save(executed,text))
        target=Path(driver).stem+'_reboot_wrapper_v11.py'
        pinsources.append(save(target,"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_reboot_complete_candidate_v11_20261011 import execute\nif __name__=='__main__':execute("+repr(executed)+")\n"))
        wrappers[driver]=target
    for original,wrapped in old['driver_wrappers'].items():
        if original in wrappers:wrappers[wrapped]=wrappers[original]
    create(PROOF,{'status':'verified_reboot_dead_owned_dispatchers_and_completed180_candidate_continuation','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'boot_time':psutil.boot_time(),'service_aliases':aliases,'driver_wrappers':wrappers,'source_factories':factories,'input_sha256':{str(p):sha(p) for p in dict.fromkeys(pinsources)},'remaining_tasks':tasks,'new_model_fits':0,'new_quality_scores':0,'original_failed_services_preserved':True})
    # A new post-reboot deadline guard, with a new identity/folder; no old guard is restarted.
    oldguard=A/'user_requested_stop1100_until_manual_continue_v1_20261011'
    assert not owned(read(oldguard/'actual_schedule_activation.json')['identity'])
    folder=A/'user_requested_stop1100_reboot_guard_v2_20261011';folder.mkdir(exist_ok=False)
    config=read(oldguard/'schedule.json');config['output_folder']=str(folder);create(folder/'schedule.json',config)
    create(folder/'handoff_committed.json',{'status':'new_guard_for_same_user_deadline_after_verified_reboot','old_guard_not_restarted':True})
    row=start_service('actual_user_stop1100_reboot_guard_v2_20261011','user_requested_stop1100_v1_20261011.py',['run','--folder',str(folder)],{str(folder/'schedule.json'):sha(folder/'schedule.json')})
    create(folder/'actual_schedule_activation.json',{'status':'actual_owned_new_post_reboot_guard_started','identity':row,'stop_at_local':config['stop_at_local'],'old_guard_not_restarted':True})
    from atomic_optimization_observer_writes_20261005 import write
    for filename in ['current_user_runtime_control_20261010.json','current_user_runtime_control_20261009.json']:
        c=read(A/filename);c.update(schedule=str(folder/'schedule.json'),activation=str(folder/'actual_schedule_activation.json'),guard_status=str(folder/'guardian_status.json'),disk_recovery_manifest=str(folder/'disk_recovery_manifest.json'));write(A/filename,c)
    assert allowed();publisher=start_service('main_publisher_reboot_v12_20261011','watch_validations_main_safe_v11_20261010.py',[],{str(A/'watch_validations_main_safe_v11_20261010.py'):sha(A/'watch_validations_main_safe_v11_20261010.py')});create(A/'main_publisher_reboot_v12_activation_20261011.json',publisher)
    for name,driver in tasks:
        assert allowed();driver=wrappers.get(driver,driver)
        try:row=start_service(name,driver,[],{str(PROOF):sha(PROOF),str(A/driver):sha(A/driver)})
        except AssertionError:
            f=A/'service_owned_workflows_20261006'/name;assert read(f/'service_execution.json')['status']=='passed';row=read(f/'native_launch.json')
        create(A/(name+'_reboot_activation.json'),row)
    print({'started_reboot_continuations':len(tasks),'completed_models_retrained':0,'completed_scores_repeated':0},flush=True)
if __name__=='__main__':main()
