"""Freeze a genuinely new stock/numeric interaction recipe without editing old sources."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def once(text,old,new):
    assert text.count(old)==1,(old,text.count(old));return text.replace(old,new)
def save(name,text):
    path=A/name;assert not path.exists(),path;compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return path
def main():
    assert allowed();generated=[]
    original=A/'neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_native_v1_20261009.py'
    text=original.read_text(encoding='utf8')
    text=text.replace('import train_diverse_backbones_20261003 as architecture','import stock_identity_embedding_network_v1_20261010 as architecture')
    text=once(text,"'hidden': [2048, 1024, 512]","'hidden': [512, 256, 128]")
    text=once(text,"'epochs': 64","'epochs': 24")
    text=once(text,"'encoded_feature_count':120","'encoded_feature_count':121,'numeric_feature_count':120,'stock_embedding_dim':16,'stock_vocabulary_size':4651")
    oldrecipe='own_mature_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_weighted_accum_v1_20261009'
    newrecipe='own_mature_stock_embedding16_cross120_return1d_recent252_small512_BF16_e24_v1_20261010'
    text=once(text,oldrecipe,newrecipe)
    text=once(text,"cfg['encoded_feature_count']==120","cfg['encoded_feature_count']==121\n    architecture.validate_ids(x)")
    text=once(text,'    target,target_bounds=prepare_return_targets(y,cfg)',"    mean[-1]=0.;scale[-1]=1.;clean[:,-1]=x[:,-1]\n    target,target_bounds=prepare_return_targets(y,cfg)")
    text=once(text,"    assert bundle['config']['recipe'] == CONFIG['recipe']","    assert bundle['config']['recipe'] == CONFIG['recipe']\n    architecture.validate_ids(x)")
    text=once(text,'            if len(clean) < batch:',"            clean[:,-1]=raw[:,-1]\n            if len(clean) < batch:")
    nativepath=save('stock_embedding_small512_BF16_native_v1_20261010.py',text);generated.append(nativepath)
    native=importlib.import_module(nativepath.stem)
    assert native.CONFIG['epochs']==24 and native.CONFIG['encoded_feature_count']==121
    original_bank=A/'train_neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_bank6_v1_20261009.py'
    bank=original_bank.read_text(encoding='utf8')
    bank=bank.replace('neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_native_v1_20261009','stock_embedding_small512_BF16_native_v1_20261010')
    bank=bank.replace('neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_bank6_v1_20261009','stock_embedding_small512_BF16_bank6_v1_20261010')
    bank=bank.replace('actual_BF16_medium2048_cross120recent252returnhuber050_seed09_restart_control_v1_20261009','actual_stock_embedding_small512_restart_v1_20261010')
    bank=bank.replace('actual_BF16_medium2048_cross120recent252returnhuber050_seed09_restart_location_v1_20261009.json','actual_stock_embedding_small512_restart_location_v1_20261010.json')
    bank=bank.replace('actual_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_bank6_location_v1_20261009.json','actual_stock_embedding_small512_bank6_location_v1_20261010.json')
    bank=once(bank,'        y = train[\'y_ret_1d\'].to_numpy()',"        vocabulary=sorted(set(train['ts_code'].to_list()))\n        x=native.architecture.attach(x,train['ts_code'].to_list(),vocabulary)\n        y = train['y_ret_1d'].to_numpy()")
    bank=once(bank,"'features': encoded_features, 'raw_features':features","'stock_vocabulary':vocabulary,'vocabulary_fitted_only_mature_training_rows':True,'features': encoded_features, 'raw_features':features")
    bank=once(bank,"        joblib.dump(bundle, folder / 'model.joblib', compress=0)","        bundle['stock_vocabulary']=vocabulary\n        joblib.dump(bundle, folder / 'model.joblib', compress=0)")
    bank=once(bank,'            raw = native.predict_arrays(bundle, vx)',"            vx=native.architecture.attach(vx,valid['ts_code'].to_list(),vocabulary)\n            raw = native.predict_arrays(bundle, vx)")
    bank=bank.replace('64 fixed epochs','24 fixed epochs')
    bankpath=save('train_stock_embedding_small512_BF16_bank6_v1_20261010.py',bank);generated.append(bankpath)
    original_restart=A/'verify_neural_BF16_medium2048_cross120recent252returnhuber050_seed09_restart_v1_20261009.py'
    restart=original_restart.read_text(encoding='utf8')
    restart=restart.replace('neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_native_v1_20261009','stock_embedding_small512_BF16_native_v1_20261010')
    restart=restart.replace('BF16_medium2048_cross120recent252returnhuber050_seed09_restart_v1','stock_embedding_small512_restart_v1_20261010')
    restart=restart.replace('actual_BF16_medium2048_cross120recent252returnhuber050_seed09_restart_location_v1_20261009.json','actual_stock_embedding_small512_restart_location_v1_20261010.json')
    restart=once(restart,'        return x, np.clip',"        x=np.column_stack((x,rng.integers(0,4651,len(x)).astype(np.float32)))\n        return x, np.clip")
    restart=once(restart,"    return np.load(fixture/'past_features.npy'),np.load(fixture/'past_return_targets.npy')", "    embedding=Path(read(A/'actual_stock_embedding_mature_fixture_location_v1_20261010.json')['output'])\n    return np.load(embedding/'past_features121.npy'),np.load(fixture/'past_return_targets.npy')")
    restart=once(restart,"    paths += [fixture/'past_features.npy'", "    embedding=Path(read(A/'actual_stock_embedding_mature_fixture_location_v1_20261010.json')['output'])\n    paths += [embedding/'past_features121.npy',embedding/'verification.json',A/'stock_embedding_saved_tensor_decoder_v1_20261010.py',fixture/'past_features.npy'")
    restart=once(restart,'            cold = []','            cold = []') if '            cold = []' in restart else restart
    restart=once(restart,'            assert np.array_equal(before.view(\'u8\'), after.view(\'u8\'))',"            from stock_embedding_saved_tensor_decoder_v1_20261010 import predict_saved_tensors\n            decoded=predict_saved_tensors(resumed,sample,device='cuda')\n            assert np.array_equal(decoded.view('u8'),after.view('u8'))\n            assert np.array_equal(before.view('u8'), after.view('u8'))")
    restartpath=save('verify_stock_embedding_small512_restart_v1_20261010.py',restart);generated.append(restartpath)
    original_full=A/'verify_BF16Cross120RecentReturn252Huber050175_full5_independent_GPU_v1_20261009.py'
    full=original_full.read_text(encoding='utf8')
    full=full.replace('neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_native_v1_20261009','stock_embedding_small512_BF16_native_v1_20261010')
    full=full.replace('neural_BF16_medium2048_cross120recent252returnhuber050_seed09_independent_forward_v1_20261009','stock_embedding_saved_tensor_decoder_v1_20261010')
    full=full.replace('neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_bank6_v1_20261009','stock_embedding_small512_BF16_bank6_v1_20261010')
    full=full.replace('actual_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_bank6_location_v1_20261009.json','actual_stock_embedding_small512_bank6_location_v1_20261010.json')
    full=full.replace('BF16Cross120RecentReturn252Huber050175','StockEmbeddingSmall512')
    full=full.replace("info['configuration']['epochs'] == 64","info['configuration']['epochs'] == 24")
    full=once(full,"        expected = observed['pred_raw'].to_numpy()","        import stock_identity_embedding_network_v1_20261010 as embedding\n        assert meta['stock_vocabulary']==bundle['stock_vocabulary'] and meta['vocabulary_fitted_only_mature_training_rows']\n        x=embedding.attach(x,frame['ts_code'].to_list(),bundle['stock_vocabulary'])\n        expected = observed['pred_raw'].to_numpy()")
    fullpath=save('verify_stock_embedding_small512_full5_independent_v1_20261010.py',full);generated.append(fullpath)
    paths=[Path(__file__),original,original_bank,original_restart,original_full,*generated,A/'stock_identity_embedding_network_v1_20261010.py',A/'stock_embedding_saved_tensor_decoder_v1_20261010.py']
    create(A/'stock_embedding_small512_sources_admission_v1_20261010.json',{'status':'compiled_new_stock_embedding_recipe_and_fresh_own_controls_training_sources','input_sha256':{str(p):sha(p) for p in paths},'configuration':native.CONFIG,'actual_native_fits':0,'new_quality_scores':0,'test_labels_read':False,'actual_GPU_controls_and_quality_pending':True})
    print({'fresh_sources':len(generated),'recipe':native.CONFIG},flush=True)
if __name__=='__main__':main()
