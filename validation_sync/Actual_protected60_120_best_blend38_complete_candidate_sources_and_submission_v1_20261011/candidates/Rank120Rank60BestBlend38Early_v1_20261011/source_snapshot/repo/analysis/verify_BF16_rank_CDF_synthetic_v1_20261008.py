"""Exercise new2020-active rank-CDF roles on tied, invalid, flagged and whole-day prefix fixtures."""
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import sha, create


def main():
    import numpy as np
    import BF16_complete_parent_rank_CDF_v1_20261008 as codec
    out = A / 'BF16_rank_CDF_synthetic_preflight_v1_20261008'
    assert not out.exists();out.mkdir()
    rng = np.random.default_rng(2026100827)
    dates = np.repeat(np.array([20200102, 20201230, 20250102], dtype=np.int32), 4650)
    parent = np.round(rng.normal(size=len(dates)), 2).astype(np.float64)
    neural = np.round(rng.normal(size=len(dates)), 2).astype(np.float64)
    valid = rng.random(len(dates)) > .17
    flags = (rng.random(len(dates)) > .85).astype(np.int8)
    parent[~valid] = -1e6;neural[~valid] = -1e6
    pins = {str(p): sha(p) for p in [Path(__file__), Path(codec.__file__)]}
    create(out / 'frozen_before_actual_synthetic_controls.json', {'input_sha256': pins,
        'dates': [20200102, 20201230, 20250102], 'rows': len(dates),
        'synthetic_dates_not_actual_future_data': True, 'new_quality_scores': 0, 'test_labels_read': False})
    records = []
    prepared = codec.prepare(parent, neural, dates, flags, valid)
    for role in codec.ROLES:
        for weight in (0., .0025, .025, .2, .5, 1.):
            value = codec.apply_prepared(parent, flags, valid, role, weight, prepared)
            oracle = codec.pandas_oracle(parent, neural, dates, flags, valid, role, weight)
            assert np.array_equal(value.view('u8'), oracle.view('u8'))
            cohort = codec.selected(flags, valid, role)
            assert np.array_equal(value[~cohort].view('u8'), parent[~cohort].view('u8'))
            for days in (1, 2):
                n = days*4650
                prefix = codec.transform(parent[:n], neural[:n], dates[:n], flags[:n], valid[:n], role, weight)
                assert np.array_equal(prefix.view('u8'), value[:n].view('u8'))
            if weight == 0.:assert np.array_equal(value.view('u8'), parent.view('u8'))
            else:assert np.any(value[dates<20210101] != parent[dates<20210101])
            records.append({'role': role, 'weight': weight, 'full_oracle_and2_prefixes_bits_exact': True})
    for p, d in pins.items(): assert sha(p) == d, p
    create(out / 'verification.json', {'status': 'passed_actual18_synthetic_BF16_rank_CDF_roles_and36_day_prefixes',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'records': records,
        'first2020_active_explicitly_checked': True, 'invalid_and_declared_unselected_forecast_bits_preserved': True,
        'new_quality_scores': 0, 'test_labels_read': False, 'actual5635800_and111_cold_controls_pending': True})
    print('18 actual tied/invalid/cohort fixtures and36 day-prefix checks passed;2020 active.', flush=True)


if __name__ == '__main__':main()
