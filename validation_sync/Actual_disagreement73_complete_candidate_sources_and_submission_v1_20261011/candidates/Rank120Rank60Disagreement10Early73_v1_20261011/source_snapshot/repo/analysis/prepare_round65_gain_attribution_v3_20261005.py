"""Check scorer labels against raw training precision, preserving both failed audits."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    old = ROOT / 'analysis/audit_limit_up_score_gain_round65_v2_20261005.py'
    new = ROOT / 'analysis/audit_limit_up_score_gain_round65_v3_20261005.py'
    run = ROOT / 'analysis/round65_limit_up_gain_audit_v3_run_20261005.json'
    assert not new.exists() and not run.exists()
    text = old.read_text(encoding='utf-8').replace(
        'round65_limit_up_gain_audit_v2_20261005', 'round65_limit_up_gain_audit_v3_20261005')
    text = text.replace("               ROOT / 'data/features.parquet',",
                        "               ROOT / 'data/features.parquet', ROOT / 'data/raw/训练集.csv',")
    text = text.replace("    original_labels = original['y_ret_1d'].to_numpy()", """    raw_training = pd.read_csv(ROOT / 'data/raw/训练集.csv', usecols=['ts_code', 'trade_date', 'y_ret_1d'])
    raw_training = raw_training.loc[raw_training['trade_date'].between(20200101, 20241231)].sort_values(['trade_date', 'ts_code']).reset_index(drop=True)
    assert keys.equals(pl.from_pandas(raw_training[['ts_code', 'trade_date']]).select('ts_code', pl.col('trade_date').cast(pl.Int64)))
    original_labels = raw_training['y_ret_1d'].to_numpy(dtype=np.float64)""")
    text = text.replace("'official_adapter_labels_and_flags_proven_original_training_only': True,",
                        "'official_adapter_labels_and_flags_proven_original_training_only': True,\n              'label_origin_checked_against_raw_float64_training_labels': True,\n              'feature_table_float32_labels_not_used_for_spearman': True,")
    ast.parse(text)
    new.write_text(text, encoding='utf-8', newline='')
    errors = [ROOT / 'analysis/run_logs/round65_limit_up_gain_audit_20261005.stderr.log',
              ROOT / 'analysis/run_logs/round65_limit_up_gain_audit_v2_repaired_20261005.stderr.log']
    repair = {'status': 'preserved_previous_auxiliary_failures_and_checked_raw_label_precision',
              'at_local': datetime.datetime.now().isoformat(),
              'reason': 'Feature generation intentionally stores y_ret_1d as float32; official validation labels preserve raw training precision. Compare against original raw training CSV, retaining the exact official pandas scoring labels.',
              'previous_source_sha256': sha(old), 'new_source_sha256': sha(new),
              'preserved_failed_stderr_sha256': {str(path): sha(path) for path in errors},
              'official_score_and_scientific_source_unchanged': True,
              'new_quality_scores': 0, 'test_labels_read': False}
    (ROOT / 'analysis/round65_limit_up_gain_audit_v3_repair_20261005.json').write_text(
        json.dumps(repair, ensure_ascii=False, indent=2), encoding='utf-8')
    scratch = ROOT / 'tmp/round65_limit_up_gain_audit_v3_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMP=str(scratch), TEMP=str(scratch), TMPDIR=str(scratch),
               OMP_NUM_THREADS='8', OPENBLAS_NUM_THREADS='8', MKL_NUM_THREADS='8', POLARS_MAX_THREADS='8')
    stdout = ROOT / 'analysis/run_logs/round65_limit_up_gain_audit_v3_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/round65_limit_up_gain_audit_v3_20261005.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        child = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(new)],
                                 cwd=ROOT, env=env, stdout=output, stderr=error,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
    receipt = {'status': 'launched_raw_precision_training_validation_gain_attribution',
               'at_local': datetime.datetime.now().isoformat(), 'pid': child.pid,
               'script': str(new), 'stdout': str(stdout), 'stderr': str(stderr),
               'input_sha256': {str(new): sha(new), str(Path(__file__)): sha(__file__)},
               'original_failures_preserved': True, 'new_model_fits': 0,
               'new_quality_scores': 0, 'test_labels_read': False}
    run.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
