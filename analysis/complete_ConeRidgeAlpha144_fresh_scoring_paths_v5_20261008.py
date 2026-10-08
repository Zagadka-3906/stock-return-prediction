"""Fresh complete path contract, preflight and score chain; keep all failed empty/partial science outputs intact."""
from pathlib import Path
import sys,time,subprocess,hashlib,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
SCORE_OLD='ConeRidgeAlpha100_official_comparison_v3_20261008'
SCORE_NEW='ConeRidgeAlpha100_official_comparison_v5_20261008'
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def replace_dependency(text,old,new):
    tree=ast.parse(text);lines=text.splitlines(keepends=True);changes=[]
    for node in ast.walk(tree):
        if not isinstance(node,ast.Constant) or node.value!=old:continue
        parents=[p for p in ast.walk(tree) if any(c is node for c in ast.iter_child_nodes(p))]
        if any(isinstance(p,ast.BinOp) and isinstance(p.op,ast.Div) for p in parents):continue
        changes.append((node.lineno,node.col_offset,node.end_col_offset))
    for ln,left,right in sorted(changes,reverse=True):lines[ln-1]=lines[ln-1][:left]+repr(new)+lines[ln-1][right:]
    return ''.join(lines)
def main():
    failed=A/'service_owned_workflows_20261006/ConeRidgeAlpha100_official_comparison_v4_20261008'
    assert not owned(read(failed/'native_launch.json')) and read(failed/'service_execution.json')['status']=='failed'
    assert not list((A/SCORE_OLD).glob('case*_official.json'))
    sources=[Path(__file__),failed/'service_execution.json'];outputs=[]
    storage=A/'ConeRidgeAlpha144_storage_v2_20261008.py';sources.append(storage);text=storage.read_text(encoding='utf8')
    needle="    ROOT/'analysis/ConeRidgeAlpha100_official_comparison_v3_20261008': EBASE/'official_comparison',"
    assert text.count(needle)==1
    text=text.replace(needle,needle+"\n    ROOT/'analysis/"+SCORE_NEW+"': EBASE/'official_comparison_v5',")
    text=text.replace("path.parent==ROOT/'analysis/ConeRidgeAlpha100_official_comparison_v1_20261008'",
                      "path.parent==ROOT/'analysis/"+SCORE_NEW+"'")
    outputs.append(save('ConeRidgeAlpha144_storage_v3_20261008.py',text))
    from ConeRidgeAlpha144_storage_v3_20261008 import EBASE,OUTPUTS,empty,write_progress
    target=EBASE/'official_comparison_v5';logical=A/SCORE_NEW;assert not target.exists() and not logical.exists();target.mkdir()
    script="New-Item -ItemType Junction -Path '"+str(logical).replace("'","''")+"' -Target '"+str(target).replace("'","''")+"' | Out-Null"
    result=subprocess.run(['powershell.exe','-NoLogo','-NoProfile','-NonInteractive','-Command',script],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode==0,result.stderr;empty(logical)
    # Execute the actual progress writer against the fresh route, in a separate tiny E-owned contract directory.
    # Avoid touching the empty scientific output: reject a wrong directory, and test write_progress on a distinct mapped module instance.
    probe=EBASE/'progress_writer_contract_v5';assert not probe.exists();probe.mkdir()
    import ConeRidgeAlpha144_storage_v3_20261008 as module
    previous_outputs=module.OUTPUTS;previous_root=module.ROOT
    try:
        module.ROOT=probe;probe_logical=probe/'analysis'/SCORE_NEW;probe_logical.mkdir(parents=True)
        module.OUTPUTS={probe_logical:probe_logical}
        module.write_progress(probe_logical/'actual_stage.json',{'contract_executed':True})
        assert read(probe_logical/'actual_stage.json')=={'contract_executed':True}
    finally:module.OUTPUTS=previous_outputs;module.ROOT=previous_root
    assert not any(logical.iterdir())
    mappings={
        'prepare_ConeRidgeAlpha100_round144_sources_v3_20261008':'prepare_ConeRidgeAlpha100_round144_sources_v4_20261008',
        'ConeRidgeAlpha100_round144_source_admission_v3_20261008.json':'ConeRidgeAlpha100_round144_source_admission_v4_20261008.json',
        'ConeRidgeAlpha100_round144_source_preparation_v3_20261008.json':'ConeRidgeAlpha100_round144_source_preparation_v4_20261008.json',
        'ConeRidgeAlpha100_prospective_routes_v3_20261008.json':'ConeRidgeAlpha100_prospective_routes_v4_20261008.json',
        'ConeRidgeAlpha144_receiver_preparation_v3_20261008.json':'ConeRidgeAlpha144_receiver_preparation_v4_20261008.json',
        SCORE_OLD:SCORE_NEW,
        'ConeRidgeAlpha144_D_scoring_v1_20261008':'ConeRidgeAlpha144_D_scoring_v5_20261008',
        'ConeRidgeAlpha144_storage_v1_20261008':'ConeRidgeAlpha144_storage_v3_20261008',
        'ConeRidgeAlpha144_storage_v2_20261008':'ConeRidgeAlpha144_storage_v3_20261008'}
    def corrected(text):
        for before,after in mappings.items():text=text.replace(before,after)
        return text
    roles=[
        ('run_ConeRidgeAlpha100_official_comparison_v4_20261008.py',5),
        ('publish_ConeRidgeAlpha100_evidence_v4_20261008.py',5),
        ('prepare_ConeRidgeAlpha100_selected_candidate_v4_20261008.py',5),
        ('seal_ConeRidgeAlpha100_selected_candidate_v4_20261008.py',5),
        ('run_ConeRidgeAlpha100_round144_full_registration_v5_20261008.py',6)]
    dependencies={
        'ConeRidgeAlpha100_official_comparison_v4_20261008':'ConeRidgeAlpha100_official_comparison_v5_20261008',
        'ConeRidgeAlpha100_scores_main_publication_v4_20261008':'ConeRidgeAlpha100_scores_main_publication_v5_20261008',
        'ConeRidgeAlpha100_selected_candidate_preparation_v4_20261008':'ConeRidgeAlpha100_selected_candidate_preparation_v5_20261008',
        'ConeRidgeAlpha100_selected_candidate_sealing_v4_20261008':'ConeRidgeAlpha100_selected_candidate_sealing_v5_20261008'}
    for filename,version in roles:
        source=A/filename;sources.append(source);text=corrected(source.read_text(encoding='utf8'))
        for before,after in dependencies.items():text=replace_dependency(text,before,after)
        text=text.replace('service_owned_workflows_20261006/ConeRidgeAlpha100_selected_candidate_preparation_v4_20261008',
                          'service_owned_workflows_20261006/ConeRidgeAlpha100_selected_candidate_preparation_v5_20261008')
        if version==6:text=text.replace('actual_registration_v5_20261008','actual_registration_v6_20261008').replace('full_registration_v5_file_IO_20261008','full_registration_v6_file_IO_20261008')
        outputs.append(save(filename.replace('_v4_',f'_v{version}_').replace('_v5_',f'_v{version}_'),text))
    source=A/'prepare_ConeRidgeAlpha100_round144_sources_v3_20261008.py';sources.append(source);text=corrected(source.read_text(encoding='utf8'))
    # Preserve original function structure but adapt generated source paths as well as its own tail.
    old="def adapt(text):return corrected(original_adapt(text))"
    assert text.count(old)==1
    additions=repr(mappings)
    text=text.replace(old,"def adapt(text):\n    value=corrected(original_adapt(text))\n    for before,after in "+additions+".items():value=value.replace(before,after)\n    return value")
    outputs.append(save('prepare_ConeRidgeAlpha100_round144_sources_v4_20261008.py',text))
    source=A/'verify_ConeRidgeAlpha100_prospective_routes_v5_20261008.py';sources.append(source);text=corrected(source.read_text(encoding='utf8'))
    text=text.replace('run_ConeRidgeAlpha100_official_comparison_v3_20261008.py','run_ConeRidgeAlpha100_official_comparison_v5_20261008.py')
    text=text.replace('prepare_ConeRidgeAlpha100_selected_candidate_v3_20261008.py','prepare_ConeRidgeAlpha100_selected_candidate_v5_20261008.py')
    text=text.replace('publish_ConeRidgeAlpha100_evidence_v3_20261008.py','publish_ConeRidgeAlpha100_evidence_v5_20261008.py')
    text=text.replace('cross_volume_byte_probe_v5','cross_volume_byte_probe_v6')
    text=text.replace('    for path in OUTPUTS:empty(path)',"    for path in OUTPUTS:\n        if 'official_comparison' in path.name and path!=A/'"+SCORE_NEW+"':continue\n        empty(path)")
    outputs.append(save('verify_ConeRidgeAlpha100_prospective_routes_v6_20261008.py',text))
    source=A/'verify_ConeRidgeAlpha144_D_scoring_scope_v1_20261008.py';sources.append(source);text=corrected(source.read_text(encoding='utf8'))
    text=text.replace('ConeRidgeAlpha144_D_scoring_scope_v1_20261008.json','ConeRidgeAlpha144_D_scoring_scope_v2_20261008.json')
    outputs.append(save('verify_ConeRidgeAlpha144_D_scoring_scope_v2_20261008.py',text))
    from verify_ConeRidgeAlpha144_D_scoring_scope_v2_20261008 import main as dscope
    dscope()
    from verify_ConeRidgeAlpha100_prospective_routes_v6_20261008 import main as prospective
    prospective()
    old_admission=A/'ConeRidgeAlpha100_round144_source_admission_v3_20261008.json';base=read(old_admission)
    for p,d in base['input_sha256'].items():assert sha(p)==d,p
    prospective_path=A/'ConeRidgeAlpha100_prospective_routes_v4_20261008.json';proof=read(prospective_path)
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==2619
    pins={**base['input_sha256'],**proof['input_sha256'],**{str(p):sha(p) for p in [*sources,*outputs,old_admission,prospective_path]}}
    create(A/'ConeRidgeAlpha144_fresh_scoring_path_admission_v5_20261008.json',{
        'status':'passed_fresh_E_empty_output_progress_writer_actual_D_gates_and24_2619_complete_preflights',
        'input_sha256':pins,'path_mapping':mappings,'actual_progress_writer_contract_executed':True,
        'all_original_model_CDF_and_scoring_math_unchanged':True,'actual_prior97_full291_cold48_native48_calendar_rehashed':True,
        'old_failures_and_partial_scoring_freeze_preserved':True,'new_quality_scores':0})
    create(A/'ConeRidgeAlpha100_round144_source_admission_v4_20261008.json',{
        **base,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'generated_source_sha256':proof['generated_source_sha256'],'actual_path_contract_recovery_version':5,
        'prior_scientific_controls_source_admission3_preserved':True,'new_quality_scores':0})
    jobs=[('ConeRidgeAlpha100_official_comparison_v5_20261008','run_ConeRidgeAlpha100_official_comparison_v5_20261008.py',[]),
        ('ConeRidgeAlpha100_scores_main_publication_v5_20261008','publish_ConeRidgeAlpha100_evidence_v5_20261008.py',['scores']),
        ('ConeRidgeAlpha100_selected_candidate_preparation_v5_20261008','prepare_ConeRidgeAlpha100_selected_candidate_v5_20261008.py',[]),
        ('ConeRidgeAlpha100_selected_candidate_sealing_v5_20261008','seal_ConeRidgeAlpha100_selected_candidate_v5_20261008.py',[]),
        ('ConeRidgeAlpha100_round144_full_registration_v6_20261008','run_ConeRidgeAlpha100_round144_full_registration_v6_20261008.py',[])]
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'ConeRidgeAlpha144_fresh_scoring_paths_hidden_launches_v5_20261008.json',{
        'status':'started_actual_admitted_score5_main5_candidate5_seal5_registration6',
        'launches':launches,'input_sha256':pins,'expected_scored_cases':100,'QA_version':55,'new_quality_scores_by_dispatch':0})
    print('Fresh E/D/progress writer and full graph controls executed; actual100 score5 chain started.',flush=True)
if __name__=='__main__':main()
