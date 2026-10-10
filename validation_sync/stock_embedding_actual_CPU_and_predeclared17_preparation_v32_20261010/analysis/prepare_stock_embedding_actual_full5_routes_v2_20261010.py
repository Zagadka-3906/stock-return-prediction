"""Correct unlaunched template routes without changing their pinned prototypes."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    prototype=A/'verify_BF16Cross120RecentReturn252Huber050175_independent_small_CPU_v1_20261009.py'
    text=prototype.read_text(encoding='utf8')
    text=text.replace('actual_BF16_medium2048_cross120recent252returnhuber050_seed09_restart_control_v1_20261009','actual_stock_embedding_small512_restart_v1_20261010')
    text=text.replace('actual_BF16_medium2048_cross120recent252returnhuber050_seed09_restart_location_v1_20261009.json','actual_stock_embedding_small512_restart_location_v1_20261010.json')
    text=text.replace('neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_native_v1_20261009','stock_embedding_small512_BF16_native_v1_20261010')
    text=text.replace('neural_BF16_medium2048_cross120recent252returnhuber050_seed09_independent_forward_v1_20261009','stock_embedding_saved_tensor_decoder_v1_20261010')
    text=text.replace('BF16Cross120RecentReturn252Huber050175','StockEmbeddingSmall512')
    text=text.replace('    x[::17, 4] = np.nan;',"    x=np.column_stack((x,rng.integers(0,4651,len(x)).astype(np.float32)))\n    x[::17, 4] = np.nan;")
    small=A/'verify_stock_embedding_small512_small_CPU_v2_20261010.py';assert not small.exists();compile(text,str(small),'exec');small.write_text(text,encoding='utf8',newline='\n')
    prototypefull=A/'verify_stock_embedding_small512_full5_independent_v1_20261010.py'
    text=prototypefull.read_text(encoding='utf8')
    text=text.replace('actual_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_bank6_v1_20261009','actual_stock_embedding_small512_bank6_v1_20261010')
    text=text.replace('[2048, 1024, 512]','[512, 256, 128]').replace("len(bundle['training_losses']) == 64","len(bundle['training_losses']) == 24")
    text=text.replace('verify_StockEmbeddingSmall512_independent_small_CPU_v1_20261009.py','verify_stock_embedding_small512_small_CPU_v2_20261010.py')
    full=A/'verify_stock_embedding_small512_full5_independent_v2_20261010.py';assert not full.exists();compile(text,str(full),'exec');full.write_text(text,encoding='utf8',newline='\n')
    create(A/'stock_embedding_actual_full5_routes_admission_v2_20261010.json',{'status':'compiled_correct_own_small_CPU_and_six_bank_full5_routes','input_sha256':{str(p):sha(p) for p in [Path(__file__),prototype,prototypefull,small,full]},'actual_native_fits':0,'new_quality_scores':0})
if __name__=='__main__':main()
