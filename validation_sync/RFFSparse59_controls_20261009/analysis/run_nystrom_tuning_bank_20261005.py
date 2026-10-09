"""Run real controls and serialized past-only fits without competing for scarce RAM."""
from pathlib import Path
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def main():
    import train_nystrom_tuning_bank_20261005 as bank
    import verify_nystrom_tuning_bank_20261005 as preflight
    scratch = Path(bank.read(bank.STORAGE)['temporary_directory'])
    assert bank.OUT.drive.upper() in ('D:', 'E:') and scratch.drive.upper() in ('D:', 'E:')
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        assert Path(bank.native.os.environ[key]) == scratch
    run_path = ROOT / 'analysis/nystrom_tuning_bank_run_20261005.json'
    deadline = time.monotonic() + 60
    while not run_path.exists():
        assert time.monotonic() < deadline, 'Launch receipt missing before any numerical or training work.'
        time.sleep(.1)
    for path, digest in bank.read(run_path)['input_sha256'].items():
        assert bank.sha(Path(path)) == digest, path
    last = time.monotonic()
    while psutil.virtual_memory().available < 14 * 2**30:
        if time.monotonic() - last >= 50:
            print('Waiting for14GiB available RAM before numerical preflight; scheduling reserve only.', flush=True)
            last = time.monotonic()
        time.sleep(10)
    preflight.main()
    bank.all_oof()
    print('All50 actual mature annual fits passed; complete-output quality validation remains pending.', flush=True)


if __name__ == '__main__':
    main()
