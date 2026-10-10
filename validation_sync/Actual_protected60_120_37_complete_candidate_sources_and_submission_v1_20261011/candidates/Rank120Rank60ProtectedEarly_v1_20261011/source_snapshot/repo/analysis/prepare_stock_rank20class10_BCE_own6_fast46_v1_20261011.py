"""Fresh mature20d Top10 classification objective; no reused trained weights."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def renamed(s):return s.replace('stock_rank20tail4','stock_rank20class10').replace('StockRank20Tail4','StockRank20Class10').replace('rank20tail4','rank20class10').replace('Rank20Tail4','Rank20Class10').replace('STOCK_RANK20TAIL4','STOCK_RANK20CLASS10')
def main():
 assert allowed();inputs=[];outputs=[]
 def save(name,s):
  p=A/name;assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');outputs.append(p);return p
 p=A/'stock_rank20tail4_embedding_small512_BF16_native_v1_20261011.py';inputs.append(p);s=renamed(p.read_text(encoding='utf8'))
 s=s.replace("'loss': 'Huber'","'loss': 'BCEWithLogits'").replace("cfg['loss']=='Huber'","cfg['loss']=='BCEWithLogits'")
 old="'loss_weighting': 'label_rank_upper15_linear_tail4', 'tail_rank_threshold': .85, 'tail_rank_extra_weight': 4.,";assert old in s
 s=s.replace(old,"'loss_weighting': 'balanced_mature_rank20_top10_binary', 'classification_raw_rank_threshold': .9, 'positive_class_weight': 9.,")
 start=s.index('def weighted_rank_huber(');s=s[:start]+'''def binary_rank_loss(pred,target,cfg):
    import torch
    assert pred.ndim==target.ndim==1 and pred.shape==target.shape
    assert cfg['loss']=='BCEWithLogits' and cfg['loss_weighting']=='balanced_mature_rank20_top10_binary'
    assert cfg['classification_raw_rank_threshold']==.9 and cfg['positive_class_weight']==9.
    labels=(target.float()>=.4).float()
    return torch.nn.functional.binary_cross_entropy_with_logits(pred.float(),labels,pos_weight=pred.new_tensor(9.,dtype=torch.float32))
'''
 s=s.replace('weighted_rank_huber(pred.float(), yt[part], cfg)','binary_rank_loss(pred.float(), yt[part], cfg)')
 native=save(renamed(p.name),s)
 p=A/'stock_rank20tail4_embedding_saved_tensor_decoder_v1_20261011.py';inputs.append(p);decoder=save(renamed(p.name),renamed(p.read_text(encoding='utf8')))
 cpu=save('verify_stock_rank20class10_balanced_BCE_actual_CPU_v1_20261011.py','''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 import numpy as np,torch
 import stock_rank20class10_embedding_small512_BF16_native_v1_20261011 as native
 target=np.asarray([-.495,-.2,0.,.399,.4,.401,.49,.495],dtype=np.float32)
 labels=(target>=np.float32(.4)).astype(np.float64);records=[]
 for shift in (-80.,-3.,-1.,0.,2.,80.):
  logits=np.asarray([shift+.13*i for i in range(len(target))],dtype=np.float32);pt=torch.tensor(logits,requires_grad=True)
  actual=native.binary_rank_loss(pt,torch.tensor(target),native.CONFIG)
  z=logits.astype(np.float64);scalar=np.maximum(z,0.)-z*labels+np.log1p(np.exp(-np.abs(z)));expected=float(np.mean(scalar*np.where(labels==1.,9.,1.)))
  assert abs(actual.item()-expected)<max(1e-6,abs(expected)*2e-7)
  actual.backward();sigmoid=1./(1.+np.exp(-z));gradient=np.where(labels==1.,9.,1.)*(sigmoid-labels)/len(labels)
  assert np.allclose(pt.grad.numpy(),gradient,rtol=2e-6,atol=1e-7) and torch.isfinite(pt.grad).all()
  records.append({'logit_shift':shift,'native_BCE':actual.item(),'independent_FP64_stable_scalar':expected,'independent_gradient_verified':True})
 pointer=A/'actual_stock_rank20_embedding_mature_fixture_location_v1_20261010.json';folder=Path(read(pointer)['output']);v=read(folder/'verification.json');assert v['rows']==49153 and v['last_label_end']<20191231
 y=np.load(folder/'past_rank20_targets.npy');centered,bounds=native.prepare_rank_targets(y,native.CONFIG);binary=(centered>=np.float32(.4))
 assert 0<int(binary.sum())<len(binary) and np.isfinite(centered).all()
 paths=[Path(__file__),Path(native.__file__),pointer,folder/'verification.json',folder/'past_features121.npy',folder/'past_rank20_targets.npy',A/'recent252_rank20_mature_population_actual_CPU_controls_v1_20261010.json']
 for name,d in v['input_sha256'].items():assert sha(name)==d,name
 create(A/'stock_rank20class10_balanced_BCE_actual_CPU_controls_v1_20261011.json',{'status':'passed6_independent_stable_BCE_and_gradient_checks_and49153_mature_label_binary_conversion','records':records,'fixture_rows':len(y),'mature_Top10_positive_rows':int(binary.sum()),'input_sha256':{str(p):sha(p) for p in paths},'raw_rank_threshold':.9,'positive_weight':9.,'new_fits':0,'new_scores':0,'test_labels_read':False})
 print({'actual_BCE_scalar_and_gradient_checks':6,'mature_fixture_rows':len(y),'positive_rows':int(binary.sum())},flush=True)
if __name__=='__main__':main()
''')
 fixture=save('verify_rank20class10_reused_actual_mature_fixture_gate_v1_20261011.py',renamed((A/'verify_rank20tail4_reused_actual_mature_fixture_gate_v1_20261011.py').read_text(encoding='utf8')).replace('weighted_Huber','balanced_BCE').replace('upper_tail_weighted_rows','mature_Top10_positive_rows').replace('weighted_loss6','binary_BCE_gradient6'))
 mapping={'verify_stock_rank20tail4_embedding_small512_restart_v2_20261011.py':'verify_stock_rank20class10_embedding_small512_restart_v1_20261011.py','verify_stock_rank20tail4_embedding_small512_small_CPU_v2_20261011.py':'verify_stock_rank20class10_embedding_small512_small_CPU_v1_20261011.py','train_stock_rank20tail4_embedding_small512_BF16_bank6_own64_v2_20261011.py':'train_stock_rank20class10_embedding_small512_BF16_bank6_own64_v1_20261011.py','verify_stock_rank20tail4_embedding_small512_full5_independent_v1_20261011.py':'verify_stock_rank20class10_embedding_small512_full5_independent_v1_20261011.py'}
 for old,new in mapping.items():
  p=A/old;inputs.append(p);s=renamed(p.read_text(encoding='utf8')).replace('small512_restart_v2_20261011','small512_restart_v1_20261011');save(new,s)
 module=importlib.import_module(native.stem)
 assert module.CONFIG['loss']=='BCEWithLogits' and module.CONFIG['label_horizon_trading_days']==20
 pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]}
 for name in ['stock_rank20class10_own64_native_sources_preparation_v1_20261011.json','stock_rank20class10_embedding_own64_native_sources_preparation_v1_20261011.json']:
  create(A/name,{'status':'compiled_fresh_mature20_top10_binary_objective_before_any_fit','configuration':module.CONFIG,'input_sha256':pins,'new_fits':0,'new_scores':0,'fresh_weights_required':True,'provided_mature_rank20_population_reused_unchanged':True,'test_labels_read':False})
 queue=save('run_stock_rank20class10_BCE_own6_full5_fast_queue_v1_20261011.py',"""from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('actual_stock_rank20tail4_embedding_six_state_native42_v1_20261011')
 for name,driver in [('actual_stock_rank20class10_balanced_BCE_CPU_v1_20261011','verify_stock_rank20class10_balanced_BCE_actual_CPU_v1_20261011.py'),('StockRank20Class10Embedding_actual_mature_fixture_CPU_v1_20261011','verify_rank20class10_reused_actual_mature_fixture_gate_v1_20261011.py'),('actual_stock_rank20class10_embedding_small512_restart_v1_20261011','verify_stock_rank20class10_embedding_small512_restart_v1_20261011.py'),('StockRank20Class10EmbeddingSmall512_independent_small_CPU_v1_20261011','verify_stock_rank20class10_embedding_small512_small_CPU_v1_20261011.py'),('actual_stock_rank20class10_embedding_small512_bank6_v1_20261011','train_stock_rank20class10_embedding_small512_BF16_bank6_own64_v1_20261011.py'),('StockRank20Class10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','verify_stock_rank20class10_embedding_small512_full5_independent_v1_20261011.py')]:
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r);closed(name)
if __name__=='__main__':main()
""")
 proof=A/'stock_rank20class10_BCE_own6_sources_admission_v1_20261011.json';create(proof,{'status':'compiled_BCE_scalar_controls_fixture_reuse_restart_own6_full5_queue_before_training','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'new_fits':0,'new_scores':0,'raw_rank_label_horizon':20,'classification_Top_fraction':.1,'target_source_only_mature_training_labels':True,'test_labels_read':False})
 assert allowed();r=start_service('actual_stock_rank20class10_BCE_own6_full5_queue_v1_20261011',queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)});create(A/'actual_stock_rank20class10_BCE_own6_full5_queue_activation_v1_20261011.json',r)
 print({'new_mature20_Top10_BCE_fresh_training_queue_dispatched':True,'GPU_fits_pending_CPU_checks':True},flush=True)
if __name__=='__main__':main()
