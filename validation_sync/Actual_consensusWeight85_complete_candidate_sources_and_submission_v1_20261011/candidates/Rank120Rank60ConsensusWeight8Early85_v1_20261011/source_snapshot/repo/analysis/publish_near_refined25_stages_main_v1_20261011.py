"""Publish declared sources, actual37 scores and actual native14 controls to main."""
from pathlib import Path
import re, runpy, sys

A = Path(__file__).resolve().parent
ROOT = A.parent
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed, closed


def main():
    template = A / 'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    declaration = A / 'near_refined25_sources_and_dispatch_admission_v1_20261011.json'
    native_declaration = declaration
    plan_path = A / 'rank5_rank20_near_refined25_predeclared_plan_v1_20261011.json'
    plan = read(plan_path)
    for phase in ('sources', 'official25'):
        assert allowed()
        paths = [Path(__file__), template, ROOT / '后续选模标准.md', declaration, native_declaration, plan_path]
        for p in (declaration, native_declaration):
            for filename, digest in read(p)['input_sha256'].items():
                assert sha(filename) == digest, filename
                paths.append(Path(filename))
        actual_native = actual_cold = actual_prefit = 0
        if phase == 'official25':
            closed(plan['actual_service'])
            folder = Path(plan['output'])
            proof = read(folder / 'verification.json')
            assert len(proof['records']) == proof['new_quality_score_records'] == 25
            assert (proof['actual_nonidentity_full_controls'], proof['actual_nonidentity_prefix_controls']) == (24, 72)
            for filename, digest in proof['input_sha256'].items():
                assert sha(filename) == digest, filename
                if Path(filename).suffix.lower() in ('.json', '.py', '.md'):
                    paths.append(Path(filename))
            paths.extend(p for p in folder.glob('*.json') if p.name not in ('actual_stage.json', 'best_so_far.json'))
            paths.extend(Path(row['official_score_cache']['official_metrics_source']) for row in proof['records'])
        paths = list(dict.fromkeys(paths))
        assert all(p.is_file() for p in paths)
        stem = 'near_refined25_' + phase + '_v1_20261011'
        text = template.read_text(encoding='utf8')
        text = text.replace('StockRank20_actual_own6_full5_v66_20261010', stem)
        text = text.replace('StockRank20_actual_own6_full5_main_v66_20261010', 'near_refined25_' + phase + '_main_v1_20261011')
        text = text.replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010', 'near_refined25_' + phase + '_main_receipt_v1_20261011')
        text = text.replace('main_publisher_v11_20261010', 'main_publisher_reboot_v12_20261011')
        start = text.index('    paths=')
        end = text.index('    import publish_classifier_consensus_workflows_20261006 as h', start)
        text = text[:start] + '    paths=[Path(__file__),*[Path(p) for p in ' + repr([str(p) for p in paths]) + ']]\n' + text[end:]
        start = text.index("    payload[(prefix/'manifest.json').as_posix()]")
        end = text.index('    out=Path(', start)
        metadata = {'status': 'actual_near_pure_horizon_refined25_phase_evidence', 'phase': phase,
                    'official_score_records': 25 if phase == 'official25' else 0,
                    'actual_full_Pandas_controls': 24 if phase == 'official25' else 0,
                    'actual_prefix_controls': 72 if phase == 'official25' else 0,
                    'actual_native_cases': actual_native, 'actual_cold_cases': actual_cold,
                    'actual_prefit_refusals': actual_prefit, 'new_native_fits': 0,
                    'new_quality_scores_by_publication': 0, 'training_populations_equal_not_claimed': True,
                    'adaptive_TRAIN_selection_bias_uncorrected': True,
                    'full191_registration_and_candidate_not_yet_created': True,
                    'future_candidate_qualification_pending': True, 'test_labels_read': False,
                    'global_exhaustion_proven': False}
        text = text[:start] + "    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**" + repr(metadata) + ",'files':bindings})\n" + text[end:]
        text, count = re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",
                             repr('保存跨目标小比例融合的25项较大权重保护排序及实际原生独立检查：' + phase), text)
        assert count == 1
        target = A / ('publish_' + stem + '_payload_main.py')
        assert not target.exists(), target
        compile(text, str(target), 'exec')
        target.write_text(text, encoding='utf8', newline='\n')
        assert allowed()
        runpy.run_path(str(target), run_name='__main__')


if __name__ == '__main__':
    main()
