"""Reuse unchanged14 science and generated24 source preflights, bind the actual15 score receipt for honest anchor reuse."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def save(path,text):
    assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n')
def main():
    sources=[];outputs=[]
    mapping={'BF16reverse40_scores_main_publication_v14_20261008':'BF16reverse40_scores_main_publication_v15_20261008',
        'BF16reverse40_selected_candidate_preparation_v14_20261008':'BF16reverse40_selected_candidate_preparation_v15_20261008',
        'BF16reverse40_selected_candidate_sealing_v14_20261008':'BF16reverse40_selected_candidate_sealing_v15_20261008',
        'BF16reverse40_scores_github_v1_20261008/receipt.json':'BF16reverse40_scores_github_v2_20261008/receipt.json'}
    for role in ('prepare','seal'):
        old=A/f'{role}_BF16reverse40_selected_candidate_v14_20261008.py';value=old.read_text(encoding='utf8')
        for before,after in mapping.items():value=value.replace(before,after)
        value=value.replace('seal_BF16reverse40_selected_candidate_v14_20261008.py','seal_BF16reverse40_selected_candidate_v15_20261008.py')
        target=A/f'{role}_BF16reverse40_selected_candidate_v15_20261008.py';save(target,value);sources.append(old);outputs.append(target)
    old=A/'run_BF16reverse40_round138_full_registration_v14_20261008.py';value=old.read_text(encoding='utf8')
    for before,after in mapping.items():value=value.replace(before,after)
    value=value.replace('actual_registration_v14_20261008','actual_registration_v15_20261008').replace('full_registration_v14_file_IO_20261008','full_registration_v15_file_IO_20261008')
    value=value.replace('from file_backed_hidden_git_runtime_20261007 import installed','from verified_TLS_Git_retry_runtime_v1_20261008 import installed')
    needle='    from prepare_BF16reverse40_round138_sources_v14_20261008 import main as prepare_sources';assert value.count(needle)==1
    hook="""    import prepare_BF16reverse40_round138_sources_v14_20261008 as actual_generator
    original_paths=actual_generator.source_paths
    def actual15_paths():
        paths=[]
        for path in original_paths():
            if path.name=='receipt.json' and path.parent.name=='BF16reverse40_scores_github_v1_20261008':path=A/'BF16reverse40_scores_github_v2_20261008/receipt.json'
            paths.append(path)
        extras=[Path(__file__),A/'prepare_actual138_candidate_registration_after_TLS15_20261008.py',
            A/'recover_actual138_score_publication_TLS_v15_20261008.py',A/'verified_TLS_Git_retry_runtime_v1_20261008.py',
            A/'actual138_TLS_score_publication_recovery_v15_20261008.json',A/'actual138_candidate_registration_recovery_v15_20261008.json',
            A/'publish_BF16reverse40_evidence_v15_20261008.py',A/'prepare_BF16reverse40_selected_candidate_v15_20261008.py',A/'seal_BF16reverse40_selected_candidate_v15_20261008.py']
        for name in ('BF16reverse40_scores_main_publication_v15_20261008','BF16reverse40_selected_candidate_preparation_v15_20261008','BF16reverse40_selected_candidate_sealing_v15_20261008'):
            folder=A/'service_owned_workflows_20261006'/name;extras.extend(folder.glob('*.json'));extras.extend(folder.glob('*.log'))
        return list(dict.fromkeys([*paths,*extras]))
    actual_generator.source_paths=actual15_paths
"""
    value=value.replace(needle,hook+needle)
    target=A/'run_BF16reverse40_round138_full_registration_v15_20261008.py';save(target,value);sources.append(old);outputs.append(target)
    pins={str(p):sha(p) for p in [Path(__file__),*sources,*outputs,A/'verified_TLS_Git_retry_runtime_v1_20261008.py']}
    create(A/'actual138_candidate_registration_recovery_v15_20261008.json',{'status':'frozen_actual15_receipt_and_gate_receivers_same40_official_records_and_same24_generated_scientific_sources',
        'input_sha256':pins,'administrative_dependency_and_receipt_mapping':mapping,'all14_scientific_sources_preserved':True,
        'fresh_TLS_retries_do_not_change_Git_payload_or_model_math':True,'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    names=['BF16reverse40_selected_candidate_preparation_v15_20261008','BF16reverse40_selected_candidate_sealing_v15_20261008','BF16reverse40_round138_full_registration_v15_20261008']
    rows={name:start(name,path.name,[],pins) for name,path in zip(names,outputs)}
    create(A/'actual138_candidate_registration_hidden_launches_v15_20261008.json',{'launches':rows,'input_sha256':pins,'new_quality_scores':0})
    print(json.dumps({'started':list(rows)}),flush=True)
if __name__=='__main__':main()
