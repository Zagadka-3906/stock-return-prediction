"""Prepare a versioned R50 engine adapter for the latest qualified R62 graph."""
from pathlib import Path
from datetime import datetime
import ast
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from locked_read_hash_cache_20261004 import fresh_sha


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    analysis = ROOT / 'analysis'
    source = analysis / 'optimize_training_round50.py'
    target = analysis / 'optimize_training_round63.py'
    out = analysis / 'latest_graph_joint_round63_source_preflight_20261005'
    out.mkdir(exist_ok=True)
    assert not target.exists() and not (out / 'verification.json').exists()
    old_protocol = read(analysis / 'optimization_20261003_r50/protocol.json')
    assert fresh_sha(source) == old_protocol['input_sha256'][str(source.resolve())]
    text = source.read_text(encoding='utf-8')
    changes = []
    def replace(before, after):
        nonlocal text
        assert before in text, before
        text = text.replace(before, after)
        changes.append({'before': before, 'after': after})
    replace('optimize_training_round49', 'optimize_training_round62')
    replace('optimization_20261003_r49', 'optimization_20261003_r62')
    replace('optimization_20261003_r50', 'optimization_20261003_r63')
    replace('optimize_training_round50', 'optimize_training_round63')
    replace('from selected_scheme_graph_20261004 import with_weight_overrides',
        'from latest_graph_joint_axes_20261005 import active_axes,with_weight,retention_axes,expected_records')
    replace("GRAPH=ROOT/'analysis/whole_selected_scheme_graph_20261004/graph.json'", "GRAPH_FIELD='latest_joint_scheme_graph'\nNUMBER=63\nfuture_native_sources=resolve_native_sources")
    replace("def baseline():return {**previous.configuration(read(PREVIOUS/'selection.json')['winner']),'whole_scheme_graph':deepcopy(read(GRAPH)['graph'])}",
        "def baseline():\n    cfg=previous.configuration(read(PREVIOUS/'selection.json')['winner'])\n    graph=deepcopy(cfg['nystrom_ridge_standalone_scheme_graph'])\n    graph['active_weight_axes']=active_axes(graph)\n    return {**cfg,'latest_joint_scheme_graph':graph}")
    replace("def retention_axes(graph):\n    return [{'kind':'root','round':graph['root']['round']}]+[\n        {'kind':'layer','round':node['round']} for node in graph['layers'] if node['specs']['membership']['weight']>0]\ndef expected_records(graph):return 1+18*len(graph['active_weight_axes'])+5*len(retention_axes(graph))+20\n", '')
    start = text.index('def freeze():\n')
    end = text.index('def prefix_controls(', start)
    text = text[:start] + '''def freeze():
    if (OUT/'protocol.json').exists():verify();return
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    assert complete_round_evidence(62) is not None
    OUT.mkdir(exist_ok=True)
    graph=baseline()['latest_joint_scheme_graph']
    plan=ROOT/'analysis/latest_graph_joint_search_plan_20261005.json'
    preflight=ROOT/'analysis/latest_graph_joint_round63_source_preflight_20261005/verification.json'
    prepared=read(preflight)
    assert prepared['status']=='passed_pre_execution_source_and_lazy_dispatch_checks'
    for path,digest in prepared['input_sha256'].items():assert sha(path)==digest,path
    sources=[Path(__file__),ROOT/'analysis/latest_graph_joint_axes_20261005.py',
        ROOT/'analysis/finalize_training_round63.py',ROOT/'analysis/predict_latest_joint_scheme_20261005.py',
        ROOT/'analysis/check_latest_joint_scheme_20261005.py',ROOT/'analysis/run_training_round63_pipeline.py',
        ROOT/'analysis/prepare_latest_graph_joint_round63_sources_20261005.py',plan,preflight,
        ROOT/'analysis/latest_graph_joint_axes_scope_audit_20261005/verification.json',
        ROOT/'analysis/whole_scheme_replay_runtime_20261004.py',ROOT/'analysis/whole_scheme_future_runtime_20261004.py',
        ROOT/'analysis/nystrom_ridge_release_engine_20261004.py',ROOT/'analysis/predict_nystrom_ridge_scheme_20261004.py',
        ROOT/'analysis/parallel_candidate_scoring_four_20261004.py',ROOT/'analysis/publish_training_round.py',
        ROOT/'analysis/build_all_model_rankings_20261003.py',ROOT/'analysis/verify_all_model_rankings_20261003.py',
        ROOT/'后续选模标准.md',ROOT/'active_release.json',state_mapping_path(),
        PREVIOUS/'selection.json',PREVIOUS/'protocol.json',PREVIOUS/'selected_validation.npy',
        PREVIOUS/'provenance_scope_execution.json',
        ROOT/'results/optimization_20261003_r62.json',ROOT/'candidates/optimization_20261003_r62/verification.json',
        ROOT/'candidates/optimization_20261003_r62/manifest.json']
    sources += [Path(path) for path in read(PREVIOUS/'protocol.json')['input_sha256']]
    for paths in raw_sources(graph).values():sources.extend(paths)
    native=resolve_native_sources(graph);roots=root_model_sources(graph)
    sources += [Path(info['path']) for info in {**native,**roots}.values()]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'baseline_score':expected(),'starting_configuration':baseline(),
        'weight_axes':active_axes(graph),'retention_axes':retention_axes(graph),
        'expected_scored_records':expected_records(graph),
        'records_formula':'1+18*actual_weight_axes+5*actual_retention_axes+20',
        'waves':list(WAVES),'new_model_training':False,'new_fold_models_trained':0,
        'same_validation':'5635800 rows;1212 continuous days;2020–2024 expanding mature-label OOF',
        'method':'Current complete graph joint weights, both coordinate orders, historical retention, final temporal processing.',
        'axes_recomputed_from_actual_r62_effective_branches':True,
        'cached_earlier_active_weight_axes_not_used_as_authority':True,
        'weight_values':'zero,half,anchor,double,anchor+0.0125,anchor+0.025; clipped[0,0.8]',
        'retention_values':RETENTIONS,'each_adaptive_anchor_frozen_before_its_candidate_scores':True,
        'fixed_model_names_and_other_hyperparameters':True,
        'parallel_candidate_execution':{'workers':4,'ordered_commits':True,'private_official_scoring':True},
        'future_native_model_sources':native,'future_root_model_sources':roots,
        'current_parameter_authority':GRAPH_FIELD,
        'selection_rule':'highest actual complete official connected score; exact ties prefer fewer active model branches',
        'test_labels_read':False,'test_future_prices_used_to_select':False,
        'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
        'global_resource_exhaustion_established':False,
        'input_sha256':{str(path.resolve()):sha(path) for path in dict.fromkeys(sources)}},immutable=True)

''' + text[end:]
    replace('whole_scheme_graph', 'latest_joint_scheme_graph')
    replace('super().configure(cfg)', "super().configure({'whole_scheme_graph':cfg.get(GRAPH_FIELD,cfg.get('whole_scheme_graph'))})")
    replace('from predict_whole_scheme_round50 import predict', 'from predict_latest_joint_scheme_20261005 import predict')
    replace("with_weight_overrides(proposal['latest_joint_scheme_graph'],{(axis['round'],axis['group'],axis['role']):value})",
        "with_weight(proposal['latest_joint_scheme_graph'],axis,value,axes())")
    replace('whole_selected_R49_validation_bit_identical', 'latest_selected_R62_validation_bit_identical')
    replace('Round50 whole-scheme joint candidate', 'Round63 latest-graph joint candidate')
    for before, after in zip(range(214, 219), range(261, 266)):
        text = re.sub(rf'(?<![0-9]){before}(?![0-9])', str(after), text)
    ast.parse(text)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(text)
    names = ['latest_graph_joint_axes_20261005.py', 'latest_graph_joint_search_plan_20261005.json',
        'latest_graph_joint_axes_scope_audit_20261005/verification.json', 'optimize_training_round63.py',
        'finalize_training_round63.py', 'check_latest_joint_scheme_20261005.py',
        'predict_latest_joint_scheme_20261005.py', 'run_training_round63_pipeline.py',
        'prepare_latest_graph_joint_round63_sources_20261005.py', 'optimize_training_round50.py',
        'nystrom_ridge_release_engine_20261004.py', 'predict_nystrom_ridge_scheme_20261004.py',
        'frozen_provenance_execution_scope_20261004.py', 'locked_read_hash_cache_20261004.py']
    for name in names:
        path = analysis / name
        if path.suffix == '.py':
            ast.parse(path.read_text(encoding='utf-8'))
    result = subprocess.run([sys.executable, '-B', '-X', 'utf8', 'analysis/run_training_round63_pipeline.py', '--probe'],
        cwd=ROOT, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    probe = json.loads(result.stdout)
    assert probe['lazy_imports_only'] and probe['rss_bytes'] < 50 * 2**20
    assert probe['new_model_fits'] == probe['new_quality_scores'] == 0
    definitions = {node.name for node in ast.parse(text).body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    assert {'freeze', 'build', 'independent', 'forward', 'reverse', 'retention_refinement', 'temporal_refinement', 'Context'}.issubset(definitions)
    create(out / 'verification.json', {'status': 'passed_pre_execution_source_and_lazy_dispatch_checks',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'original_joint_engine_source_preserved': str(source),
        'effective_source': str(target), 'explicit_source_transformations': changes,
        'source_transform_does_not_establish_actual_quality': True, 'all_real_baseline_and_score_and_candidate_checks_pending': True,
        'probe': probe, 'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
        'input_sha256': {str((analysis / name).resolve()): fresh_sha(analysis / name) for name in names}})
    print(json.dumps({'status': 'passed_pre_execution_source_and_lazy_dispatch_checks',
        'lazy_dispatch_rss_bytes': probe['rss_bytes'], 'actual_quality_records': 0}), flush=True)


if __name__ == '__main__':
    main()
