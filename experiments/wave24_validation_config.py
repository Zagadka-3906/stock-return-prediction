"""Recorded constants for historical eight-/sixteen-seed score reconstruction."""

import hashlib

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OUT = ROOT / 'experiments' / 'wave24_seed16_delivery_20260929'

DELIVERED = tuple(range(2026, 2034))

POOL16 = tuple(range(2026, 2042))

VALIDATION_YEARS = [2020, 2021, 2022, 2023, 2024]

EXPECTED_DELIVERED8 = {2020: 0.43088073116524317, 2021: 0.4239262375157104, 2022: 0.4447744734170406, 2023: 0.4191728780576189, 2024: 0.4196001207358905}

EXPECTED_FULL16 = {2020: 0.432158406, 2021: 0.4248897, 2022: 0.444829865, 2023: 0.418670801, 2024: 0.420366222}

EXPECTED_FULL16_TOLERANCE = 2e-09

EXPECTED_DELIVERED8_TOLERANCE = 1e-12

def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()
