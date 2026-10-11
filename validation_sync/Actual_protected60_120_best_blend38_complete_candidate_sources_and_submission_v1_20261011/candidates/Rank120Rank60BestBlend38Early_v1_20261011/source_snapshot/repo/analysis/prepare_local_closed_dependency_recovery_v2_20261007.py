"""Recover pre-registration hash-route failure without rerunning any closed science."""
from pathlib import Path
import ast
import hashlib
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned

SOURCES = {
    'prepare_CPU_FULL_HGB44_round113_sources_v3_20261007.py': 'prepare_CPU_FULL_HGB44_round113_sources_v4_20261007.py',
    'run_CPU_FULL_HGB44_round113_full_registration_v3_20261007.py': 'run_CPU_FULL_HGB44_round113_full_registration_v4_20261007.py',
    'train_cpu_full_universe_ElasticNet_bank24_recovery_v2_20261007.py': 'train_cpu_full_universe_ElasticNet_bank24_recovery_v3_20261007.py',
    'run_full_universe_ElasticNet44_official_comparison_v2_20261007.py': 'run_full_universe_ElasticNet44_official_comparison_v3_20261007.py',
    'publish_cpu_full_universe_ElasticNet24_evidence_v4_20261007.py': 'publish_cpu_full_universe_ElasticNet24_evidence_v5_20261007.py',
    'prepare_CPU_ELASTIC_residual44_selected_candidate_v2_20261007.py': 'prepare_CPU_ELASTIC_residual44_selected_candidate_v3_20261007.py',
    'seal_CPU_ELASTIC_residual44_selected_candidate_v2_20261007.py': 'seal_CPU_ELASTIC_residual44_selected_candidate_v3_20261007.py',
    'prepare_CPU_ELASTIC44_round114_sources_v2_20261007.py': 'prepare_CPU_ELASTIC44_round114_sources_v3_20261007.py',
    'run_CPU_ELASTIC44_round114_full_registration_v2_20261007.py': 'run_CPU_ELASTIC44_round114_full_registration_v3_20261007.py',
    'verify_numpy_daily_ranks_full_parent_graph_v2_20261007.py': 'verify_numpy_daily_ranks_full_parent_graph_v3_20261007.py',
    'publish_numpy_daily_ranks_full_parent_controls_v2_20261007.py': 'publish_numpy_daily_ranks_full_parent_controls_v3_20261007.py',
    'observe_CPU_full_bank_resources_v2_20261007.py': 'observe_CPU_full_bank_resources_v3_20261007.py',
    'publish_CPU_full_bank_resource_observers_v2_20261007.py': 'publish_CPU_full_bank_resource_observers_v3_20261007.py',
    'run_protected_upper_pool_HGB66_official_comparison_20261007.py': 'run_protected_upper_pool_HGB66_official_comparison_v2_20261007.py',
    'publish_protected_upper_pool_HGB66_score_evidence_v2_20261007.py': 'publish_protected_upper_pool_HGB66_score_evidence_v3_20261007.py',
}
SERVICES = {
    'CPU_FULL_HGB44_round113_full_registration_v3': 'CPU_FULL_HGB44_round113_full_registration_v4',
    'cpu_full_universe_ElasticNet_native_bank24_v2': 'cpu_full_universe_ElasticNet_native_bank24_v3',
    'full_universe_ElasticNet44_official_comparison_v2': 'full_universe_ElasticNet44_official_comparison_v3',
    'cpu_full_universe_ElasticNet24_bank_evidence_publication_v3': 'cpu_full_universe_ElasticNet24_bank_evidence_publication_v4',
    'cpu_full_universe_ElasticNet24_scores_evidence_publication_v3': 'cpu_full_universe_ElasticNet24_scores_evidence_publication_v4',
    'CPU_ELASTIC44_selected_candidate_preparation_v2': 'CPU_ELASTIC44_selected_candidate_preparation_v3',
    'CPU_ELASTIC44_selected_candidate_sealing_v2': 'CPU_ELASTIC44_selected_candidate_sealing_v3',
    'CPU_ELASTIC44_round114_full_registration_v2': 'CPU_ELASTIC44_round114_full_registration_v3',
    'numpy_daily_ranks_full_parent_graph_preflight_v2': 'numpy_daily_ranks_full_parent_graph_preflight_v3',
    'numpy_daily_ranks_full_parent_controls_main_publication_v2': 'numpy_daily_ranks_full_parent_controls_main_publication_v3',
    'CPU_ElasticNet_full_bank_resource_observer_v2': 'CPU_ElasticNet_full_bank_resource_observer_v3',
    'CPU_full_bank_resource_observer_ElasticNet_main_publication_v2': 'CPU_full_bank_resource_observer_ElasticNet_main_publication_v3',
    'protected_upper_pool_HGB66_official_comparison': 'protected_upper_pool_HGB66_official_comparison_v2',
    'protected_upper_pool_HGB66_scores_main_publication_v2': 'protected_upper_pool_HGB66_scores_main_publication_v3',
}
FOLDERS = {
    'CPU_FULL_HGB44_round113_actual_registration_v3_20261007': 'CPU_FULL_HGB44_round113_actual_registration_v4_20261007',
    'CPU_FULL_HGB44_round113_source_preparation_v3_20261007': 'CPU_FULL_HGB44_round113_source_preparation_v4_20261007',
    'CPU_FULL_HGB44_round113_source_route_preflight_v2_20261007': 'CPU_FULL_HGB44_round113_source_route_preflight_v3_20261007',
    'cpu_full_universe_ElasticNet_bank24_recovery_v2_20261007': 'cpu_full_universe_ElasticNet_bank24_recovery_v3_20261007',
    'full_universe_ElasticNet44_official_comparison_v2_20261007': 'full_universe_ElasticNet44_official_comparison_v3_20261007',
    'cpu_full_universe_ElasticNet24_bank_recovery_v2_github_20261007': 'cpu_full_universe_ElasticNet24_bank_recovery_v3_github_20261007',
    'cpu_full_universe_ElasticNet24_scores_recovery_v2_github_20261007': 'cpu_full_universe_ElasticNet24_scores_recovery_v3_github_20261007',
    'CPU_ELASTIC_residual44_selected_release_recovery_v2_20261007': 'CPU_ELASTIC_residual44_selected_release_recovery_v3_20261007',
    'CPU_ELASTIC_residual44_recovery_v2_20261007': 'CPU_ELASTIC_residual44_recovery_v3_20261007',
    'CPU_ELASTIC44_round114_actual_registration_v2_20261007': 'CPU_ELASTIC44_round114_actual_registration_v3_20261007',
    'CPU_ELASTIC44_round114_source_preparation_v2_20261007': 'CPU_ELASTIC44_round114_source_preparation_v3_20261007',
    'CPU_ELASTIC44_round114_source_route_preflight_20261007': 'CPU_ELASTIC44_round114_source_route_preflight_v2_20261007',
    'numpy_daily_ranks_full_parent_graph_preflight_v2_20261007': 'numpy_daily_ranks_full_parent_graph_preflight_v3_20261007',
    'numpy_daily_ranks_full_parent_controls_v2_github_20261007': 'numpy_daily_ranks_full_parent_controls_v3_github_20261007',
    'CPU_ElasticNet_full_bank_resource_observation_v2_20261007': 'CPU_ElasticNet_full_bank_resource_observation_v3_20261007',
    'CPU_full_bank_resource_ElasticNet_v2_github_20261007': 'CPU_full_bank_resource_ElasticNet_v3_github_20261007',
    'protected_upper_pool_HGB66_official_comparison_20261007': 'protected_upper_pool_HGB66_official_comparison_v2_20261007',
    'protected_upper_pool_HGB66_scores_github_20261007': 'protected_upper_pool_HGB66_scores_v2_github_20261007',
}


def routed(text):
    mappings = {**{k[:-3]: v[:-3] for k, v in SOURCES.items()}, **SERVICES, **FOLDERS}
    return re.sub('|'.join(map(re.escape, sorted(mappings, key=len, reverse=True))),
        lambda m: mappings[m.group()], text)


def generated_without_io(path):
    text = path.read_text(encoding='utf-8')
    tree = ast.parse(text)
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    start = next(i for i,n in enumerate(main.body) if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='common' for t in n.targets))
    end = next(i for i,n in enumerate(main.body) if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='preflight' for t in n.targets))
    top = [n for n in tree.body if not isinstance(n, (ast.FunctionDef, ast.If))]
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name != 'main']
    namespace = {'__file__': str(path), '__name__': 'prospective_registry_routes_only'}
    code = ast.fix_missing_locations(ast.Module(body=top+funcs+main.body[start:end], type_ignores=[]))
    exec(compile(code, str(path), 'exec'), namespace)
    return namespace['generated'], namespace['routes']


def main():
    out = A / 'local_closed_dependency_recovery_v2_20261007.json'
    assert not out.exists()
    old = {}
    for service in SERVICES:
        folder = A / 'service_owned_workflows_20261006' / service
        row = read(folder/'native_launch.json')
        assert not owned(row), service
        terminal = read(folder/'service_execution.json')
        assert terminal['status']=='failed' or (service=='CPU_ElasticNet_full_bank_resource_observer_v2' and terminal['status']=='passed'), (service,terminal)
        old[service] = {'identity':row,'terminal':terminal,'source_sha256':sha(folder/'job_definition.json')}
    assert not list((A/'cpu_full_universe_ElasticNet_bank24_recovery_v2_20261007').rglob('model_*.joblib'))
    assert not (A/'optimization_20261003_r113').exists()
    for source,target in SOURCES.items():
        path=A/target
        assert not path.exists(), target
        text=routed((A/source).read_text(encoding='utf-8'))
        # Publisher's f-string folder token must advance as well as literal paths.
        if source.startswith('publish_cpu_full_universe_ElasticNet24'):
            text=text.replace('{phase}_recovery_v2_github_20261007','{phase}_recovery_v3_github_20261007')
        compile(text,str(path),'exec')
        with path.open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    controls=[]
    for number,filename,proof in (
        (113,SOURCES['prepare_CPU_FULL_HGB44_round113_sources_v3_20261007.py'],FOLDERS['CPU_FULL_HGB44_round113_source_route_preflight_v2_20261007']+'.json'),
        (114,SOURCES['prepare_CPU_ELASTIC44_round114_sources_v2_20261007.py'],FOLDERS['CPU_ELASTIC44_round114_source_route_preflight_20261007']+'.json')):
        generated,routes=generated_without_io(A/filename)
        assert len(generated)==8
        hashes={}
        for name,text in generated.items():
            assert not (A/name).exists(), name
            compile(text,str(A/name),'exec')
            hashes[name]=hashlib.sha256(text.encode('utf-8')).hexdigest()
            if name.startswith('register_'):
                assert 'baseline_score=comparison_baseline' in text
                assert "score_gain=winner['connected_final_score'] - comparison_baseline" in text
                assert "qualified_anchor_all_metrics_exact" in text
                assert "full_pool_transformation_including_nonflag_and2020_actual_native_forecasts" in text
                assert "actual_cold80_260_975_bits_exact" in text
        create(A/proof,{'status':'passed_prospective_eight_source_AST_and_original_QA_reverse_routes_only',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_generator_sha256':sha(A/filename),
            'generated_source_sha256':hashes,'routes':routes,'canonical_files_written':0,
            'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
        controls.append({'round':number,'proof':str(A/proof),'generated_source_sha256':hashes})
    create(out,{'status':'passed_actual_failed_terminal_history_and_fresh15_sources_exact16_generated_hash_preflights',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'original_failed_services':old,
        'sources':SOURCES,'services':SERVICES,'folders':FOLDERS,'prospective_controls':controls,
        'input_sha256':{str(A/name):sha(A/name) for name in [Path(__file__).name,*SOURCES,*SOURCES.values()]},
        'original24_HGB_fits_44_scores_and_anchor_candidate_controls_not_rerun':True,
        'original_ElasticNet_full_fits':0,'scientific_workers_stopped_suspended_restarted':0,
        'test_labels_read':False})
    print({'prepared_sources':len(SOURCES),'prospective_generated_sources':16,'canonical_files_written':0},flush=True)


if __name__=='__main__':main()
