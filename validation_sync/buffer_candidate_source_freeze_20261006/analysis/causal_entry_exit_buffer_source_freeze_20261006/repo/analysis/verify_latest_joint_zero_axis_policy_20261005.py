"""Count actual historical hybrid and pure graphs; do not add quality scores."""
from pathlib import Path
from datetime import datetime
import ast
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from latest_joint_zero_axis_stage_policy_20261005 import actual_records
from latest_graph_joint_axes_20261005 import active_axes, retention_axes
from locked_read_hash_cache_20261004 import LockedReadHashCache, fresh_sha


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    analysis = ROOT / 'analysis'
    output = analysis / 'latest_joint_zero_axis_policy_preflight_20261005'
    output.mkdir(exist_ok=True)
    assert not (output / 'verification.json').exists()
    original = analysis / 'latest_graph_joint_round63_source_preflight_20261005/verification.json'
    prepared = read(original)
    for path, digest in prepared['input_sha256'].items():
        assert fresh_sha(path) == digest, path
    files = [Path(__file__), original, analysis / 'latest_joint_zero_axis_stage_policy_20261005.py',
        analysis / 'run_latest_joint_round63_locked_v2_20261005.py',
        analysis / 'optimization_20261003_r59/selection.json',
        analysis / 'optimization_20261003_r54/selection.json']
    inputs = {**prepared['input_sha256'], **{str(p.resolve()): fresh_sha(p) for p in files}}
    with LockedReadHashCache(inputs):
        hybrid = read(files[-2])['winner']['portfolio_surrogate_role_scheme_graph']
        ranking = read(files[-1])['ranking']
        scored = [r for r in ranking if r['no_dropout_standalone_scheme_graph']['root']['kind'] == 'standalone']
        assert scored
        pure = scored[0]['no_dropout_standalone_scheme_graph']
        results = []
        for name, graph in (('actual_selected_r59', hybrid), ('actual_scored_r54_pure', pure)):
            axes, retention = len(active_axes(graph)), len(retention_axes(graph))
            waves = [1 + 6 * axes, max(1, 6 * axes), max(1, 6 * axes), 5 * retention, 20]
            assert all(n > 0 for n in waves) and sum(waves) == actual_records(graph)
            results.append({'source_case': name, 'active_weight_axes': axes,
                'wave_records': waves, 'total_records': sum(waves), 'all_publication_stages_nonempty': True})
        assert results[0]['total_records'] == 260 and results[1]['total_records'] == 28
        for source in files[:4]:
            if source.suffix == '.py':
                ast.parse(source.read_text(encoding='utf-8'))
        process = subprocess.run([sys.executable, '-B', '-X', 'utf8', 'analysis/run_latest_joint_round63_locked_v2_20261005.py', '--probe'],
            cwd=ROOT, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        probe = json.loads(process.stdout)
        assert probe['lazy_imports_only'] and probe['rss_bytes'] < 50 * 2**20
    value = {'status': 'passed_actual_scored_graph_count_and_source_binding_checks',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'actual_graph_cases': results,
        'original_prepared_sources_preserved': True, 'only_zero_axis_coordinate_stages_add_two_baseline_controls': True,
        'all_actual_full_vector_quality_candidate_and_causal_checks_still_pending': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
        'probe': probe, 'input_sha256': inputs}
    with (output / 'verification.json').open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'status': value['status'], 'actual_graph_case_counts': results, 'new_quality_scores': 0}), flush=True)


if __name__ == '__main__':
    main()
