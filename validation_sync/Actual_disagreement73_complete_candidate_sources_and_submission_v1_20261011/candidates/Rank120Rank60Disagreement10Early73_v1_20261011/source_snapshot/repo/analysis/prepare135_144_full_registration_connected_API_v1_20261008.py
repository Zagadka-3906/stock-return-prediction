"""Fresh original-QA receivers; only dependency receipts and main publication transport repaired."""
from pathlib import Path
import sys,ast,json,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    service='exact135_144_connected_API_publication_reconciliation_v3_20261008'
    assert read(A/'service_owned_workflows_20261006'/service/'service_execution.json')['status']=='passed'
    outputs=[];records=[]
    for number,stem,oldver,newver,genver,receiptold,receiptnew in [(135,'BF16wide40',5,6,4,2,3),(144,'ConeRidgeAlpha100',6,7,4,1,2)]:
        source=A/f'run_{stem}_round{number}_full_registration_v{oldver}_20261008.py';target=A/f'run_{stem}_round{number}_full_registration_v{newver}_20261008.py';assert not target.exists()
        value=source.read_text(encoding='utf8')
        value=value.replace(stem+'_scores_main_publication_v5_20261008',service).replace(stem+'_selected_candidate_sealing_v5_20261008',stem+'_selected_candidate_sealing_v6_20261008')
        value=value.replace(f'actual_registration_v{oldver}_20261008',f'actual_registration_v{newver}_20261008').replace(f'full_registration_v{oldver}_file_IO_20261008',f'full_registration_v{newver}_file_IO_20261008')
        # Existing source-generation and graph contracts are retained byte-for-byte.
        hook=f'''    import prepare_{stem}_round{number}_sources_v{genver}_20261008 as connected_generator
    prior_source_paths=connected_generator.source_paths
    def actual_connected_source_paths():
        paths=[Path(str(p).replace('{stem}_scores_github_v1_20261008/receipt.json','{stem}_scores_github_v{receiptnew}_20261008/receipt.json').replace('{stem}_scores_github_v{receiptold}_20261008/receipt.json','{stem}_scores_github_v{receiptnew}_20261008/receipt.json')) for p in prior_source_paths()]
        extras=[Path(__file__),A/'connected_API_full_round_transport_v1_20261008.py',A/'prepare135_144_full_registration_connected_API_v1_20261008.py',A/'exact135_144_connected_API_reconciliation_v3_20261008.json',A/'reconcile_exact135_144_connected_API_publication_v3_20261008.py',A/'prepare135_144_candidates_after_connected_API_v2_20261008.py',A/'candidates135_144_connected_API_recovery_v1_20261008.json',A/'prepare_{stem}_selected_candidate_v6_20261008.py',A/'seal_{stem}_selected_candidate_v6_20261008.py']
        for name in ('{stem}_selected_candidate_preparation_v6_20261008','{stem}_selected_candidate_sealing_v6_20261008'):
            folder=A/'service_owned_workflows_20261006'/name;extras.extend(folder.glob('*.json'));extras.extend(folder.glob('*.log'))
        return list(dict.fromkeys([*paths,*extras]))
    connected_generator.source_paths=actual_connected_source_paths
'''
        needle=f'    from prepare_{stem}_round{number}_sources_v{genver}_20261008 import main as prepare_sources';assert value.count(needle)==1;value=value.replace(needle,hook+needle)
        needle=f'        from publish_{stem}_round{number}_full_validation_20261008 import main as github';assert value.count(needle)==1
        value=value.replace(needle,f'        from connected_API_full_round_transport_v1_20261008 import execute_actual_publisher\n        def github():execute_actual_publisher({number})')
        if number==144:
            value=value.replace("'ConeRidgeAlpha100_selected_candidate_sealing_v6_20261008'):","'ConeRidgeAlpha100_selected_candidate_sealing_v6_20261008','BF16wide40_round135_full_registration_v6_20261008'):")
        compile(value,str(target),'exec');target.write_text(value,encoding='utf8',newline='\n');outputs.append(target);records.append({'original':str(source),'original_sha256':sha(source),'fresh':str(target),'fresh_sha256':sha(target)})
    pins={str(p):sha(p) for p in [Path(__file__),*outputs,A/'connected_API_full_round_transport_v1_20261008.py',A/'exact135_144_connected_API_reconciliation_v3_20261008.json']}
    create(A/'full135_144_connected_API_registration_recovery_v1_20261008.json',{'status':'frozen_two_fresh_original_full_QA_and_connected_API_publication_receivers','records':records,'input_sha256':pins,'native_science_and_original_QA_unchanged':True,'new_quality_scores':0,'old_failed_services_preserved':True})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launches={name:start(name,p.name,[],pins) for name,p in zip(('BF16wide40_round135_full_registration_v6_20261008','ConeRidgeAlpha100_round144_full_registration_v7_20261008'),outputs)}
    create(A/'full135_144_connected_API_registration_hidden_launches_v1_20261008.json',{'status':'started_original_QA_receivers_with_serial_board_registration_and_exact_main_API_rendezvous','launches':launches,'input_sha256':pins})
    print(json.dumps({'started':list(launches)},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
