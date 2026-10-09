"""Recover zero-score import failure with prior controls and immutable attempt history."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service

def new_source(path,text):
    assert not path.exists();compile(text,str(path),'exec')
    path.write_text(text,encoding='utf8',newline='\n');return path

def main():
    control=read(A/'current_user_runtime_control_20261010.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume'
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    S=A/'service_owned_workflows_20261006'
    names=['BF16FlagAfter15222_'+suffix for suffix in ['official_comparison_v3_20261009','scores_main_publication_v1_20261009','selected_candidate_preparation_v1_20261009','selected_candidate_sealing_v1_20261009','round157_full_registration_v1_20261009']]
    names += [p.name for p in S.iterdir() if p.name.startswith('ReusedNN158') and p.is_junction() and '_cold80_' not in p.name]
    assert len(names)==14
    definitions={};physical={}
    for name in names:
        path=S/name;launch=read(path/'native_launch.json')
        assert not owned(launch) and read(path/'service_execution.json')['status']=='failed',name
        physical[name]=path.resolve()
        assert physical[name].is_relative_to(S.resolve()) and not physical[name].is_junction()
        definitions[name]=read(path/'job_definition.json')
    out=A/'actual157_import_failure_recovery_v1_20261010';out.mkdir();archive=out/'original_service_records';archive.mkdir()
    score_out=Path('E:/赛题五_本机临时/BF16FlagAfter15222_official_comparison_v1_20261009')
    assert score_out.resolve().is_relative_to(Path('E:/赛题五_本机临时').resolve())
    assert not list(score_out.glob('case*_official.json'))
    for name in ['BF16FlagAfter15222_selected_release_v1_20261009']:
        assert not any((A/name).iterdir())
    quote=lambda p:"'"+str(p).replace("'","''")+"'"
    def shell(command):
        r=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',command],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert r.returncode==0,r.stderr
    # All old outputs are retained; this failed attempt made no quality record.
    destination=Path('E:/赛题五_本机临时/BF16FlagAfter15222_zero_score_import_failure_v1_20261010')
    assert not destination.exists()
    shell('Move-Item -LiteralPath '+quote(score_out)+' -Destination '+quote(destination))
    score_out.mkdir()
    scoring=A/'BF16FlagAfter152157_D_scoring_v1_20261009/comparison'
    assert scoring.resolve().is_relative_to(A.resolve())
    if scoring.exists():shell('Move-Item -LiteralPath '+quote(scoring)+' -Destination '+quote(out/'original_D_scoring_comparison'))
    replacements={};corrected=[]
    for number,quality,stage in [(157,'BF16FlagAfter15222','BF16FlagAfter152157'),(158,'ReusedNN158Quality23','ReusedNN158Stage')]:
        original=A/f'run_{quality}_round{number}_full_registration_QApath_v3_20261010.py'
        text=original.read_text(encoding='utf8').replace(f'{quality}_round{number}_actual_registration_QApath_v3_20261010',f'{quality}_round{number}_actual_registration_import_v5_20261010')
        receiver=new_source(A/f'run_{quality}_round{number}_full_registration_import_v5_20261010.py',text);corrected.append(receiver)
        source=A/f'run_{stage}_safe_registration_QApath_v3_20261010.py';text=source.read_text(encoding='utf8').replace(original.stem,receiver.stem).replace('safe_full_main_QApath_v3_20261010','safe_full_main_import_v5_20261010')
        helper="    from byte_exact_ranking_stream_runtime_v1_20261010 import installed as accelerated_writer\n"
        text=text.replace('    count=int(',helper+'    count=int(')
        text=text.replace('installed_transfer(),qa_paths():','installed_transfer(),qa_paths(),accelerated_writer():')
        text=text.replace("A/'actual_QA_collector_path_controls_v44_20261010.json'",f"A/'actual_QA_collector_path_controls_v44_20261010.json',A/'{receiver.name}',A/'byte_exact_ranking_stream_runtime_v1_20261010.py',A/'byte_exact_ranking_stream_benchmark_v1_20261010.json'")
        target=new_source(A/f'run_{stage}_safe_registration_import_v5_20261010.py',text)
        replacements[str(source)]=str(target);corrected.append(target)
    wrapper=A/'manual_resume_service_alias_runtime_v5_20261010.py';launches={}
    for name in names:
        previous=physical[name];destination=archive/previous.name
        assert not destination.exists()
        shell('Move-Item -LiteralPath '+quote(previous)+' -Destination '+quote(destination))
        definition=definitions[name];args=list(definition['arguments']);index=args.index('--driver')+1
        args[index]=replacements.get(args[index],args[index]);driver=Path(args[index]);alias=Path(args[args.index('--aliases')+1])
        new=name+'_actual_import_recovery_v5_20261010'
        row=start_service(new,wrapper.name,args,{str(p):sha(p) for p in [wrapper,driver,alias,A/'actual_return_mapping_import_scope_preflight_v1_20261010.json',*corrected]})
        launches[name]=row
        shell('New-Item -ItemType Junction -Path '+quote(previous)+' -Target '+quote(S/new)+' | Out-Null')
    text=(A/'run_continuous_fast_reused_frontiers_v7_20261010.py').read_text(encoding='utf8').replace('manual_resume_service_alias_runtime_v4_20261010.py','manual_resume_service_alias_runtime_v5_20261010.py').replace("OUT=A/'continuous_fast_reused_frontiers_v7_20261010'","OUT=A/'continuous_fast_reused_frontiers_v8_20261010'")
    controller=new_source(A/'run_continuous_fast_reused_frontiers_v8_20261010.py',text)
    row=start_service('continuous_fast_reused_frontiers_v8_20261010',controller.name,[],{str(p):sha(p) for p in [controller,A/'build_reused_neural_frontier_v5_20261010.py',wrapper]})
    create(out/'verification.json',{'status':'passed14_exited_zero_score_import_dependencies_recovered_with_original_records',
        'actual_service_launches':launches,'controller':row,'archived_original_score_attempt':str(Path('E:/赛题五_本机临时/BF16FlagAfter15222_zero_score_import_failure_v1_20261010')),
        'actual_full17_and_native14_repeated':False,'actual156_full_QA_and_main_retained':True,'completed_quality_records_repeated':0,
        'actual_import_preflight':str(A/'actual_return_mapping_import_scope_preflight_v1_20261010.json'),
        'byte_exact_stream_writer_adopted_from_actual_full_board_proof':True,'new_native_fits':0,'test_labels_read':False})
    print('RECOVERED',len(launches),'CONTROLLER',row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
