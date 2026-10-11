"""Fetch a checksum-verified portable diagnostic binary to D without installing packages."""
from pathlib import Path
from datetime import datetime
import hashlib
import io
import json
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tools/readonly_pyspy_diagnostics_20261006'


def main():
    assert not OUT.exists()
    metadata_url = 'https://pypi.org/pypi/py-spy/json'
    with urllib.request.urlopen(metadata_url, timeout=30) as response:
        metadata = json.load(response)
    urls = metadata['info'].get('project_urls') or {}
    assert any('github.com/benfred/py-spy' in value for value in urls.values())
    candidates = [entry for entry in metadata['urls'] if entry['filename'].endswith('win_amd64.whl')]
    assert len(candidates) == 1
    wheel = candidates[0]
    assert wheel['url'].startswith('https://files.pythonhosted.org/')
    with urllib.request.urlopen(wheel['url'], timeout=30) as response:
        data = response.read()
    assert hashlib.sha256(data).hexdigest() == wheel['digests']['sha256']
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        executables = [name for name in archive.namelist() if name.endswith('/py-spy.exe') or name == 'py-spy.exe']
        assert len(executables) == 1
        binary = archive.read(executables[0])
    OUT.mkdir(parents=True)
    executable = OUT / 'py-spy.exe'
    executable.write_bytes(binary)
    receipt = {'status': 'downloaded_checksum_verified_portable_binary_under_D',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'metadata_url': metadata_url,
        'version': metadata['info']['version'], 'wheel_filename': wheel['filename'], 'wheel_url': wheel['url'],
        'wheel_sha256': wheel['digests']['sha256'], 'binary': str(executable),
        'binary_sha256': hashlib.sha256(binary).hexdigest(), 'binary_bytes': len(binary),
        'Python_environment_changed': False, 'project_files_or_caches_created_on_C': False,
        'training_process_not_modified': True}
    with (OUT / 'receipt.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(receipt, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
