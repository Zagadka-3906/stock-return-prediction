"""Recover the failed operational publisher without restarting any actual185 scoring."""
from pathlib import Path
import ast
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
META=A/'Joint147_publisher_phase_scratch_recovery_v7_20261008.json'
DRIVERS={
    'publish_JointCrossHuberOrder185_evidence_v4_20261008.py':'publish_JointCrossHuberOrder185_evidence_v7_20261008.py',
    'prepare_JointCrossHuberOrder185_selected_candidate_v3_20261008.py':'prepare_JointCrossHuberOrder185_selected_candidate_v6_20261008.py',
    'run_JointCrossHuberOrder185_round147_full_registration_v5_20261008.py':'run_JointCrossHuberOrder185_round147_full_registration_v8_20261008.py'}


def protected_module():
    path=A/'recover_Joint147_after_actual146_retry_v5_20261008.py'
    text=path.read_text(encoding='utf8')
    before="A/'Joint147_actual146_retry_file_IO_v5_20261008'/DRIVERS[original].removesuffix('.py')"
    after="A/'Joint147_phase_separated_file_IO_v7_20261008'/(DRIVERS[original].removesuffix('.py')+('_'+phase if phase else ''))"
    assert text.count(before)==1
    corrected=text.replace(before,after)
    assert ast.dump(ast.parse(text),include_attributes=False)==ast.dump(ast.parse(corrected.replace(after,before)),include_attributes=False)
    namespace={'__file__':str(path),'__name__':'protected_Joint147_verified_temp_phase_recovery'}
    exec(compile(corrected,str(path),'exec'),namespace)
    namespace['MAP']={**namespace['MAP'],'JointCrossHuberOrder185_scores_main_publication_v1_20261008':'JointCrossHuberOrder185_scores_main_publication_v2_20261008'}
    namespace['DRIVERS']={**namespace['DRIVERS'],**DRIVERS}
    return namespace


def execute(original,phase=None):
    assert original in DRIVERS
    for path,digest in read(META)['input_sha256'].items():assert sha(path)==digest,path
    import prepare_JointCrossHuberOrder185_round147_sources_v4_20261008 as generator
    from recover_Joint147_actual_scorer_upstream_v6_20261008 import EXTRAS as earlier
    paths=generator.source_paths
    extra=[*earlier,Path(__file__),META,*(A/name for name in DRIVERS.values())]
    generator.source_paths=lambda:list(dict.fromkeys([*paths(),*extra]))
    protected_module()['execute'](original,phase)


def main():
    services=A/'service_owned_workflows_20261006'
    failed=services/'JointCrossHuberOrder185_scores_main_publication_v1_20261008/service_execution.json'
    assert read(failed)['status']=='failed' and 'FileExistsError' in read(failed)['failure']
    assert read(services/'JointCrossHuber147_complete_chronological_dispatch_v4_20261008/service_execution.json')['status']=='failed'
    scoring=read(services/'JointCrossHuberOrder185_official_comparison_v1_20261008/native_launch.json')
    assert owned(scoring)
    pending=['JointCrossHuberOrder185_selected_candidate_preparation_v1_20261008',
        'JointCrossHuberOrder185_selected_candidate_sealing_v1_20261008','JointCrossHuberOrder185_round147_full_registration_v1_20261008']
    assert all(not (services/name).exists() for name in pending)
    products=[]
    for old,new in DRIVERS.items():
        text="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_Joint147_publisher_phase_scratch_v7_20261008 import execute\n"
        if old.startswith('publish_'):
            text+=f"if __name__=='__main__':\n import argparse\n parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('controls','scores'));execute({old!r},parser.parse_args().phase)\n"
        else:text+=f"if __name__=='__main__':execute({old!r})\n"
        products.append(save(new,text))
    protected_module()
    pins={str(path):sha(path) for path in [Path(__file__),A/'recover_Joint147_after_actual146_retry_v5_20261008.py',
        A/'recover_Joint147_actual_scorer_upstream_v6_20261008.py',A/'Joint147_actual_scorer_upstream_recovery_v6_20261008.json',
        failed,services/'JointCrossHuber147_complete_chronological_dispatch_v4_20261008/service_execution.json',*products,
        *(A/name for name in DRIVERS),A/'seal_JointCrossHuberOrder185_selected_candidate_v1_20261008.py']}
    create(META,{'status':'recovered_failed_scores_publisher_with_distinct_phase_scratch_and_preserved_live185_scoring',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'original_scores_service1_and_dispatch4_failures_preserved':True,
        'new_scores_service':'JointCrossHuberOrder185_scores_main_publication_v2_20261008',
        'actual185_scoring_identity_preserved':scoring,'controls_and_scores_have_distinct_exclusive_IO_folders':True,
        'temporary_folder_change_is_AST_exact_after_reversal':True,
        'numerical_models_parameters_mapping_native_replays_selection_and_generated32_routes_unchanged':True,
        'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={}
    specifications=[('JointCrossHuberOrder185_scores_main_publication_v2_20261008',products[0],['scores']),
        (pending[0],products[1],[]),(pending[1],A/'seal_JointCrossHuberOrder185_selected_candidate_v1_20261008.py',[]),
        (pending[2],products[2],[])]
    for name,path,args in specifications:rows[name]=start(name,path.name,args,{**pins,str(META):sha(META)})
    assert owned(scoring) and all(owned(row) for row in rows.values())
    create(A/'Joint147_publisher_phase_scratch_hidden_launches_v7_20261008.json',{
        'status':'started_only_failed_scores_publication_retry_and_previously_unstarted_remaining_receivers',
        'launches':rows,'original_scoring_worker_not_stopped_or_restarted':True,'new_quality_scores':0})
    print({'started':{name:row['owned_worker_pid'] for name,row in rows.items()},'original_scoring_worker':scoring['owned_worker_pid']},flush=True)


if __name__=='__main__':main()
