"""Bind the verified API score receipt to fresh candidate/sealing/full receivers without changing science."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def save(path,value):
    assert not path.exists(),path;compile(value,str(path),'exec');path.write_text(value,encoding='utf8',newline='\n')
def main():
    old=A/'verified_TLS_Git_retry_runtime_v1_20261008.py'
    value=old.read_text(encoding='utf8').replace("'unexpected eof'","'unexpected eof','http 408','http 429','http 502','http 503','http 504','rpc failed','unexpected disconnect','remote end hung up'")
    retry=A/'verified_TLS_Git_retry_runtime_v2_20261008.py';save(retry,value)
    mapping={'BF16reverse40_scores_main_publication_v15_20261008':'exact138_connected_API_publication_reconciliation_v1_20261008',
        'BF16reverse40_selected_candidate_preparation_v15_20261008':'BF16reverse40_selected_candidate_preparation_v16_20261008',
        'BF16reverse40_selected_candidate_sealing_v15_20261008':'BF16reverse40_selected_candidate_sealing_v16_20261008',
        'BF16reverse40_scores_github_v2_20261008/receipt.json':'BF16reverse40_scores_github_v3_20261008/receipt.json'}
    outputs=[];sources=[old]
    for role in ('prepare','seal'):
        old=A/f'{role}_BF16reverse40_selected_candidate_v15_20261008.py';value=old.read_text(encoding='utf8')
        for before,after in mapping.items():value=value.replace(before,after)
        value=value.replace('seal_BF16reverse40_selected_candidate_v15_20261008.py','seal_BF16reverse40_selected_candidate_v16_20261008.py')
        target=A/f'{role}_BF16reverse40_selected_candidate_v16_20261008.py';save(target,value);sources.append(old);outputs.append(target)
    old=A/'run_BF16reverse40_round138_full_registration_v15_20261008.py';value=old.read_text(encoding='utf8')
    for before,after in mapping.items():value=value.replace(before,after)
    value=value.replace("A/'BF16reverse40_scores_github_v2_20261008/receipt.json'","A/'BF16reverse40_scores_github_v3_20261008/receipt.json'")
    value=value.replace('actual_registration_v15_20261008','actual_registration_v16_20261008').replace('full_registration_v15_file_IO_20261008','full_registration_v16_file_IO_20261008')
    value=value.replace('verified_TLS_Git_retry_runtime_v1_20261008','verified_TLS_Git_retry_runtime_v2_20261008')
    value=value.replace('actual15_paths','actual16_paths')
    needle="        for name in ('exact138_connected_API_publication_reconciliation_v1_20261008'";assert needle in value
    value=value.replace(needle,"        extras.extend([A/'prepare_actual138_verified_API_candidate_registration_v16_20261008.py',A/'actual138_verified_API_candidate_registration_recovery_v16_20261008.json',A/'reconcile_exact138_connected_API_publication_v1_20261008.py',A/'exact138_connected_API_reconciliation_v1_20261008.json',A/'prepare_BF16reverse40_selected_candidate_v16_20261008.py',A/'seal_BF16reverse40_selected_candidate_v16_20261008.py',A/'BF16reverse40_scores_github_v3_20261008/receipt.json'])\n"+needle)
    target=A/'run_BF16reverse40_round138_full_registration_v16_20261008.py';save(target,value);sources.append(old);outputs.append(target)
    pins={str(p):sha(p) for p in [Path(__file__),*sources,*outputs,retry,A/'reconcile_exact138_connected_API_publication_v1_20261008.py']}
    create(A/'actual138_verified_API_candidate_registration_recovery_v16_20261008.json',{'status':'frozen_verified_API_main_receipt_and_fresh16_admin_receivers_same40_scores_same24_generated_sources',
        'input_sha256':pins,'administrative_dependency_and_receipt_mapping':mapping,'all14_scientific_sources_preserved':True,'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    names=['BF16reverse40_selected_candidate_preparation_v16_20261008','BF16reverse40_selected_candidate_sealing_v16_20261008','BF16reverse40_round138_full_registration_v16_20261008']
    rows={n:start(n,p.name,[],pins) for n,p in zip(names,outputs)}
    create(A/'actual138_verified_API_candidate_registration_hidden_launches_v16_20261008.json',{'launches':rows,'input_sha256':pins,'new_quality_scores':0})
    print(json.dumps({'started':list(rows)}),flush=True)
if __name__=='__main__':main()
