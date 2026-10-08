"""Correct the pending scorer's failed upstream identity before any actual185 scoring."""
from pathlib import Path
import ast
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT/'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

META = A/'Joint147_actual_scorer_upstream_recovery_v6_20261008.json'
SCORER = 'run_JointCrossHuberOrder185_official_comparison_v2_20261008.py'
DRIVERS = {
    'verify_JointCrossHuberOrder185_round147_sources_v2_20261008.py': 'verify_JointCrossHuberOrder185_round147_sources_v4_20261008.py',
    'publish_JointCrossHuberOrder185_evidence_v4_20261008.py': 'publish_JointCrossHuberOrder185_evidence_v6_20261008.py',
    'prepare_JointCrossHuberOrder185_selected_candidate_v3_20261008.py': 'prepare_JointCrossHuberOrder185_selected_candidate_v5_20261008.py',
    'run_JointCrossHuberOrder185_round147_full_registration_v5_20261008.py': 'run_JointCrossHuberOrder185_round147_full_registration_v7_20261008.py',
}
EXTRAS = [Path(__file__), META, A/SCORER, *(A/name for name in DRIVERS.values()), A/'dispatch_JointCrossHuber147_complete_pipeline_v4_20261008.py']


def execute(original, phase=None):
    for path, digest in read(META)['input_sha256'].items():
        assert sha(path) == digest, path
    import prepare_JointCrossHuberOrder185_round147_sources_v4_20261008 as generator
    paths = generator.source_paths
    generator.source_paths = lambda: list(dict.fromkeys([*paths(), *EXTRAS]))
    from recover_Joint147_after_actual146_retry_v5_20261008 import execute as protected
    protected(original, phase)


def main():
    assert not META.exists()
    scoring_folder = A/'JointCrossHuberOrder185_official_comparison_v1_20261008'
    assert not list(scoring_folder.glob('case*_official.json'))
    assert not (scoring_folder/'frozen_before_actual_full_controls_and_official_scores.json').exists()
    prefix = 'JointCrossHuberOrder185'
    suffixes = ('round147_source_admission', 'controls_main_publication', 'official_comparison', 'scores_main_publication', 'selected_candidate_preparation', 'selected_candidate_sealing', 'round147_full_registration')
    assert all(not (A/'service_owned_workflows_20261006'/f'{prefix}_{suffix}_v1_20261008').exists() for suffix in suffixes)
    original = A/'run_JointCrossHuberOrder185_official_comparison_v1_20261008.py'
    original_source = original.read_text(encoding='utf8')
    substitutions = {
        'HuberCrossFamilyFine125_round146_full_registration_v2_20261008': 'HuberCrossFamilyFine125_round146_full_registration_v4_20261008',
        'actual_JointCrossHuber181_parent134_location_v1_20261008.json': 'actual_JointCrossHuber181_parent134_location_v2_20261008.json',
    }
    corrected = original_source
    for old, new in substitutions.items():
        assert corrected.count(old) == 1, old
        corrected = corrected.replace(old, new)
    restored = corrected
    for old, new in substitutions.items(): restored = restored.replace(new, old)
    assert ast.dump(ast.parse(restored), include_attributes=False) == ast.dump(ast.parse(original_source), include_attributes=False)
    products = [save(SCORER, corrected)]
    for original_name, new_name in DRIVERS.items():
        source = "from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_Joint147_actual_scorer_upstream_v6_20261008 import execute\n"
        if original_name.startswith('publish_'):
            source += f"if __name__=='__main__':\n import argparse\n parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('controls','scores'));execute({original_name!r},parser.parse_args().phase)\n"
        else:
            source += f"if __name__=='__main__':execute({original_name!r})\n"
        products.append(save(new_name, source))
    dispatcher = A/'dispatch_JointCrossHuber147_complete_pipeline_v3_20261008.py'
    dispatch_source = dispatcher.read_text(encoding='utf8')
    from recover_Joint147_after_actual146_retry_v5_20261008 import DRIVERS as earlier
    replacements = {earlier[old]:new for old,new in DRIVERS.items()}
    replacements['run_JointCrossHuberOrder185_official_comparison_v1_20261008.py'] = SCORER
    for old,new in replacements.items():
        assert old in dispatch_source, old
        dispatch_source = dispatch_source.replace(old,new)
    dispatch_source = dispatch_source.replace('complete_hidden_launches_v3_20261008', 'complete_hidden_launches_v4_20261008')
    old_pins = "pins={str(Path(__file__)):sha(__file__),str(p):sha(p)};rows={}"
    assert dispatch_source.count(old_pins) == 1
    dispatch_source = dispatch_source.replace(old_pins, "from recover_Joint147_actual_scorer_upstream_v6_20261008 import META,EXTRAS\n pins={str(Path(__file__)):sha(__file__),str(p):sha(p),**{str(f):sha(f) for f in EXTRAS}};rows={}")
    products.append(save('dispatch_JointCrossHuber147_complete_pipeline_v4_20261008.py',dispatch_source))
    pins = {str(path):sha(path) for path in [Path(__file__), original, dispatcher, A/'recover_Joint147_after_actual146_retry_v5_20261008.py', A/'Joint147_actual146_retry_receivers_v5_20261008.json', *products]}
    create(META, {'status':'prospectively_corrected_actual147_scorer_failed_upstream_and_actual_full_control_pointer',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256':pins,
        'only_scorer_string_substitutions':substitutions,'scorer_AST_exact_after_reversing_two_identity_substitutions':True,
        'all_numeric_transform_score_case_return_mapping_and_selection_code_unchanged':True,
        'original185_grid_and32_prospective_routes_and_all_prior_sources_preserved':True,
        'new_quality_scores':0, 'test_labels_read':False})
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    old_launch = read(A/'service_owned_workflows_20261006/JointCrossHuber147_complete_chronological_dispatch_v3_20261008/native_launch.json')
    parent, worker, proof = suspended_idle(old_launch, '    closed (dispatch_JointCrossHuber147_complete_pipeline_v3_20261008.py:8)')
    try:
        assert not worker.children()
        assert all(not (A/'service_owned_workflows_20261006'/f'{prefix}_{suffix}_v1_20261008').exists() for suffix in suffixes)
        worker.terminate(); worker.wait(timeout=10)
        parent.terminate(); parent.wait(timeout=10)
    finally:
        for process in (parent,worker):
            if process.is_running(): process.resume()
    create(A/'Joint147_proved_idle_dispatch3_retired_before_actual185_scoring_v6_20261008.json', {
        'status':'retired_only_proved_idle_pending_dispatcher_before_first185_score',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'launch':old_launch,'idle_stack':proof,
        'actual_full181_and_native80_workers_preserved':True,'scientific_workers_stopped':0})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launch = start('JointCrossHuber147_complete_chronological_dispatch_v4_20261008', products[-1].name, [], {**pins,str(META):sha(META)})
    assert owned(launch)
    create(A/'Joint147_actual_scorer_upstream_hidden_launch_v6_20261008.json',launch)
    print({'status':'corrected147_dispatch4_running_before_any185_score','worker':launch['owned_worker_pid']},flush=True)


if __name__=='__main__': main()
