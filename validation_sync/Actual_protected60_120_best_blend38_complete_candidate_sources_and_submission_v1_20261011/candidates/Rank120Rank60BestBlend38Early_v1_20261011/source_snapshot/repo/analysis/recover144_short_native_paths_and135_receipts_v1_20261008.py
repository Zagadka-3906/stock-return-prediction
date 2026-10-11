"""Fresh outputs and preflight for storage-only repair; preserve both failed candidate and registration files."""
from pathlib import Path
import sys,subprocess,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def save(name,value):
    p=A/name;assert not p.exists(),p;compile(value,str(p),'exec');p.write_text(value,encoding='utf8',newline='\n');return p
def main():
    assert read(A/'service_owned_workflows_20261006/ConeRidgeAlpha100_selected_candidate_preparation_v6_20261008/service_execution.json')['status']=='failed'
    out=[]
    old=A/'ConeRidgeAlpha144_storage_v3_20261008.py';value=old.read_text(encoding='utf8');needle="OUTPUTS = {";value=value.replace(needle,needle+"\n    ROOT/'candidates/ConeRidgeAlpha100_v2_20261008': EBASE/'candidate_v2',\n    ROOT/'analysis/ConeRidgeAlpha100_selected_release_v2_20261008': EBASE/'selected_release_v2',")
    out.append(save('ConeRidgeAlpha144_storage_v4_20261008.py',value))
    from ConeRidgeAlpha144_storage_v4_20261008 import OUTPUTS,empty
    for logical,target in OUTPUTS.items():
        if logical.name not in ('ConeRidgeAlpha100_v2_20261008','ConeRidgeAlpha100_selected_release_v2_20261008'):continue
        assert not logical.exists() and not target.exists();target.mkdir()
        command="New-Item -ItemType Junction -Path '"+str(logical).replace("'","''")+"' -Target '"+str(target).replace("'","''")+"' | Out-Null"
        r=subprocess.run(['powershell.exe','-NoLogo','-NoProfile','-NonInteractive','-Command',command],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert r.returncode==0,r.stderr;empty(logical)
    def adapt(value):
        for before,after in [('ConeRidgeAlpha100_selected_release_v1_20261008','ConeRidgeAlpha100_selected_release_v2_20261008'),('ConeRidgeAlpha100_v1_20261008','ConeRidgeAlpha100_v2_20261008'),('ConeRidgeAlpha144_storage_v3_20261008','ConeRidgeAlpha144_storage_v4_20261008'),('prepare_ConeRidgeAlpha100_round144_sources_v4_20261008','prepare_ConeRidgeAlpha100_round144_sources_v5_20261008'),('ConeRidgeAlpha100_round144_source_admission_v4_20261008','ConeRidgeAlpha100_round144_source_admission_v5_20261008'),('ConeRidgeAlpha100_round144_source_preparation_v4_20261008','ConeRidgeAlpha100_round144_source_preparation_v5_20261008')]:value=value.replace(before,after)
        return value
    for role in ('prepare','seal'):
        source=A/f'{role}_ConeRidgeAlpha100_selected_candidate_v6_20261008.py';value=adapt(source.read_text(encoding='utf8')).replace('ConeRidgeAlpha100_selected_candidate_preparation_v6_20261008','ConeRidgeAlpha100_selected_candidate_preparation_v7_20261008')
        if role=='prepare':
            value=value.replace('pre_inference_source_freeze_v1','pre_inference_source_freeze_v2')
            needle="            prediction,storage=predict(ns,selection,CANDIDATE,parent_candidate/'cohort_curve.json',OUT/'future_return_mapping.json');output_scope.reverify()";assert value.count(needle)==1
            value=value.replace(needle,"            from short_content_addressed_native_storage_v1_20261008 import installed as short_storage\n            with short_storage() as storage_contract:\n                prediction,storage=predict(ns,selection,CANDIDATE,parent_candidate/'cohort_curve.json',OUT/'future_return_mapping.json')\n            create(OUT/'short_native_storage_execution.json',storage_contract)\n            output_scope.reverify()")
        out.append(save(f'{role}_ConeRidgeAlpha100_selected_candidate_v7_20261008.py',value))
    source=A/'prepare_ConeRidgeAlpha100_round144_sources_v4_20261008.py';value=source.read_text(encoding='utf8')
    # Preserve all old generation transforms, then map only the fresh selected-output and administrative source package routes.
    marker='ROOT=original.ROOT;A=original.A';assert value.count(marker)==1
    insert="\n_previous_adapt=adapt\ndef adapt(text):\n    value=_previous_adapt(text)\n    for before,after in "+repr({'ConeRidgeAlpha100_selected_release_v1_20261008':'ConeRidgeAlpha100_selected_release_v2_20261008','ConeRidgeAlpha100_v1_20261008':'ConeRidgeAlpha100_v2_20261008','ConeRidgeAlpha144_storage_v3_20261008':'ConeRidgeAlpha144_storage_v4_20261008','prepare_ConeRidgeAlpha100_round144_sources_v4_20261008':'prepare_ConeRidgeAlpha100_round144_sources_v5_20261008'})+".items():value=value.replace(before,after)\n    return value\n"
    value=value.replace(marker,insert+marker)
    value=value.replace('ConeRidgeAlpha100_round144_source_admission_v4_20261008','ConeRidgeAlpha100_round144_source_admission_v5_20261008').replace('ConeRidgeAlpha100_round144_source_preparation_v4_20261008','ConeRidgeAlpha100_round144_source_preparation_v5_20261008').replace('ConeRidgeAlpha100_selected_release_v1_20261008','ConeRidgeAlpha100_selected_release_v2_20261008').replace('ConeRidgeAlpha100_scores_github_v1_20261008/receipt.json','ConeRidgeAlpha100_scores_github_v2_20261008/receipt.json')
    out.append(save('prepare_ConeRidgeAlpha100_round144_sources_v5_20261008.py',value))
    source=A/'verify_ConeRidgeAlpha100_prospective_routes_v6_20261008.py';value=adapt(source.read_text(encoding='utf8'))
    first=value.index('    for path in OUTPUTS:');last=value.index('    original_graph=',first)
    value=value[:first]+"    for path in OUTPUTS:\n        if path.name in ('ConeRidgeAlpha100_v2_20261008','ConeRidgeAlpha100_selected_release_v2_20261008','optimization_20261003_r144','round144','lossless_ranking_display_qa_v55_20261007'):empty(path)\n"+value[last:]
    value=value.replace('ConeRidgeAlpha100_prospective_routes_v4_20261008.json','ConeRidgeAlpha100_prospective_routes_v5_20261008.json').replace('ConeRidgeAlpha144_receiver_preparation_v4_20261008.json','ConeRidgeAlpha144_receiver_preparation_v5_20261008.json').replace('cross_volume_byte_probe_v6','cross_volume_byte_probe_v7')
    # Actual score consumer is now connected-API receipt2; old native controls publisher remains receipt1.
    value=value.replace("('scores',A/'prepare_ConeRidgeAlpha100_selected_candidate_v5_20261008.py')","('scores',A/'prepare_ConeRidgeAlpha100_selected_candidate_v7_20261008.py')")
    old="        assert output==A/f'ConeRidgeAlpha100_{phase}_github_v1_20261008' and output.name+'/receipt.json' in consumer.read_text(encoding='utf8')"
    assert old in value;value=value.replace(old,"        assert output==A/f'ConeRidgeAlpha100_{phase}_github_v1_20261008'\n        expected=output.name if phase=='controls' else 'ConeRidgeAlpha100_scores_github_v2_20261008'\n        assert expected+'/receipt.json' in consumer.read_text(encoding='utf8')")
    out.append(save('verify_ConeRidgeAlpha100_prospective_routes_v7_20261008.py',value))
    from verify_ConeRidgeAlpha100_prospective_routes_v7_20261008 import main as preflight
    preflight()
    proof=read(A/'ConeRidgeAlpha100_prospective_routes_v5_20261008.json');assert proof['actual_graph_controls']==2619
    original=read(A/'ConeRidgeAlpha100_round144_source_admission_v4_20261008.json')
    for p,d in original['input_sha256'].items():assert sha(p)==d,p
    pins={**original['input_sha256'],**proof['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),*out,A/'short_content_addressed_native_storage_v1_20261008.py']}}
    create(A/'ConeRidgeAlpha100_round144_source_admission_v5_20261008.json',{**original,'input_sha256':pins,'generated_source_sha256':proof['generated_source_sha256'],'selected_output_storage_recovery_version':2,'native_filename_only_sha_content_addressing':True,'new_quality_scores':0})
    # Fresh135 registration: exact old generated receiver bytes already passed and were emitted before the missing-receipt failure.
    source=A/'run_BF16wide40_round135_full_registration_v6_20261008.py';value=source.read_text(encoding='utf8').replace('actual_registration_v6_20261008','actual_registration_v7_20261008').replace('full_registration_v6_file_IO_20261008','full_registration_v7_file_IO_20261008')
    needle='    prepare_sources()';assert value.count(needle)==1
    hook="    old_paths=actual_generator.source_paths\n    def correct_windows_receipt_paths():\n        paths=[A/'BF16wide40_scores_github_v3_20261008/receipt.json' if p.name=='receipt.json' and p.parent.name in ('BF16wide40_scores_github_v1_20261008','BF16wide40_scores_github_v2_20261008') else p for p in old_paths()]\n        return list(dict.fromkeys([*paths,Path(__file__),A/'recover144_short_native_paths_and135_receipts_v1_20261008.py']))\n    actual_generator.source_paths=correct_windows_receipt_paths\n    existing=A/'BF16wide40_round135_source_preparation_v4_20261008.json'\n    if existing.exists():\n        for p,d in read(existing)['input_sha256'].items():assert sha(p)==d,p\n    else:prepare_sources()"
    value=value.replace(needle,hook);out.append(save('run_BF16wide40_round135_full_registration_v7_20261008.py',value))
    # Prospective original-QA144 receiver is bound to fresh outputs and waits for135 publication before changing current board.
    source=A/'run_ConeRidgeAlpha100_round144_full_registration_v7_20261008.py';value=adapt(source.read_text(encoding='utf8')).replace('actual_registration_v7_20261008','actual_registration_v8_20261008').replace('full_registration_v7_file_IO_20261008','full_registration_v8_file_IO_20261008').replace('ConeRidgeAlpha100_selected_candidate_sealing_v6_20261008','ConeRidgeAlpha100_selected_candidate_sealing_v7_20261008').replace('BF16wide40_round135_full_registration_v6_20261008','BF16wide40_round135_full_registration_v7_20261008')
    value=value.replace("paths=[Path(str(p).replace(","paths=[Path(str(p).replace(")
    needle='    connected_generator.source_paths=actual_connected_source_paths';assert value.count(needle)==1
    value=value.replace(needle,needle+"\n    prior_windows_paths=connected_generator.source_paths\n    def actual_windows_paths():\n        return list(dict.fromkeys([A/'ConeRidgeAlpha100_scores_github_v2_20261008/receipt.json' if p.name=='receipt.json' and p.parent.name=='ConeRidgeAlpha100_scores_github_v1_20261008' else p for p in prior_windows_paths()]+[Path(__file__),A/'short_content_addressed_native_storage_v1_20261008.py',A/'recover144_short_native_paths_and135_receipts_v1_20261008.py',A/'prepare_ConeRidgeAlpha100_selected_candidate_v7_20261008.py',A/'seal_ConeRidgeAlpha100_selected_candidate_v7_20261008.py']))\n    connected_generator.source_paths=actual_windows_paths")
    out.append(save('run_ConeRidgeAlpha100_round144_full_registration_v8_20261008.py',value))
    create(A/'actual144_short_native_and135_receipt_recovery_v1_20261008.json',{'status':'passed_actual24_sources2619_graphs_and_fresh_paths_before_native144_retry','input_sha256':{str(p):sha(p) for p in [Path(__file__),*out,A/'short_content_addressed_native_storage_v1_20261008.py']},'actual_scored_records_unchanged':140,'old_partial_candidate_and_native_failure_preserved':True,'new_quality_scores':0})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    jobs=[('ConeRidgeAlpha100_selected_candidate_preparation_v7_20261008','prepare_ConeRidgeAlpha100_selected_candidate_v7_20261008.py'),('ConeRidgeAlpha100_selected_candidate_sealing_v7_20261008','seal_ConeRidgeAlpha100_selected_candidate_v7_20261008.py'),('BF16wide40_round135_full_registration_v7_20261008','run_BF16wide40_round135_full_registration_v7_20261008.py'),('ConeRidgeAlpha100_round144_full_registration_v8_20261008','run_ConeRidgeAlpha100_round144_full_registration_v8_20261008.py')]
    launches={n:start(n,driver,[],{}) for n,driver in jobs};create(A/'actual144_short_native_and135_receipt_launches_v1_20261008.json',{'launches':launches,'new_quality_scores':0})
    print(json.dumps({'started':list(launches)},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
