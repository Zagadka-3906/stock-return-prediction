"""Allow only an exact empty project-owned E display junction, before any output exists."""
from pathlib import Path
import ctypes

ROOT = Path(__file__).resolve().parents[1]


def ensure(path, number, create=True):
    path = Path(path)
    assert number in (133, 134)
    logical = ROOT / 'analysis/lossless_ranking_display_v2_20261006' / f'round{number}'
    assert path == logical
    if not path.exists():
        if create:
            path.mkdir(parents=True)
        return
    attributes = ctypes.windll.kernel32.GetFileAttributesW(str(path))
    assert attributes != 0xFFFFFFFF and attributes & 0x400, 'Existing output must be a junction.'
    expected = Path('E:/赛题五_本机临时/完整榜归档_20261008') / f'round{number}'
    assert path.resolve() == expected.resolve()
    assert path.is_dir() and not any(path.iterdir()), 'Never reuse a populated display output.'

