"""Admit exact empty E-backed outputs and preserve bytes across volume boundaries."""
from pathlib import Path
from contextlib import contextmanager
import ctypes
import hashlib
import json
import os
import shutil
import time

ROOT = Path(__file__).resolve().parents[1]
EBASE = Path('E:/赛题五_本机临时/第150轮_20261008')
OUTPUTS = {
    ROOT/'candidates/HuberSparse59_v1_20261008': EBASE/'candidate',
    ROOT/'candidates/optimization_20261003_r150': EBASE/'registered_candidate',
    ROOT/'analysis/HuberSparse59_selected_release_v1_20261008': EBASE/'selected_release',
    ROOT/'analysis/HuberSparse59_official_comparison_v1_20261008': EBASE/'official_comparison',
    ROOT/'analysis/lossless_ranking_display_v2_20261006/round150': EBASE/'display',
    ROOT/'analysis/lossless_ranking_display_qa_v61_20261007': EBASE/'QA61',
}


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def empty(path):
    path = Path(path)
    expected = OUTPUTS[path]
    assert path.is_dir() and path.resolve() == expected.resolve(), path
    flags = ctypes.windll.kernel32.GetFileAttributesW(str(path))
    assert flags != 0xFFFFFFFF and flags & 0x400, path
    assert not any(path.iterdir()), 'Never admit a populated output.'


def ensure_display(path, number, create=True):
    assert number == 150
    assert Path(path) == ROOT/'analysis/lossless_ranking_display_v2_20261006/round150'
    empty(path)


def write_progress(path, value):
    path=Path(path)
    assert path.name=='actual_stage.json' and path.parent==ROOT/'analysis/HuberSparse59_official_comparison_v1_20261008'
    assert path.parent.resolve()==OUTPUTS[path.parent].resolve()
    temporary=path.with_name(path.name+f'.observer-{os.getpid()}.tmp')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    for attempt in range(500):
        try:os.replace(temporary,path);return
        except OSError as error:
            if error.errno not in (13,22) and getattr(error,'winerror',None) not in (32,33):raise
            if attempt==499:raise
            time.sleep(.1)


@contextmanager
def installed_transfer():
    original = os.link
    def transfer(source, destination, *args, **kwargs):
        source, destination = Path(source), Path(destination)
        assert source.is_file() and not destination.exists()
        resolved = destination.parent.resolve()
        assert resolved.is_relative_to(ROOT.resolve()) or resolved.is_relative_to(EBASE.resolve()), destination
        digest = sha(source)
        if source.resolve().drive.upper() == resolved.drive.upper():
            original(source, destination, *args, **kwargs)
        else:
            assert not args and not kwargs
            with source.open('rb') as reader, destination.open('xb') as writer:
                shutil.copyfileobj(reader, writer, 4*1024**2)
        assert sha(source) == sha(destination) == digest
    os.link = transfer
    try:
        yield
    finally:
        assert os.link is transfer
        os.link = original
