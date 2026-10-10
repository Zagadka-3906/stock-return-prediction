"""Prepare a previously uncovered wide direct-return network; preserve all existing sources."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected162_candidate_sources_v2_20261010 import change
def main():
    sources=['neural_BF16_medium2048_huber010_seed09_e64_native_v1_20261009.py','neural_BF16_medium2048_huber010_seed09_independent_forward_v1_20261009.py','train_neural_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009.py']
    output={}
    for name in sources:
        text=(A/name).read_text(encoding='utf8').replace('huber010','returnhuber050')
        if '_native_' in name:
            text=change(text,"'target': 'y_rank'","'target': 'y_ret_1d'")
            text=change(text,"'loss': 'Huber', 'huber_delta': .1,","'loss': 'Huber', 'huber_delta': .5, 'return_target_scale': 20., 'return_winsor_quantiles': [.005,.995],")
            text=change(text,"    assert cfg['target'] == 'y_rank'","    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed\n    assert allowed()\n    assert cfg['target'] == 'y_ret_1d'")
            text=change(text,"assert cfg['loss']=='Huber' and cfg['huber_delta']==.1","assert cfg['loss']=='Huber' and cfg['huber_delta']==.5 and cfg['return_target_scale']==20. and cfg['return_winsor_quantiles']==[.005,.995]")
            text=change(text,'    target = y.astype(np.float32) - .5','    target,target_bounds=prepare_return_targets(y,cfg)')
            text=change(text,"'target_bounds': [0., 1.], 'target_scale': 1.","'target_bounds': target_bounds, 'target_scale': cfg['return_target_scale']")
            text=change(text,"    return np.concatenate(parts) if parts else np.empty(0, dtype=np.float64)","    assert bundle['target_scale']==CONFIG['return_target_scale']\n    return (np.concatenate(parts) if parts else np.empty(0,dtype=np.float64))/bundle['target_scale']")
            text+='''

def prepare_return_targets(y,cfg):
    import numpy as np
    y=np.asarray(y);assert y.ndim==1 and len(y) and np.isfinite(y).all()
    low,high=np.quantile(y,cfg['return_winsor_quantiles'])
    target=(np.clip(y,low,high)*cfg['return_target_scale']).astype(np.float32)
    return target,[float(low),float(high)]
'''
        elif '_independent_forward_' in name:
            text=change(text,"    return np.concatenate(parts) if parts else np.empty(0, dtype=np.float64)","    assert config['target']=='y_ret_1d' and config['return_target_scale']==20. and bundle['target_scale']==20.\n    return (np.concatenate(parts) if parts else np.empty(0,dtype=np.float64))/20.")
        else:
            text=change(text,".select(KEYS + features + ['y_rank'])",".select(KEYS + features + ['y_ret_1d'])")
            text=change(text,"train['y_rank'].to_numpy()","train['y_ret_1d'].to_numpy()")
            text=change(text,"        cutoff = fold_cutoff(year)","        from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed\n        assert allowed()\n        cutoff = fold_cutoff(year)")
        output[name.replace('huber010','returnhuber050')]=text
    for name,text in output.items():assert not (A/name).exists();compile(text,str(A/name),'exec')
    for name,text in output.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    import neural_BF16_medium2048_returnhuber050_seed09_e64_native_v1_20261009 as native
    evidence=[A/'train_diverse_backbones_20261003.py',A/'train_neural_width_bank_20261004.py',A/'train_neural_tuning_bank_20261004.py',A/'train_neural16384_full_bank_20261005.py']
    create(A/'neural_BF16_medium2048_returnhuber050_seed09_e64_frontier_v1_20261010.json',{'status':'frozen_distinct_wide_direct_return_training_before_any_fit_or_quality','configuration':native.CONFIG,'input_sha256':{str(p):sha(p) for p in [Path(__file__),ROOT/'后续选模标准.md',*[A/n for n in sources],*[A/n for n in output],*evidence]},'coverage_evidence':'Inspected existing return_mlp128 has hidden128/64 and16 epochs; inspected width/tuning/16384 banks are rank targets; this2048/1024/51264epoch BF16 direct-return recipe is distinct','training_target':'Provided mature y_ret_1d; winsor bounds learned only from each prior window; fixed positive scale20; Huber delta0.5 in scaled return units','inference_output':'Native and independent saved-tensor head divided by20 into return units; no future labels or future-derived returns','own_target_formula_gradient_micro_tail_restart_full5_native42_required_before_quality':True,'planned_own_states':list(range(2020,2026)),'actual_native_fits':0,'new_quality_scores':0,'test_labels_read':False,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    print('Compiled distinct wide direct-return Huber recipe; no GPU fit or quality claim',flush=True)
if __name__=='__main__':main()
