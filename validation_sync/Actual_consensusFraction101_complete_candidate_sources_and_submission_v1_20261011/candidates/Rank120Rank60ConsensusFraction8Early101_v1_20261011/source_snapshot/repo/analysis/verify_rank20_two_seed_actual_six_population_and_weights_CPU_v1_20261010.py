"""Verify identical mature annual populations and genuinely different learned tensors for both seeds."""
from pathlib import Path
import sys,hashlib,gc
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def state_sha(state):
    h=hashlib.sha256()
    for key in sorted(state):
        value=state[key].detach().cpu().contiguous().numpy()
        h.update(key.encode());h.update(str(value.shape).encode());h.update(str(value.dtype).encode());h.update(memoryview(value).cast('B'))
    return h.hexdigest()
def main():
    assert allowed()
    import joblib
    banks=[Path(f'E:/赛题五_本机临时/{name}_small512_BF16_bank6_v1_20261010') for name in ('stock_rank20_embedding','stock_rank20seed10_embedding')]
    assert all(read(bank/'verification.json')['actual_native_fits']==6 for bank in banks)
    inputs=[Path(__file__),*[bank/'verification.json' for bank in banks]];records=[]
    for year in range(2020,2026):
        assert allowed();infos=[read(bank/str(year)/'info.json') for bank in banks]
        for key in ('training_matrix_sha256','training_target_sha256','first','last','days','cutoff_exclusive','last_label_end','stock_vocabulary'):
            assert infos[0]['training_meta'][key]==infos[1]['training_meta'][key],(year,key)
        states=[]
        for i,bank in enumerate(banks):
            path=bank/str(year)/'model.joblib';assert sha(path)==infos[i]['model_sha256']
            bundle=joblib.load(path);assert bundle['config']['seed']==(20261009,20261010)[i]
            assert bundle['config']['epochs']==64 and len(bundle['training_losses'])==64
            states.append(state_sha(bundle['state']));del bundle;gc.collect()
            assert sha(path)==infos[i]['model_sha256'];inputs += [path,bank/str(year)/'info.json']
        assert states[0]!=states[1],year
        records.append({'year':year,'mature_training_x_sha256':infos[0]['training_meta']['training_matrix_sha256'],
            'mature_training_y_sha256':infos[0]['training_meta']['training_target_sha256'],'parameter_state_sha256':states,
            'actual_tensor_parameters_differ':True,'own_completed_epochs':[64,64]})
    create(A/'rank20_two_seed_actual_six_population_and_weights_CPU_v1_20261010.json',{
        'status':'passed_actual6_equal_mature_population_and_distinct_learned_tensor_pairs_CPU',
        'input_sha256':{str(p):sha(p) for p in inputs},'records':records,'actual_completed_physical_models':12,
        'new_native_fits_by_this_verifier':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'actual_pairs_checked':6,'both_models_own64':True,'actual_parameter_tensors_differ_all6':True},flush=True)
if __name__=='__main__':main()
