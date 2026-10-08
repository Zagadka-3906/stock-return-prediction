"""Reuse forty completed scores exactly; fresh publication/candidate/seal/registration after preserved TLS failures."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert read(A/'service_owned_workflows_20261006/BF16wide40_official_comparison_v4_20261008/service_execution.json')['status']=='passed'
    assert read(A/'BF16wide40_official_comparison_v1_20261008/verification.json')['new_quality_score_records']==40
    changes={
        'BF16wide40_scores_main_publication_v4_20261008':'BF16wide40_scores_main_publication_v5_20261008',
        'BF16wide40_selected_candidate_preparation_v4_20261008':'BF16wide40_selected_candidate_preparation_v5_20261008',
        'BF16wide40_selected_candidate_sealing_v4_20261008':'BF16wide40_selected_candidate_sealing_v5_20261008',
        'BF16wide40_scores_github_v1_20261008/receipt.json':'BF16wide40_scores_github_v2_20261008/receipt.json'}
    originals=['publish_BF16wide40_evidence_v4_20261008.py','prepare_BF16wide40_selected_candidate_v4_20261008.py',
               'seal_BF16wide40_selected_candidate_v4_20261008.py','run_BF16wide40_round135_full_registration_v4_20261008.py']
    outputs=[];sources=[Path(__file__),A/'BF16wide40_official_comparison_v1_20261008/verification.json']
    for name in originals:
        source=A/name;sources.append(source);text=source.read_text(encoding='utf8')
        for before,after in changes.items():text=text.replace(before,after)
        if name.startswith('publish_'):
            needle="out=A/f'BF16wide40_{phase}_github_v1_20261008'";assert text.count(needle)==1
            text=text.replace(needle,"out=A/f'BF16wide40_{phase}_github_v2_20261008'")
        if name.startswith('run_'):
            text=text.replace('actual_registration_v4_20261008','actual_registration_v5_20261008').replace('full_registration_v4_file_IO_20261008','full_registration_v5_file_IO_20261008')
            needle='    from prepare_BF16wide40_round135_sources_v4_20261008 import main as prepare_sources'
            assert text.count(needle)==1
            hook='''    import prepare_BF16wide40_round135_sources_v4_20261008 as actual_generator
    original_source_paths=actual_generator.source_paths
    def actual_recovered_source_paths():
        paths=[Path(str(p).replace('BF16wide40_scores_github_v1_20261008/receipt.json','BF16wide40_scores_github_v2_20261008/receipt.json')) for p in original_source_paths()]
        extras=[Path(__file__),A/'recover_BF16wide135_after_TLS_publication_v5_20261008.py',
            A/'BF16wide135_TLS_publication_receiver_recovery_v5_20261008.json',
            A/'publish_BF16wide40_evidence_v5_20261008.py',A/'prepare_BF16wide40_selected_candidate_v5_20261008.py',
            A/'seal_BF16wide40_selected_candidate_v5_20261008.py']
        return list(dict.fromkeys([*paths,*extras]))
    actual_generator.source_paths=actual_recovered_source_paths
'''
            text=text.replace(needle,hook+needle)
        outputs.append(save(name.replace('_v4_','_v5_'),text))
    for name in ('BF16wide40_scores_main_publication_v4_20261008','BF16wide40_selected_candidate_preparation_v4_20261008',
                 'BF16wide40_selected_candidate_sealing_v4_20261008','BF16wide40_round135_full_registration_v4_20261008'):
        folder=A/'service_owned_workflows_20261006'/name;sources.extend(folder.glob('service_execution.json'));sources.extend(folder.glob('stderr.log'))
    pins={str(p):sha(p) for p in [*sources,*outputs]}
    create(A/'BF16wide135_TLS_publication_receiver_recovery_v5_20261008.json',{
        'status':'frozen_fresh_four_administrative_receivers_after_TLS_failure_with_actual40_scores_unchanged',
        'input_sha256':pins,'dependency_changes':changes,'main_transport_uses_verified_Windows_Schannel_HTTP11',
        'all_models_and_CDF_and_grid_and_original_generated24_receivers_unchanged':True,
        'original_failed_drivers_and_terminal_and_logs_preserved':True,'new_quality_scores':0,'new_native_fits':0})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    jobs=[('BF16wide40_scores_main_publication_v5_20261008',outputs[0].name,['scores']),
          ('BF16wide40_selected_candidate_preparation_v5_20261008',outputs[1].name,[]),
          ('BF16wide40_selected_candidate_sealing_v5_20261008',outputs[2].name,[]),
          ('BF16wide40_round135_full_registration_v5_20261008',outputs[3].name,[])]
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'BF16wide135_TLS_publication_hidden_launches_v5_20261008.json',{
        'status':'started_four_fresh135_receivers_for_exact40_existing_scores_and_QA46_main',
        'launches':launches,'input_sha256':pins,'new_quality_scores':0,'full135_registration_and_future_dependency_repair_still_required':True})
    print('Completed40 BF16 scores retained; fresh publication/candidate/sealing/registration5 started.',flush=True)
if __name__=='__main__':main()
