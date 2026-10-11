from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();inputs=[];outputs=[]
 def save(name,text):
  p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');outputs.append(p);return p
 def renamed(text):
  text=text.replace('stock_rank20_embedding','stock_rank20tail4_embedding').replace('StockRank20Embedding','StockRank20Tail4Embedding')
  return re.sub(r'[A-Za-z0-9_]*(?:stock_rank20tail4|StockRank20Tail4)[A-Za-z0-9_]*',lambda m:m.group().replace('20261010','20261011').replace('20261009','20261011'),text)
 native_source=A/'stock_rank20_embedding_small512_BF16_native_v1_20261010.py';inputs.append(native_source);text=renamed(native_source.read_text(encoding='utf8'))
 needle="          'recipe':";assert needle in text;text=text.replace(needle,"          'loss_weighting': 'label_rank_upper15_linear_tail4', 'tail_rank_threshold': .85, 'tail_rank_extra_weight': 4.,\n"+needle,1)
 old="torch.nn.functional.huber_loss(pred.float(), yt[part], delta=cfg['huber_delta'])";assert text.count(old)==1;text=text.replace(old,"weighted_rank_huber(pred.float(), yt[part], cfg)")
 text += '''
def weighted_rank_huber(pred,target,cfg):
    import torch
    assert pred.ndim==target.ndim==1 and pred.shape==target.shape
    assert cfg['loss_weighting']=='label_rank_upper15_linear_tail4'
    assert cfg['tail_rank_threshold']==.85 and cfg['tail_rank_extra_weight'] in (0.,4.)
    weights=1.+cfg['tail_rank_extra_weight']*torch.clamp((target.float()-.35)/.15,0.,1.)
    loss=torch.nn.functional.huber_loss(pred.float(),target.float(),delta=cfg['huber_delta'],reduction='none')
    return (weights*loss).mean()
'''
 native=save('stock_rank20tail4_embedding_small512_BF16_native_v1_20261011.py',text)
 decoder_source=A/'stock_rank20_embedding_saved_tensor_decoder_v1_20261010.py';inputs.append(decoder_source);decoder=save('stock_rank20tail4_embedding_saved_tensor_decoder_v1_20261011.py',renamed(decoder_source.read_text(encoding='utf8')))
 verifier=save('verify_stock_rank20tail4_weighted_Huber_actual_CPU_v1_20261011.py', '''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 import numpy as np,torch
 import stock_rank20tail4_embedding_small512_BF16_native_v1_20261011 as native
 cases=[]
 target=np.asarray([-.4999,-.3,0.,.349,.35,.365,.4,.425,.45,.495,.5],dtype=np.float32)
 for amplitude in (0.,.07,.21):
  pred=(target+amplitude).astype(np.float32)
  for extra in (0.,4.):
   cfg={**native.CONFIG,'tail_rank_extra_weight':extra}
   pt=torch.tensor(pred,requires_grad=True);yt=torch.tensor(target)
   actual=native.weighted_rank_huber(pt,yt,cfg)
   errors=np.abs(pred.astype(np.float64)-target.astype(np.float64));base=np.where(errors<=.1,.5*errors**2,.1*(errors-.05))
   weights=np.asarray([1.+extra*min(1.,max(0.,(float(y)-.35)/.15)) for y in target])
   expected=float(np.mean(weights*base));assert abs(actual.item()-expected)<1e-7
   if not extra:assert actual.item()==torch.nn.functional.huber_loss(pt,yt,delta=.1).item()
   actual.backward();assert torch.isfinite(pt.grad).all()
   cases.append({'amplitude':amplitude,'extra_weight':extra,'native':actual.item(),'independent_FP64_scalar':expected,'gradients_finite':True})
 assert weights.min()>=1. and weights.max()<=5.
 # Reuse the actual independently verified20-day mature fixture, without changing labels or reading future labels.
 pointer=A/'actual_stock_rank20_embedding_mature_fixture_location_v1_20261010.json';folder=Path(read(pointer)['output']);proof=read(folder/'verification.json')
 assert proof['last_label_end']<20191231
 y=np.load(folder/'past_rank20_targets.npy');centered,bounds=native.prepare_rank_targets(y,native.CONFIG)
 assert len(y)==49153 and np.isfinite(centered).all() and (centered>=-.5).all() and (centered<=.5).all()
 w=1.+4.*np.clip((centered-.35)/.15,0.,1.);assert w.min()>=1. and w.max()<=5. and (w>1.).any()
 create(A/'stock_rank20tail4_weighted_Huber_actual_CPU_controls_v1_20261011.json',{'status':'passed6_independent_scalar_weighted_Huber_controls_and_actual49153_rank20_mature_target_weights','records':cases,'fixture_rows':len(y),'upper_tail_weighted_rows':int((w>1.).sum()),'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(native.__file__),pointer,folder/'verification.json',folder/'past_rank20_targets.npy',A/'recent252_rank20_mature_population_actual_CPU_controls_v1_20261010.json']},'new_fits':0,'new_scores':0,'future_X_read':False,'test_labels_read':False})
 print({'actual_scalar_loss_checks':6,'actual_mature_rows':len(y),'new_fits':0},flush=True)
if __name__=='__main__':main()
''')
 module=importlib.import_module(native.stem)
 create(A/'stock_rank20tail4_own64_native_sources_preparation_v1_20261011.json',{'status':'compiled_prospective_upper15_rank_label_weighted_new_loss_not_old_bank_weights','configuration':module.CONFIG,'input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'new_fits':0,'new_scores':0,'own_rank20_maturity_and_targets_reused_unchanged':True,'training_tail_weight':{'threshold_raw_rank':.85,'maximum_weight':5.,'target_weight_only_from_mature_training_labels':True},'gpu_restart_and_own6_pending':True})
 r=start_service('actual_stock_rank20tail4_weighted_Huber_CPU_v1_20261011',verifier.name,[],{str(verifier):sha(verifier)});create(A/'actual_stock_rank20tail4_weighted_Huber_CPU_activation_v1_20261011.json',r)
 print({'new_upper15_tail4_loss_CPU_dispatched':True,'new_native_fits':0},flush=True)
if __name__=='__main__':main()
