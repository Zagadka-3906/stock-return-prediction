from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 import numpy as np,torch
 import stock_rank20class25_embedding_small512_BF16_native_v1_20261011 as native
 target=np.asarray([-.495,-.2,0.,.249,.25,.251,.49,.495],dtype=np.float32)
 labels=(target>=np.float32(.25)).astype(np.float64);records=[]
 for shift in (-80.,-3.,-1.,0.,2.,80.):
  logits=np.asarray([shift+.13*i for i in range(len(target))],dtype=np.float32);pt=torch.tensor(logits,requires_grad=True)
  actual=native.binary_rank_loss(pt,torch.tensor(target),native.CONFIG)
  z=logits.astype(np.float64);scalar=np.maximum(z,0.)-z*labels+np.log1p(np.exp(-np.abs(z)));expected=float(np.mean(scalar*np.where(labels==1.,3.,1.)))
  assert abs(actual.item()-expected)<max(1e-6,abs(expected)*2e-7)
  actual.backward();sigmoid=1./(1.+np.exp(-z));gradient=np.where(labels==1.,3.,1.)*(sigmoid-labels)/len(labels)
  assert np.allclose(pt.grad.numpy(),gradient,rtol=2e-6,atol=1e-7) and torch.isfinite(pt.grad).all()
  records.append({'logit_shift':shift,'native_BCE':actual.item(),'independent_FP64_stable_scalar':expected,'independent_gradient_verified':True})
 pointer=A/'actual_stock_rank20_embedding_mature_fixture_location_v1_20261010.json';folder=Path(read(pointer)['output']);v=read(folder/'verification.json');assert v['rows']==49153 and v['last_label_end']<20191231
 y=np.load(folder/'past_rank20_targets.npy');centered,bounds=native.prepare_rank_targets(y,native.CONFIG);binary=(centered>=np.float32(.25))
 assert 0<int(binary.sum())<len(binary) and np.isfinite(centered).all()
 paths=[Path(__file__),Path(native.__file__),pointer,folder/'verification.json',folder/'past_features121.npy',folder/'past_rank20_targets.npy',A/'recent252_rank20_mature_population_actual_CPU_controls_v1_20261010.json']
 for name,d in v['input_sha256'].items():assert sha(name)==d,name
 create(A/'stock_rank20class25_balanced_BCE_actual_CPU_controls_v1_20261011.json',{'status':'passed6_independent_stable_BCE_and_gradient_checks_and49153_mature_label_binary_conversion','records':records,'fixture_rows':len(y),'mature_Top25_positive_rows':int(binary.sum()),'input_sha256':{str(p):sha(p) for p in paths},'raw_rank_threshold':.75,'positive_weight':3.,'new_fits':0,'new_scores':0,'test_labels_read':False})
 print({'actual_BCE_scalar_and_gradient_checks':6,'mature_fixture_rows':len(y),'positive_rows':int(binary.sum())},flush=True)
if __name__=='__main__':main()
