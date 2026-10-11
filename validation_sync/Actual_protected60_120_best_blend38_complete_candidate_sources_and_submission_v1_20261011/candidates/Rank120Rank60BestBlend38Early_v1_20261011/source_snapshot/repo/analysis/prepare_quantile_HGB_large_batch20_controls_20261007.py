"""Prepare a fresh8192 quantile codec and real20-model equivalence benchmark."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    old=A/'quantile_HGB_cpu_codec_v2_20261007.py';text=old.read_text(encoding='utf8')
    text=text.replace('BATCH, fit_preprocessing, prepare, predict_native','BATCH, fit_preprocessing, prepare')
    text=text.replace('\n\ndef export(', '\n\nRUNTIME_BATCH = 8192\n\ndef export(')
    before=text.index('def predict_decoded');prefix=text[:before];decoder=text[before:]
    decoder=decoder.replace('range(0, len(x), BATCH)','range(0, len(x), RUNTIME_BATCH)').replace('min(BATCH, len(x) - left)','min(RUNTIME_BATCH, len(x) - left)')
    decoder=decoder.replace('(BATCH, x.shape[1])','(RUNTIME_BATCH, x.shape[1])').replace('np.full(BATCH,','np.full(RUNTIME_BATCH,').replace('np.zeros(BATCH,','np.zeros(RUNTIME_BATCH,')
    large=A/'cpu_numerical_HGB_large_batch_codec_v2_20261007.py';native=large.read_text(encoding='utf8').split('def predict_native',1)[1]
    native='def predict_native'+native.replace("('squared_error', 'absolute_error')","('squared_error', 'absolute_error', 'quantile')")
    codec=A/'quantile_HGB_large_batch_codec_20261007.py';assert not codec.exists();text=prefix+decoder+'\n\n'+native;compile(text,str(codec),'exec');codec.write_text(text,encoding='utf8',newline='\n')
    prototype=A/'benchmark_cpu_HGB_large_batch20_20261007.py'
    routes={
      'cpu_conditional_residual_hgb_codec_20261007':'quantile_HGB_cpu_codec_v2_20261007',
      'cpu_numerical_HGB_large_batch_codec_v2_20261007':'quantile_HGB_large_batch_codec_20261007',
      'cpu_HGB_large_batch20_benchmark_20261007':'quantile_HGB_large_batch20_benchmark_20261007',
      'cpu_conditional_residual_hgb_bank20_20261007':'quantile_HGB_native_bank20_v2_20261007',
      'passed_actual20_CPU_conditional_HGB_native_independent_numpy_and_prefix_controls':'passed_actual20_CPU_quantile_HGB_native_independent_numpy_and_prefix_controls',
      'cpu_conditional_residual_hgb_native_bank20':'quantile_HGB_native_bank20_training_v2'}
    text=substitute(prototype.read_text(encoding='utf8'),routes)
    target=A/'benchmark_quantile_HGB_large_batch20_20261007.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'quantile_HGB_large_batch20_source_preparation_20261007.json',{'status':'compiled_quantile8192_native_and_independent20_model_two_order_full_validation_benchmark',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,large,codec,prototype,target]},'new_native_fits':0,'new_quality_scores':0})

if __name__=='__main__':main()
