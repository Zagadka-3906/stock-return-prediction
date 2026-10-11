"""Extend only fresh quantile codec sources; retain the actual old diagnostic failure."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    failed=A/'service_owned_workflows_20261006/quantile_HGB_codec4_preflight'
    assert not owned(read(failed/'native_launch.json')) and read(failed/'service_execution.json')['status']=='failed'
    old=A/'cpu_conditional_residual_hgb_codec_20261007.py';text=old.read_text(encoding='utf8')
    text=text.replace("('squared_error', 'absolute_error')","('squared_error', 'absolute_error', 'quantile')")
    needle='    assert model.n_trees_per_iteration_ == 1';assert text.count(needle)==1
    text=text.replace(needle,"    probes = np.array([-2., -0., 0., 3.], dtype=np.float64)\n    assert np.array_equal(model._loss.link.inverse(probes).view('u8'), probes.view('u8'))\n    if model.loss == 'quantile':assert np.isfinite(model.quantile) and 0. < model.quantile < 1.\n"+needle)
    text=text.replace("'prediction_link': 'identity', 'baseline':", "'quantile': float(model.quantile) if model.loss == 'quantile' else None,\n        'prediction_link': 'identity', 'baseline':")
    needle="    assert state['fixed_inference_batch'] == BATCH";assert text.count(needle)==1
    text=text.replace(needle,"    if state['loss'] == 'quantile':assert np.isfinite(state['quantile']) and 0. < state['quantile'] < 1.\n"+needle)
    codec=save('quantile_HGB_cpu_codec_v2_20261007.py',text)
    routes={
      'cpu_conditional_residual_hgb_codec_20261007':'quantile_HGB_cpu_codec_v2_20261007',
      'quantile_HGB_codec_preflight_20261007':'quantile_HGB_codec_preflight_v2_20261007',
      'verify_quantile_HGB_codec_preflight_20261007':'verify_quantile_HGB_codec_preflight_v2_20261007',
      'admit_quantile_HGB_native_bank20_20261007':'admit_quantile_HGB_native_bank20_v2_20261007',
      'train_quantile_HGB_native_bank20_20261007':'train_quantile_HGB_native_bank20_v2_20261007',
      'quantile_HGB_native_bank20_admission_20261007':'quantile_HGB_native_bank20_admission_v2_20261007',
      'quantile_HGB_native_bank20_20261007':'quantile_HGB_native_bank20_v2_20261007',
      'quantile_HGB_codec4_preflight':'quantile_HGB_codec4_preflight_v2',
      'quantile_HGB_native_bank20_source_admission':'quantile_HGB_native_bank20_source_admission_v2',
      'quantile_HGB_native_bank20_source_preparation_20261007':'quantile_HGB_native_bank20_source_recovery_preparation_v2_20261007',
    }
    prototypes=[('verify_quantile_HGB_codec_preflight_20261007.py','verify_quantile_HGB_codec_preflight_v2_20261007.py'),
      ('admit_quantile_HGB_native_bank20_20261007.py','admit_quantile_HGB_native_bank20_v2_20261007.py'),
      ('train_quantile_HGB_native_bank20_20261007.py','train_quantile_HGB_native_bank20_v2_20261007.py'),
      ('run_quantile_HGB_native_bank20_after_admission_20261007.py','run_quantile_HGB_native_bank20_after_admission_v2_20261007.py')]
    paths=[Path(__file__),old,codec]
    for old_name,new_name in prototypes:
        old=A/old_name;p=save(new_name,substitute(old.read_text(encoding='utf8'),routes));paths += [old,p]
    create(A/'quantile_HGB_native_bank20_source_recovery_preparation_v2_20261007.json',{'status':'compiled_fresh_quantile_identity_link_codec_and4_diagnostic20_training_routes',
      'input_sha256':{str(p):sha(p) for p in paths},'original_failure':read(failed/'service_execution.json'),
      'original_failed_diagnostic_native_models_saved':len(list((A/'quantile_HGB_codec_preflight_20261007').glob('*.joblib'))),
      'original_failed_selection_bank_fits':0,'new_native_fits_by_source_recovery':0,'new_quality_scores':0})

if __name__=='__main__':main()
