from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('actual_stock_rank20class10_balanced_BCE_CPU_v1_20261011')
 pointer=A/'actual_stock_rank20_embedding_mature_fixture_location_v1_20261010.json';folder=Path(read(pointer)['output']);p=folder/'verification.json';v=read(p)
 assert sha(p)==read(pointer)['verification_sha256'] and v['rows']==49153 and v['last_label_end']<20191231
 for name,d in v['input_sha256'].items():assert sha(name)==d,name
 weights=A/'stock_rank20class10_balanced_BCE_actual_CPU_controls_v1_20261011.json';w=read(weights)
 assert len(w['records'])==6 and w['fixture_rows']==49153 and w['mature_Top10_positive_rows']>0
 for name,d in w['input_sha256'].items():assert sha(name)==d,name
 paths=[Path(__file__),pointer,p,folder/'past_features121.npy',folder/'past_rank20_targets.npy',weights]
 create(A/'rank20class10_actual_reused_fixture_gate_v1_20261011.json',{'status':'passed_actual_rehashed49153_original_mature_rank20_features_targets_and_new_independent_binary_BCE_gradient6_CPU_controls','input_sha256':{str(p):sha(p) for p in paths},'new_feature_derivation_or_native_fit_claimed':False,'actual_fixture_reuse_for_new_loss':True,'original_mature_fixture_preserved':True,'test_labels_read':False})
if __name__=='__main__':main()
