"""Execute independent sparse native3/full37 controls after mature bank; no scoring."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    preparation=A/'nonflag_SparseGram64_actual_native_and_transform_source_preparation_20261007.json'
    for path,digest in read(preparation)['input_sha256'].items():assert sha(path)==digest,path
    from run_nonflag_residual_SparseGram64_hook3_after_bank_20261007 import main as native
    native()
    from verify_nonflag_residual_SparseGram37_transform_20261007 import main as full
    full()
    nativeproof=A/'nonflag_residual_SparseGram64_native_hook3_preflight_20261007/verification.json'
    fullproof=A/'nonflag_residual_SparseGram37_transform_preflight_20261007/verification.json'
    assert len(read(nativeproof)['records'])==3 and len(read(fullproof)['controls'])==37
    create(A/'nonflag_SparseGram64_actual_native3_full37_cold111_controls_20261007.json',{
      'status':'passed_actual_sparse_native3_full37_independent_CDF_and111_cold_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':{**read(preparation)['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),preparation,nativeproof,fullproof]}},
      'new_native_fits_by_controls':0,'actual_native_fits_in_own_bank':10,'new_quality_scores':0,
      'official_comparison_and_future_candidate_not_claimed':True,'test_labels_read':False})

if __name__=='__main__':main()
