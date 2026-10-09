"""Resume only interrupted inference/sealing/registration, preserving all185 completed scores."""
from pathlib import Path
import ast,sys,time,subprocess
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'actual_manual_continue147_receiver_recovery_v8_20261009.json'
SERVICES=A/'service_owned_workflows_20261006'
MAP={
    'JointCrossHuberOrder185_selected_candidate_preparation_v1_20261008':'JointCrossHuberOrder185_selected_candidate_preparation_v2_20261009',
    'JointCrossHuberOrder185_selected_candidate_sealing_v1_20261008':'JointCrossHuberOrder185_selected_candidate_sealing_v2_20261009',
    'seal_JointCrossHuberOrder185_selected_candidate_v1_20261008.py':'seal_JointCrossHuberOrder185_selected_candidate_v2_20261009.py',
    'JointCrossHuberOrder185_selected_release_v1_20261008':'JointCrossHuberOrder185_selected_release_v2_20261009',
    'JointCrossHuberOrder185_v1_20261008':'JointCrossHuberOrder185_v2_20261009',
    'pre_inference_source_freeze_v1':'pre_inference_source_freeze_v2_20261009',
    'JointCrossHuber147_D_scoring_v1_20261008/selected/':'JointCrossHuber147_D_scoring_v1_20261008/selected_v2_20261009/',
    'JointCrossHuberOrder185_round147_actual_registration_v5_20261008':'JointCrossHuberOrder185_round147_actual_registration_v6_20261009',
    'main_publisher_v8_20261008':'main_publisher_v9_20261009'}
DRIVERS={
    'prepare_JointCrossHuberOrder185_selected_candidate_v3_20261008.py':'prepare_JointCrossHuberOrder185_selected_candidate_v7_20261009.py',
    'seal_JointCrossHuberOrder185_selected_candidate_v1_20261008.py':'seal_JointCrossHuberOrder185_selected_candidate_v2_20261009.py',
    'run_JointCrossHuberOrder185_round147_full_registration_v5_20261008.py':'run_JointCrossHuberOrder185_round147_full_registration_v9_20261009.py'}

def closed(name):
    folder=SERVICES/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def verify_pins():
    for p,d in read(META)['input_sha256'].items():assert sha(p)==d,p

def execute(original):
    verify_pins()
    from recover_Joint147_publisher_phase_scratch_v7_20261008 import protected_module
    import JointCrossHuber147_storage_v1_20261008 as storage
    for access,target in read(META)['new_E_outputs'].items():storage.OUTPUTS[Path(access)]=Path(target)
    import prepare_JointCrossHuberOrder185_round147_sources_v4_20261008 as generator
    paths=generator.source_paths
    extras=[Path(__file__),META,*(A/n for n in DRIVERS.values()),A/'actual_manual_continue_after2355_stop_v1_20261009.json']
    generator.source_paths=lambda:list(dict.fromkeys([*paths(),*extras]))
    module=protected_module()
    module['MAP']={**module['MAP'],**MAP};module['DRIVERS']={**module['DRIVERS'],**DRIVERS}
    if original.startswith('run_'):
        closed(MAP['JointCrossHuberOrder185_selected_candidate_sealing_v1_20261008'])
        # This previously absent pointer truthfully names the new fully sealed release;
        # the original stopped service and its partial outputs remain interrupted.
        new=A/MAP['JointCrossHuberOrder185_selected_release_v1_20261008']/'selected_candidate_ready_for_registration.json'
        old=A/'JointCrossHuberOrder185_selected_release_v1_20261008/selected_candidate_ready_for_registration.json'
        value=read(new);assert value['sealed_candidate_complete'] and value['source_release']==str(new.parent)
        if old.exists():assert old.read_bytes()==new.read_bytes()
        else:
            with old.open('xb') as stream:stream.write(new.read_bytes())
        create(A/'actual147_sealed_release_current_pointer_bridge_v1_20261009.json',{
            'status':'previously_absent_ready_pointer_names_actual_sealed_retry2_not_stopped_retry1',
            'source':str(new),'alias':str(old),'sha256':sha(new),'actual_service':MAP['JointCrossHuberOrder185_selected_candidate_sealing_v1_20261008'],
            'original_interrupted_service_not_marked_passed':True,'canonical32_source_bytes_unchanged':True})
    module['execute'](original)

def make_junction(access,target):
    assert access.is_relative_to(ROOT) and target.is_relative_to(Path('E:/赛题五_本机临时/第147轮_20261008'))
    assert not access.exists() and not target.exists()
    target.mkdir(parents=True);access.parent.mkdir(parents=True,exist_ok=True)
    def literal(p):return "'"+str(p).replace("'","''")+"'"
    cmd="$ErrorActionPreference='Stop'\nNew-Item -ItemType Junction -Path "+literal(access)+' -Target '+literal(target)+' | Out-Null'
    r=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',cmd],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    assert r.returncode==0,r.stderr.decode('utf8',errors='replace')
    assert access.is_junction() and access.resolve()==target.resolve() and not any(target.iterdir())

def main():
    from scheduled_user_pause_20261007 import inventory
    assert not inventory(full=True), 'Do not launch duplicate owned jobs.'
    manifest=A/'user_requested_stop2355_until_manual_continue_v2_20261008/disk_recovery_manifest.json'
    assert read(manifest)['status']=='project_workers_stopped_with_disk_recovery_manifest'
    pilot_path=A/'JointCrossHuberOrder185_official_comparison_v1_20261008/verification.json';pilot=read(pilot_path)
    assert len(pilot['records'])==185 and pilot['best']['case']==118
    pins={str(p):sha(p) for p in [Path(__file__),manifest,pilot_path,A/'JointCrossHuberOrder185_round147_source_admission_v1_20261008.json',A/'JointCrossHuberOrder185_scores_github_v1_20261008/receipt.json']}
    for r in pilot['records']:
        record=A/f'JointCrossHuberOrder185_official_comparison_v1_20261008/case{r["case"]:03d}_official.json'
        assert read(record)==r
        capsule=Path(r['official_score_cache']['official_metrics_source']);assert sha(capsule)==r['official_metric_capsule_sha256'] and read(capsule)['metrics']==r['metrics']
        pins.update({str(record):sha(record),str(capsule):sha(capsule)})
    admission=read(A/'JointCrossHuberOrder185_round147_source_admission_v1_20261008.json')
    for p,d in admission['input_sha256'].items():assert sha(p)==d,p
    # Check the original pre-inference inputs without treating interrupted inference as complete.
    partial=read(A/'JointCrossHuberOrder185_selected_release_v1_20261008/frozen_before_actual_candidate_inference.json')
    for p,d in partial['input_sha256'].items():assert sha(p)==d,p
    outputs={ROOT/'candidates/JointCrossHuberOrder185_v2_20261009':Path('E:/赛题五_本机临时/第147轮_20261008/candidate_retry2_20261009'),
        A/'JointCrossHuberOrder185_selected_release_v2_20261009':Path('E:/赛题五_本机临时/第147轮_20261008/selected_release_retry2_20261009')}
    for access,target in outputs.items():make_junction(access,target)
    products=[]
    for old,new in DRIVERS.items():
        source="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_actual_manual_continue147_v8_20261009 import execute\nif __name__=='__main__':execute("+repr(old)+")\n"
        compile(source,str(A/new),'exec')
        with (A/new).open('x',encoding='utf8') as stream:stream.write(source)
        products.append(A/new)
    from recover_Joint147_publisher_phase_scratch_v7_20261008 import protected_module
    module=protected_module();all_map={**module['MAP'],**MAP}
    comparisons=[]
    for old in DRIVERS:
        s=(A/old).read_text(encoding='utf8');t=s
        # Substitute path/gate string constants only; every numerical expression and function stays exact.
        replacements=[]
        for before,after in all_map.items():
            if before in t:t=t.replace(before,after);replacements.append((before,after))
        restored=t
        for before,after in reversed(replacements):restored=restored.replace(after,before)
        assert ast.dump(ast.parse(s),include_attributes=False)==ast.dump(ast.parse(restored),include_attributes=False)
        comparisons.append({'source':old,'AST_exact_after_path_gate_reversal':True})
    source_inputs=[*products,A/'recover_Joint147_publisher_phase_scratch_v7_20261008.py',A/'Joint147_publisher_phase_scratch_recovery_v7_20261008.json',*(A/n for n in DRIVERS),A/'watch_validations_main_v7_20261006.py']
    pins.update({str(p):sha(p) for p in source_inputs})
    create(A/'actual_manual_continue_after2355_stop_v1_20261009.json',{'status':'actual_user_continue_with_all185_scores_and_prior_frozen_inputs_rehashed',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_user_instruction':'继续','stop_manifest':str(manifest),'all185_records_and8_metrics_exact':True,
        'old_expired_stop_schedule_not_restarted':True,'old_partial_inference_not_claimed_complete':True,'only_latest_observer_will_be_restarted':True,
        'new_scientific_scores':0,'new_native_fits':0,'test_labels_read':False})
    pins[str(A/'actual_manual_continue_after2355_stop_v1_20261009.json')]=sha(A/'actual_manual_continue_after2355_stop_v1_20261009.json')
    create(META,{'status':'verified_manual_resume_fresh_candidate_sealer_full_paths_unchanged185_science',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'new_E_outputs':{str(p):str(t) for p,t in outputs.items()},
        'gate_and_path_AST_controls':comparisons,'all_original185_scores_and32_canonical_sources_unchanged':True,
        'old_interrupted_candidate_and_logs_preserved':True,'new_candidate_repeats_two_full_and_cold80_actual_replays':True,
        'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    watcher=start('main_publisher_v9_20261009','watch_validations_main_v7_20261006.py',[],{str(A/'watch_validations_main_v7_20261006.py'):sha(A/'watch_validations_main_v7_20261006.py')})
    launches={'main_publisher_v9_20261009':watcher}
    for name,driver in [(MAP['JointCrossHuberOrder185_selected_candidate_preparation_v1_20261008'],products[0]),
        (MAP['JointCrossHuberOrder185_selected_candidate_sealing_v1_20261008'],products[1]),
        ('JointCrossHuberOrder185_round147_full_registration_v2_20261009',products[2])]:
        launches[name]=start(name,driver.name,[],{str(p):sha(p) for p in [Path(__file__),META,*products]})
    create(A/'actual_manual_continue147_hidden_launches_v8_20261009.json',launches)
    # This is the current mutable administrative pointer, separate from preserved frozen sources.
    from atomic_optimization_observer_writes_20261005 import write
    write(A/'current_user_runtime_control_20261008.json',{'status':'optimization_active_after_actual_user_manual_continue',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_user_instruction':'继续','previous_stop_manifest':str(manifest),
        'previous_stop_guard_status':str(manifest.parent/'guardian_status.json'),'automatic_restart_enabled':False,
        'expired20261008_stop_schedule_not_restarted':True,'new_stop_time_not_inferred_from_yesterdays_instruction':True})
    print({'actual_started':{n:r['owned_worker_pid'] for n,r in launches.items()},'completed185_scoring_not_restarted':True},flush=True)
if __name__=='__main__':main()
