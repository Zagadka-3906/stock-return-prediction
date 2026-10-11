"""Measure only report serialization after round145, on immutable full round138 data."""
from pathlib import Path
from datetime import datetime
import ast
import gc
import hashlib
import json
import re
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from deferred_full_board_serialization_v1_20261008 import SOURCE, fragment, source_note

OUT = Path('E:/赛题五_本机临时/full_board_deferred_serialization_benchmark_v2_20261008')
DISPLAY = Path('E:/赛题五_本机临时/第138轮_20261008/display')


def gate():
    import psutil
    name = 'CrossFamilyFine125_round145_full_registration_v2_20261008'
    folder = A / 'service_owned_workflows_20261006' / name
    while True:
        if (folder / 'service_execution.json').exists():
            result = read(folder / 'service_execution.json')
            assert result['status'] == 'passed', result
            assert not owned(read(folder / 'native_launch.json'))
            break
        time.sleep(15)
    # Preserve the24GiB start threshold; give optional RAM waiting a finite300second budget.
    resource=Path('E:/赛题五_本机临时/full_board_deferred_resource_budget_v2_20261008')
    resource.mkdir(exist_ok=False)
    tick=time.monotonic();samples=[]
    while True:
        available=psutil.virtual_memory().available
        samples.append({'elapsed_seconds':time.monotonic()-tick,'available_bytes':available,'total_bytes':psutil.virtual_memory().total})
        if available>=24*2**30:break
        if time.monotonic()-tick>=300:
            create(resource/'verification.json',{'status':'actual_optional_benchmark_not_admitted_due_to300second_24GiB_RAM_boundary',
                'samples':samples,'minimum_required_available_bytes':24*2**30,'benchmark_encodes_executed':0,
                'new_model_fits':0,'new_quality_scores':0,'new_runtime_adopted':False,'test_labels_read':False})
            raise RuntimeError('Actual24GiB start resource unavailable throughout300seconds; optional speed benchmark withdrawn; model146 may continue unchanged.')
        time.sleep(15)
    create(resource/'verification.json',{'status':'actual_optional_benchmark_admitted_at_original24GiB_threshold','samples':samples,'new_quality_scores':0})
    assert psutil.disk_usage('E:/').free>30*2**30


def load_report():
    from build_lossless_ranking_display_v2_20261006 import unpack_report
    proof = read(DISPLAY / 'verification.json')
    assert proof['status'] == 'passed_all_original_report_values_and_six_views_lossless_roundtrip'
    page = DISPLAY / 'complete_rankings_lossless.html'
    assert sha(page) == proof['lossless_HTML_sha256']
    match = re.search(r'<script\s+id="data"\s+type="application/json">(.*?)</script>',
                      page.read_text(encoding='utf-8'), re.S)
    assert match
    report = unpack_report(json.loads(match.group(1)))
    assert len(report['connected']) == proof['connected_records'] == 14064
    assert report['notes'].count(source_note()) == 1
    return report, proof


def one_run(report, proof, index, deferred):
    import psutil
    directory = OUT / f'run{index}_{"deferred" if deferred else "original"}'
    directory.mkdir()
    local_report = dict(report, notes=[n for n in report['notes'] if n != source_note()])
    original_module = ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
    page_node = next(n for n in original_module.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == 'PAGE' for t in n.targets))
    template = ast.literal_eval(page_node.value)
    fixed = datetime.fromisoformat(report['generated_at_local'])

    class FixedDatetime:
        @staticmethod
        def now():
            return fixed

    encodes = []

    class TracedJSON:
        @staticmethod
        def dumps(value, **kwargs):
            tick = time.perf_counter()
            result = json.dumps(value, **kwargs)
            encodes.append({'indent': kwargs.get('indent'), 'seconds': time.perf_counter() - tick,
                            'characters': len(result)})
            return result

    namespace = {'ROOT': ROOT, 'OUT': directory, 'report': local_report,
                 'connected': report['connected'], 'PAGE': template,
                 'datetime': FixedDatetime, 'json': TracedJSON}
    procedure = fragment(deferred)
    stats = {'peak_RSS_bytes': 0, 'minimum_host_available_bytes': psutil.virtual_memory().available}
    stop = threading.Event()

    def sample():
        process = psutil.Process()
        while not stop.wait(.25):
            stats['peak_RSS_bytes'] = max(stats['peak_RSS_bytes'], process.memory_info().rss)
            stats['minimum_host_available_bytes'] = min(stats['minimum_host_available_bytes'], psutil.virtual_memory().available)

    observer = threading.Thread(target=sample, daemon=True)
    gc.collect()
    observer.start()
    tick = time.perf_counter()
    try:
        exec(procedure, namespace)
        elapsed = time.perf_counter() - tick
    finally:
        stop.set()
        observer.join()
    assert len(encodes) == (2 if deferred else 4)
    pretty = directory / 'all_model_rankings_20261003.json'
    html = directory / 'all_model_rankings_20261003.html'
    assert sha(pretty) == proof['original_report_sha256'], 'Actual complete original JSON bytes must match.'
    assert local_report['notes'] == report['notes']
    result = {'order': index, 'mode': 'deferred' if deferred else 'original',
              'serialization_phase_seconds': elapsed, 'actual_encode_calls': encodes,
              'JSON_sha256': sha(pretty), 'HTML_sha256': sha(html),
              'JSON_bytes': pretty.stat().st_size, 'HTML_bytes': html.stat().st_size, **stats}
    create(directory / 'measurement.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return result, pretty


def main():
    gate()
    assert not OUT.exists()
    OUT.mkdir()
    paths = [Path(__file__), A / 'deferred_full_board_serialization_v1_20261008.py',
             A / 'verify_deferred_full_board_QA_v2_20261008.py', SOURCE,
             A / 'verify_lossless_ranking_display_round138_20261007.py',
             A / 'verify_all_model_rankings_20261003.py', DISPLAY / 'verification.json',
             DISPLAY / 'complete_rankings_lossless.html',
             ROOT / 'results/validation_provenance_erratum_20261003.json']
    pins = {str(p): sha(p) for p in paths}
    create(OUT / 'frozen_before_actual_benchmark.json', {'input_sha256': pins,
        'orders': ['original', 'deferred', 'deferred', 'original'],
        'scope': 'actual_complete_14064_record_report_serialization_phase_only',
        'scientific_workers_held': 0, 'existing_139_to_145_runtime_not_changed': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    try:
        report, proof = load_report()
        measurements = []
        pretty = None
        for index, deferred in enumerate((False, True, True, False), 1):
            measurement, path = one_run(report, proof, index, deferred)
            measurements.append(measurement)
            if deferred:
                pretty = path
            gc.collect()
        assert len({m['JSON_sha256'] for m in measurements}) == 1
        assert len({m['HTML_sha256'] for m in measurements}) == 1
        from verify_deferred_full_board_QA_v2_20261008 import main as qa
        qa(138, report, pretty)
        qa_proof = read(OUT / 'full_original_QA/verification.json')
        assert qa_proof['status'] == 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
        for path, digest in pins.items():
            assert sha(path) == digest, path
        original = sum(m['serialization_phase_seconds'] for m in measurements if m['mode'] == 'original') / 2
        deferred = sum(m['serialization_phase_seconds'] for m in measurements if m['mode'] == 'deferred') / 2
        result = {'status': 'passed_actual_full14064_report_four_run_byte_equivalence_and_original_six_view_QA',
            'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': pins,
            'measurements': measurements, 'mean_original_serialization_seconds': original,
            'mean_deferred_serialization_seconds': deferred, 'measured_serialization_phase_speedup': original / deferred,
            'whole_pipeline_speedup_not_measured': True, 'new_runtime_not_yet_adopted': True,
            'original_source_unchanged': True, 'actual_full_QA_sha256': sha(OUT / 'full_original_QA/verification.json'),
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
        create(OUT / 'verification.json', result)
        create(A / 'actual_deferred_full_board_serialization_benchmark_v2_20261008.json',
               {'status': result['status'], 'output': str(OUT), 'verification_sha256': sha(OUT / 'verification.json')})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_full_report_benchmark',
               'at_local': datetime.now().isoformat(timespec='seconds'), 'error': f'{type(error).__name__}: {error}',
               'existing_scientific_runtime_unchanged': True})
        raise


if __name__ == '__main__':
    main()
