"""Declare the actual module-routed comparison output alias on E; unchanged100 score mathematics, fresh dependent receivers."""
from pathlib import Path
import sys,time,subprocess,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    failed=A/'service_owned_workflows_20261006/ConeRidgeAlpha100_official_comparison_v3_20261008'
    assert not owned(read(failed/'native_launch.json')) and read(failed/'service_execution.json')['status']=='failed'
    from ConeRidgeAlpha144_storage_v1_20261008 import EBASE
    logical=A/'ConeRidgeAlpha100_official_comparison_v3_20261008';target=EBASE/'official_comparison'
    assert not logical.exists() and target.is_dir() and not any(target.iterdir())
    # Only a fresh alias to the existing admitted empty E output. No moves/deletions/overwrites.
    script="New-Item -ItemType Junction -Path '"+str(logical).replace("'","''")+"' -Target '"+str(target).replace("'","''")+"' | Out-Null"
    result=subprocess.run(['powershell.exe','-NoLogo','-NoProfile','-NonInteractive','-Command',script],capture_output=True,
        creationflags=subprocess.CREATE_NO_WINDOW);assert result.returncode==0,result.stderr
    assert logical.resolve()==target.resolve() and not any(logical.iterdir())
    storage=A/'ConeRidgeAlpha144_storage_v1_20261008.py';text=storage.read_text(encoding='utf8')
    needle="    ROOT/'analysis/ConeRidgeAlpha100_official_comparison_v1_20261008': EBASE/'official_comparison',"
    assert text.count(needle)==1
    text=text.replace(needle,needle+"\n    ROOT/'analysis/ConeRidgeAlpha100_official_comparison_v3_20261008': EBASE/'official_comparison',")
    outputs=[save('ConeRidgeAlpha144_storage_v2_20261008.py',text)]
    scorer=A/'run_ConeRidgeAlpha100_official_comparison_v3_20261008.py';original=scorer.read_text(encoding='utf8')
    score4=original.replace('from ConeRidgeAlpha144_storage_v1_20261008 import','from ConeRidgeAlpha144_storage_v2_20261008 import')
    assert score4.replace('from ConeRidgeAlpha144_storage_v2_20261008 import','from ConeRidgeAlpha144_storage_v1_20261008 import')==original
    outputs.append(save('run_ConeRidgeAlpha100_official_comparison_v4_20261008.py',score4))
    replacements={
        'ConeRidgeAlpha100_official_comparison_v3_20261008':'ConeRidgeAlpha100_official_comparison_v4_20261008',
        'ConeRidgeAlpha100_scores_main_publication_v3_20261008':'ConeRidgeAlpha100_scores_main_publication_v4_20261008',
        'ConeRidgeAlpha100_selected_candidate_preparation_v3_20261008':'ConeRidgeAlpha100_selected_candidate_preparation_v4_20261008',
        'ConeRidgeAlpha100_selected_candidate_sealing_v3_20261008':'ConeRidgeAlpha100_selected_candidate_sealing_v4_20261008'}
    sources=[Path(__file__),storage,scorer,failed/'service_execution.json']
    jobs=[('ConeRidgeAlpha100_official_comparison_v4_20261008',outputs[-1].name,[])]
    for source_name,version,service,args in (
        ('publish_ConeRidgeAlpha100_evidence_v3_20261008.py',4,'ConeRidgeAlpha100_scores_main_publication_v4_20261008',['scores']),
        ('prepare_ConeRidgeAlpha100_selected_candidate_v3_20261008.py',4,'ConeRidgeAlpha100_selected_candidate_preparation_v4_20261008',[]),
        ('seal_ConeRidgeAlpha100_selected_candidate_v3_20261008.py',4,'ConeRidgeAlpha100_selected_candidate_sealing_v4_20261008',[]),
        ('run_ConeRidgeAlpha100_round144_full_registration_v4_20261008.py',5,'ConeRidgeAlpha100_round144_full_registration_v5_20261008',[])):
        source=A/source_name;sources.append(source);text=source.read_text(encoding='utf8')
        # Change only service dependency string arguments; actual scientific output paths stay on alias v3.
        tree=ast.parse(text)
        edits=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value in replacements:
                # A literal naming the output is part of an A/path expression, not a closed-service argument.
                parents=[p for p in ast.walk(tree) if any(c is node for c in ast.iter_child_nodes(p))]
                if any(isinstance(p,ast.BinOp) and isinstance(p.op,ast.Div) for p in parents):continue
                edits.append((node.lineno,node.col_offset,node.end_lineno,node.end_col_offset,replacements[node.value]))
        lines=text.splitlines(keepends=True)
        for ln,col,endln,endcol,value in sorted(edits,reverse=True):
            assert ln==endln;lines[ln-1]=lines[ln-1][:col]+repr(value)+lines[ln-1][endcol:]
        text=''.join(lines)
        # Sealer directly constructs its preparation service path as a composite literal.
        text=text.replace('service_owned_workflows_20261006/ConeRidgeAlpha100_selected_candidate_preparation_v3_20261008',
                          'service_owned_workflows_20261006/ConeRidgeAlpha100_selected_candidate_preparation_v4_20261008')
        if version==5:
            text=text.replace('actual_registration_v4_20261008','actual_registration_v5_20261008').replace('full_registration_v4_file_IO_20261008','full_registration_v5_file_IO_20261008')
        name=source_name.replace('_v3_',f'_v{version}_').replace('_v4_',f'_v{version}_')
        output=save(name,text);outputs.append(output);jobs.append((service,output.name,args))
    pins={str(p):sha(p) for p in [*sources,*outputs]}
    create(A/'ConeRidgeAlpha144_comparison_output_alias_recovery_v4_20261008.json',{
        'status':'passed_actual_empty_E_output_alias_and_exact_score_import_only_recipe4',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'logical':str(logical),'physical_E':str(target),'all100_math_and_cases_and_native_models_unchanged':True,
        'original_failure3_preserved':'empty_output_admission_KeyError_before_any_quality',
        'original_24_sources_2619_graphs_and_source_admission3_preserved':True,'new_quality_scores':0})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'ConeRidgeAlpha144_comparison_output_alias_hidden_launches_v4_20261008.json',{
        'status':'started_score4_scores_main4_candidate4_seal4_and_full_registration5',
        'launches':launches,'input_sha256':pins,'expected_records':100,'QA_version':55,'new_quality_scores_by_dispatch':0})
    print('Actual admitted E comparison alias; exact100 scoring4 and dependent candidate/main chain dispatched.',flush=True)
if __name__=='__main__':main()
