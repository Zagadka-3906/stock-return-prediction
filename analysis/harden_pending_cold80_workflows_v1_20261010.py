"""Correct only pending schema consumers; retain original science, source proofs and service history."""
from pathlib import Path
import sys,subprocess,json,time
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import inventory,verified_pair,exact
from shutdown_ready_stop_v2_20261007 import StableJournal
from handoff_ready_goss_full_execution_20261006 import start_service

def write_new(path,text):
    compile(text,str(path),'exec');assert not path.exists();path.write_text(text,encoding='utf8',newline='\n');return path

def main():
    assert not (A/'optimization_20261003_r156/full_registration_execution.json').exists(), 'Reaudit pending jobs if predecessor already completed'
    families=('BF16FlagAfter15222_','ReusedNN158')
    rows=[r for r in inventory(full=True) if r['name'].startswith(families)]
    assert len(rows)==16,(len(rows),[r['name'] for r in rows])
    # Seven157 and nine158 service tasks are all still waiting for prior complete qualification.
    for r in rows:
        pair=verified_pair(r['launch']);assert pair is not None and not pair[0].children()
    ledger=A/'pending_cold80_schema_hardening_v1_20261010';ledger.mkdir();archive=ledger/'original_service_records';archive.mkdir()
    replacements={};new_sources=[]
    for tag in ('BF16FlagAfter15222','ReusedNN158Quality23','ReusedNN159Quality19','ReusedNN160Quality19'):
        source=A/f'seal_{tag}_selected_candidate_v1_20261009.py'
        text=source.read_text(encoding='utf8');assert "actual22_day_prefix_model_controls" in text
        target=A/f'seal_{tag}_selected_candidate_cold80_v2_20261010.py'
        replacements[str(source)]=str(write_new(target,text.replace('actual22_day_prefix_model_controls','actual80_day_prefix_model_controls')));new_sources.append(target)
    for family in ('BF16FlagAfter15222','ReusedNN158Quality23'):
        source=A/f'publish_{family}_evidence_v1_20261009.py';text=source.read_text(encoding='utf8')
        text=text.replace("with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'):",
            "with serial(log/'serial_mutex.json') as mutex,safe(log),git_io(log/'file_backed_git'):\n        mutex.acquire()")
        text=text.replace("('safe_'+phase+'_main_v1')","('safe_'+phase+'_main_v2')")
        target=A/f'publish_{family}_evidence_v2_20261010.py';replacements[str(source)]=str(write_new(target,text));new_sources.append(target)
    for number,quality,stage in ((157,'BF16FlagAfter15222','BF16FlagAfter152157'),(158,'ReusedNN158Quality23','ReusedNN158Stage')):
        source=A/f'run_{quality}_round{number}_full_registration_v1_20261009.py';text=source.read_text(encoding='utf8')
        old=f'{quality}_round{number}_actual_registration_v1_20261009';assert old in text
        target=A/f'run_{quality}_round{number}_full_registration_v2_20261010.py'
        write_new(target,text.replace(old,f'{quality}_round{number}_actual_registration_v2_20261010'));new_sources.append(target)
        safe_source=A/f'run_{stage}_safe_registration_v1_20261010.py';text=safe_source.read_text(encoding='utf8')
        text=text.replace(f'run_{quality}_round{number}_full_registration_v1_20261009',target.stem).replace('safe_full_main_v1','safe_full_main_v2')
        # Include the actually executed corrected source operators in the full registry's frozen scope.
        needle='def main():\n';assert text.count(needle)==1
        extra=f"    import prepare_{quality}_round{number}_sources_v1_20261009 as generator\n    original_sources=generator.source_paths\n    generator.source_paths=lambda:list(dict.fromkeys([*original_sources(),A/'pending_cold80_schema_hardening_v1_20261010/manifest.json',*map(Path,__import__('run_dependency_queue_v3_20261006').read(A/'pending_cold80_schema_hardening_v1_20261010/manifest.json')['corrected_source_sha256'])]))\n"
        text=text.replace(needle,needle+extra)
        safe_target=A/f'run_{stage}_safe_registration_v2_20261010.py';replacements[str(safe_source)]=str(write_new(safe_target,text));new_sources.append(safe_target)
    aliases=read(A/'manual_resume_service_aliases_v2_20261010.json')
    mapping={r['name']:r['name']+'_cold80_schema_v2_20261010' for r in rows}
    alias_path=A/'manual_resume_service_aliases_v4_20261010.json'
    create(alias_path,{**aliases,'service_aliases':{**aliases['service_aliases'],**mapping}})
    definitions={r['name']:read(Path(r['launch']['script_args'][0])) for r in rows}
    manifest={'status':'pending_schema_consumer_correction_before_any157_or158_quality_or_future_X',
        'corrected_source_sha256':{str(p):sha(p) for p in new_sources},'driver_replacements':replacements,
        'source_aliases':mapping,'actual_cold_prefix_days':80,'actual_prefix_rows':372000,
        'original_predictor_80_day_reports_unchanged':True,'new_native_fits':0,'new_quality_scores':0}
    create(ledger/'manifest.json',manifest)
    controller=next(r for r in inventory(full=True) if r['name']=='continuous_fast_reused_frontiers_v2_20261010')
    journal=StableJournal(ledger)
    for r in [controller,*rows]:journal.suspend_pair(r)
    for e in journal.data['entries']:
        if e['phase'] in ('pending','suspended'):
            p=exact(e['identity'])
            if p:p.terminate();p.wait(timeout=5)
            e['phase']='idle_schema_workflow_superseded_before_scientific_execution';journal.flush()
    # Archive only verified service metadata directories, within the workspace, in one native shell.
    quote=lambda p:"'"+str(p).replace("'","''")+"'"
    for r in rows:
        source=A/'service_owned_workflows_20261006'/r['name'];destination=archive/r['name']
        assert source.resolve().is_relative_to(A.resolve()) and destination.resolve().is_relative_to(archive.resolve())
        assert not destination.exists() and source.resolve()==source.absolute()
        result=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',
            'Move-Item -LiteralPath '+quote(source)+' -Destination '+quote(destination)],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,result.stderr
    wrapper=A/'manual_resume_service_alias_runtime_v3_20261010.py';launched={}
    for old,new in mapping.items():
        definition=definitions[old];args=list(definition['arguments'])
        index=args.index('--driver')+1;args[index]=replacements.get(args[index],args[index]);args[args.index('--aliases')+1]=str(alias_path)
        driver=Path(args[index]);pins={str(wrapper):sha(wrapper),str(driver):sha(driver),str(alias_path):sha(alias_path),str(ledger/'manifest.json'):sha(ledger/'manifest.json')}
        launched[old]=start_service(new,wrapper.name,args,pins)
        logical=A/'service_owned_workflows_20261006'/old;target=logical.parent/new
        result=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',
            'New-Item -ItemType Junction -Path '+quote(logical)+' -Target '+quote(target)+' | Out-Null'],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,result.stderr
    # The old logical service paths now resolve to fresh evidence; historical metadata stays in archive.
    source=A/'build_reused_neural_frontier_v2_20261010.py';text=source.read_text(encoding='utf8')
    needle="        compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\\n');created.append(target)"
    text=text.replace(needle,"        if name.startswith('seal_'):text=text.replace('actual22_day_prefix_model_controls','actual80_day_prefix_model_controls')\n"+needle)
    builder=write_new(A/'build_reused_neural_frontier_v3_20261010.py',text)
    source=A/'run_continuous_fast_reused_frontiers_v2_20261010.py';text=source.read_text(encoding='utf8').replace('build_reused_neural_frontier_v2_20261010','build_reused_neural_frontier_v3_20261010')
    text=text.replace("OUT=A/'continuous_fast_reused_frontiers_v2_20261010'","OUT=A/'continuous_fast_reused_frontiers_v3_20261010'")
    # Derived159/160 were preflighted before this schema correction; select their corrected sealer operator.
    needle="        path=A/driver;assert path.is_file()"
    text=text.replace(needle,needle+"\n        if driver.startswith('seal_'):\n            corrected=A/driver.replace('_selected_candidate_v1_20261009.py','_selected_candidate_cold80_v2_20261010.py')\n            if corrected.is_file():path=corrected")
    cont=write_new(A/'run_continuous_fast_reused_frontiers_v3_20261010.py',text)
    new_controller=start_service('continuous_fast_reused_frontiers_v3_20261010',cont.name,[],{str(cont):sha(cont),str(builder):sha(builder)})
    create(ledger/'verification.json',{'status':'passed_idle_only16_workflow_recovery_with_original_records_and_cold80_schema',
        'launches':launched,'controller':new_controller,'original_service_archives':str(archive),
        'already_completed156_training_or_scoring_stopped':0,'future_X_not_read_for_new157_or158':True})
    print({'schema_corrected_pending_jobs':len(rows),'controller':new_controller['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
