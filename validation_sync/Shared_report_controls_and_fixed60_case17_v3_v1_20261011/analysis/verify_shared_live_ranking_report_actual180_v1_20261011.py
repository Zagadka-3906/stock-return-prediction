"""Actual full180 byte identity and strict private reader controls before adoption."""
from pathlib import Path
import sys, json, time, math, hashlib
A = Path(__file__).resolve().parent; sys.path[:0] = [str(A.parent), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    import psutil
    while psutil.virtual_memory().available < 3 * 2**30:
        assert allowed(); time.sleep(15)
    assert allowed()
    import shared_live_ranking_report_runtime_v1_20261011 as runtime
    from verified_shared_publication_board_loader_v1_20261011 import SharedBoard
    original = read(A/'verified_shared_publication_board_loader_actual_complete180_controls_v1_20261011.json')
    for p, d in original['input_sha256'].items(): assert sha(p) == d, p
    archive = A/'lossless_ranking_display_v2_20261006/round180/full_report_reconstructed_for_publication.json.gz'
    owner = SharedBoard(archive); started = time.perf_counter(); report = owner.load()
    containers = runtime.validate_json_tree(report)
    digest, count = runtime.native_digest(report)
    assert (digest, count) == (original['original_native_sha256'], original['original_native_bytes'])
    state = {'report': report, 'shared_reads': 0}; marker = runtime.ReportText(state)
    proxy = runtime.JsonProxy(json)
    assert proxy.loads(marker) is report and proxy.loads(marker) is report
    assert len(report['connected']) == 17062 and state['shared_reads'] == 2
    for value in [None, {'中文': '\\n', 'x': [0., -0., 1e-7, True, None]}, [1, 2]]:
        assert proxy.loads(json.dumps(value)) == value
    for invalid in [float('nan'), float('inf'), (1, 2), {1: 'bad'}, {'x': object()}]:
        try: runtime.validate_json_tree(invalid)
        except AssertionError: pass
        else: raise AssertionError('Non JSON graph admitted')
    cycle = []; cycle.append(cycle)
    try: runtime.validate_json_tree(cycle)
    except AssertionError: pass
    else: raise AssertionError('Cycle admitted')
    shared = {'x': [1, 2]}; runtime.validate_json_tree({'a': shared, 'b': shared})
    try: proxy.loads(marker, parse_float=str)
    except AssertionError: pass
    else: raise AssertionError('Custom parse hook must not reuse typed report')
    owner.reverify()
    pins = {str(p): sha(p) for p in [Path(__file__), Path(runtime.__file__),
        A/'verified_shared_publication_board_loader_actual_complete180_controls_v1_20261011.json', *map(Path, owner.pins)]}
    for p, d in pins.items(): assert sha(p) == d, p
    create(runtime.PROOF, {'status': 'passed_actual180_native_bytes_typed_graph_and_private_reader_controls',
        'input_sha256': pins, 'original_native_sha256': digest, 'original_native_bytes': count,
        'connected_records': 17062, 'unique_containers': containers,
        'actual_RSS_bytes': psutil.Process().memory_info().rss,
        'elapsed_seconds': time.perf_counter()-started,
        'private_reader_controls': True, 'runtime_not_yet_adopted': True,
        'full_installed_scope_and_restore_control_still_required_before_adoption': True,
        'original_full_browser_QA_still_required_for_each_round': True,
        'new_fits': 0, 'new_scores': 0, 'test_labels_read': False})
    print({'status': 'passed_actual_full180_live_report_reader_controls', 'native_bytes': count}, flush=True)

if __name__ == '__main__': main()
