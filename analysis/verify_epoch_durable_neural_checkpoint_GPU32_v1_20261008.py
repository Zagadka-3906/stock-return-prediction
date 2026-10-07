"""Actual fresh-process GPU32 small-network training equivalence and poisoned-input checkpoint rejection."""
from pathlib import Path
from unittest.mock import patch
import argparse,os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
SCRATCH=ROOT/'tmp/epoch_durable_GPU32_v1_20261008'
for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(SCRATCH)
for key in ('TORCH_HOME','TORCHINDUCTOR_CACHE_DIR','TRITON_CACHE_DIR','CUDA_CACHE_PATH'):os.environ[key]=str(SCRATCH/key)
os.environ['CUDA_CACHE_DISABLE']='1'
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=A/'epoch_durable_neural_checkpoint_GPU32_preflight_v1_20261008'
CFG={'kind':'mlp','target':'y_rank','hidden':[128,64],'epochs':32,'batch_size':257,
  'learning_rate':.001,'weight_decay':.0001,'dropout':.05,'seed':20261007}

def inputs():
    import numpy as np
    rng=np.random.default_rng(20261007)
    x=rng.normal(size=(1024,63)).astype(np.float32);x[::7,3]=np.nan
    y=rng.uniform(size=1024).astype(np.float64)
    return x,y

def phase(mode):
    import numpy as np,joblib,torch
    import train_diverse_backbones_20261003 as native
    from epoch_durable_neural_checkpoint_adapter_v2_20261007 import install
    assert torch.cuda.is_available(), 'No real GPU available; no CPU substitution.'
    fit,generated_sha=install(native);x,y=inputs()
    with torch.cuda.device(0):
        if mode=='original':bundle=native.fit_arrays(x,y,CFG);joblib.dump(bundle,OUT/'original32.joblib',compress=3)
        elif mode=='first7':
            record=fit(x,y,CFG,SCRATCH/'checkpoint.joblib',stop_after_epoch=7)
            assert record['next_epoch']==7
            create(OUT/'first7_actual.json',{'status':'saved_completed7_epochs','checkpoint_sha256':sha(SCRATCH/'checkpoint.joblib'),'generated_fit_source_sha256':generated_sha})
        elif mode=='resume32':bundle=fit(x,y,CFG,SCRATCH/'checkpoint.joblib');joblib.dump(bundle,OUT/'resumed32.joblib',compress=3)
        else:raise AssertionError(mode)

def main():
    import subprocess,joblib,numpy as np,torch
    from epoch_durable_neural_checkpoint_adapter_v2_20261007 import install
    import train_diverse_backbones_20261003 as native
    assert torch.cuda.is_available(), 'No real GPU available; no CPU substitution.'
    assert not OUT.exists();OUT.mkdir();SCRATCH.mkdir(parents=True,exist_ok=True)
    paths=[Path(__file__),A/'epoch_durable_neural_checkpoint_adapter_v2_20261007.py',A/'train_diverse_backbones_20261003.py']
    pins={str(p):sha(p) for p in paths}
    create(OUT/'frozen_before_actual_controls.json',{'input_sha256':pins,'configuration':CFG,'test_labels_read':False,'original_wide16384_GPU_equivalence_not_claimed':True})
    from hidden_windows_child_creation_20261006 import install as hidden
    restore=hidden();phases=[]
    try:
        for mode in ('original','first7','resume32'):
            start=time.monotonic()
            result=subprocess.run([sys.executable,'-B','-X','utf8',str(Path(__file__)),'--phase',mode],
              capture_output=True,text=True,encoding='utf8',timeout=300,check=False)
            (OUT/f'{mode}.log').write_text(result.stdout+result.stderr,encoding='utf8',newline='\n')
            assert result.returncode==0, result.stderr
            phases.append({'phase':mode,'elapsed_seconds':time.monotonic()-start,'actual_child_exit':result.returncode})
        original=joblib.load(OUT/'original32.joblib');resumed=joblib.load(OUT/'resumed32.joblib')
        assert original['training_losses']==resumed['training_losses']
        for key in original['state']:assert np.array_equal(original['state'][key].numpy().view('u4'),resumed['state'][key].numpy().view('u4')),key
        for key in ('mean','scale'):assert np.array_equal(original[key].view('u4'),resumed[key].view('u4'))
        x,y=inputs()
        with torch.cuda.device(0):
            before=native.predict_arrays(original,x);after=native.predict_arrays(resumed,x)
            assert np.array_equal(before.view('u8'),after.view('u8'))
            fit,_=install(native);poisoned=x.copy();poisoned[0,0]+=1.;rejected=False
            try:fit(poisoned,y,CFG,SCRATCH/'checkpoint.joblib')
            except AssertionError:rejected=True
            assert rejected
        for p,d in pins.items():assert sha(p)==d,p
        create(OUT/'verification.json',{'status':'passed_actual_fresh_process_GPU32_small_network_epoch7_restart_all_weights_losses_and_predictions_exact',
          'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'phases':phases,
          'actual_original32_vs_separate_process7_plus25_weights_bits_exact':True,
          'actual_all32_training_losses_exact':True,'actual_native_prediction_bits_exact':True,
          'poisoned_training_input_checkpoint_rejected':True,'actual_small_network_GPU_equivalence_verified':True,'GPU_device_name':torch.cuda.get_device_name(0),'original_wide16384_GPU_equivalence_not_claimed':True,
          'running_original16384_fitter_not_replaced':True,'actual_complete_native_annual_fits_added':0,
          'new_quality_scores':0,'test_labels_read':False})
    finally:create(OUT/'actual_hidden_children.json',{'events':restore()})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=('original','first7','resume32'));args=parser.parse_args()
    if args.phase:phase(args.phase)
    else:main()
