"""Freeze, copy and byte-verify a preparation kit onto the identified USB drive."""
from pathlib import Path
import hashlib
import html
import json
import shutil
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'cooperation_worker_usb_v1_20261006'
KIT = OUT / '赛题五双机准备包'
USB = Path('F:/赛题五双机准备包_20261006')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024**2), b''):
            h.update(block)
    return h.hexdigest()


def main():
    signature = json.loads((OUT / 'installer_signature.json').read_text(encoding='utf-8-sig'))
    assert signature['Status'] == 'Valid'
    assert 'Python Software Foundation' in signature['Signer']
    download = json.loads((OUT / 'installer_download.json').read_text(encoding='utf-8'))
    assert sha(KIT / 'python-3.12.9-amd64.exe') == download['sha256']
    assert download['url'].startswith('https://www.python.org/ftp/python/3.12.9/')
    proof = json.loads((OUT / 'powershell_preflight.json').read_text(encoding='utf-8-sig'))
    assert proof['status'] == 'passed_actual_Windows_PowerShell51_source_parsing'
    assert not USB.exists()
    # This is an unfrozen preparation document. Correct one literal path before
    # the first user copy and retain the preparation digest in the final receipt.
    guide_path = KIT / '运行说明.txt'
    before = sha(guide_path)
    guide = guide_path.read_text(encoding='utf-8-sig')
    bad = 'D:\\赛题五协作\neports'
    assert guide.count(bad) == 1
    guide = guide.replace(bad, r'D:\赛题五协作\reports')
    guide_path.write_text(guide, encoding='utf-8-sig', newline='\r\n')
    document_path = KIT / '运行说明.html'
    document = document_path.read_text(encoding='utf-8')
    assert '<pre>' in document and '</pre>' in document
    document = document.split('<pre>')[0] + '<pre>' + html.escape(guide) + '</pre></body></html>'
    document_path.write_text(document, encoding='utf-8')
    assert html.unescape(document.split('<pre>', 1)[1].split('</pre>', 1)[0]) == guide
    assert not any(ord(c) < 32 and c not in '\n\t' for c in guide)
    # The old manifest binds the unchanged original ZIP, not the BOM-normalized
    # Windows5.1 copies. Keep it clearly identified as original metadata.
    (KIT / 'manifest.json').rename(KIT / '原始准备包文件清单.json')
    boot = A / 'cooperation_worker_bootstrap_20261006'
    for name in ('prepare_worker_environment.ps1', 'inspect_worker_hardware.ps1'):
        assert (KIT / name).read_text(encoding='utf-8-sig') == (boot / name).read_text(encoding='utf-8-sig')
    for path in KIT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    for path in KIT.glob('*.cmd'):
        text = path.read_text(encoding='ascii')
        assert '%~dp0' in text and 'pause' in text and 'exit /b %RESULT%' in text
        worker = 'worker1' if 'worker1' in path.name else 'worker2'
        assert f'-WorkerId {worker}' in text
    assert sha(KIT / '原始准备包.zip') == 'b294ebf2ff8d7d1ce80cfde92c83ba4bc87f5b096d20295a130274a7e20695a7'
    files = {str(p.relative_to(KIT)): {'bytes': p.stat().st_size, 'sha256': sha(p)}
             for p in sorted(KIT.iterdir()) if p.is_file()}
    manifest = {
        'status': 'frozen_preparation_kit_no_remote_installation_or_training_performed',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'files': files,
        'installer_official_url': download['url'], 'installer_signature': signature,
        'dependencies_downloaded_by_workers_over_internet': True,
        'Python_installer_included': True, 'training_data_and_models_included': False,
        'Windows_PowerShell51_parse_passed': True,
    }
    (KIT / 'USB文件校验.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    packed = OUT / '赛题五双机准备包_20261006.zip'
    with zipfile.ZipFile(packed, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(KIT.iterdir()):
            archive.write(path, '赛题五双机准备包/' + path.name)
    with zipfile.ZipFile(packed) as archive:
        assert archive.testzip() is None
        for path in KIT.iterdir():
            assert hashlib.sha256(archive.read('赛题五双机准备包/' + path.name)).hexdigest() == sha(path)
    shutil.copytree(KIT, USB)
    shutil.copyfile(packed, USB / packed.name)
    actual = {}
    for path in KIT.iterdir():
        target = USB / path.name
        assert sha(target) == sha(path), str(target)
        actual[path.name] = sha(target)
    assert sha(USB / packed.name) == sha(packed)
    receipt = {
        'status': 'copied_to_identified_USB_and_every_file_rehashed_successfully',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'USB_directory': str(USB),
        'USB_file_count': len(actual) + 1, 'USB_total_bytes': sum(p.stat().st_size for p in USB.iterdir()),
        'verified_USB_sha256': actual, 'archive_sha256': sha(packed),
        'archive_file': str(USB / packed.name),
        'unfrozen_guide_literal_path_corrected_before_first_delivery': {'previous_SHA256': before, 'final_SHA256': sha(guide_path)},
        'installer_signature_verified': True, 'all_PS51_scripts_parsed': True,
        'all_Python_sources_compiled_without_execution': True,
        'existing_USB_files_changed_or_deleted': False,
        'remote_worker_installation_or_training_performed': False,
        'sources_sha256': {str(p): sha(p) for p in (Path(__file__), A / 'build_cooperation_worker_usb_v1_20261006.py')},
    }
    (OUT / 'USB_copy_verification_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: receipt[k] for k in ('status', 'USB_directory', 'USB_file_count', 'USB_total_bytes', 'archive_sha256')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
