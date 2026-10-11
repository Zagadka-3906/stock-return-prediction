"""Finish two undispatched helpers after the v6 factory's preserved launch-name error."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed()
 import prepare_StockRank60Direct200_complete35_pipeline_v6_20261011 as factory
 proof=A/factory.PROOF;d=read(proof)
 for p,h in d['input_sha256'].items():assert sha(p)==h,p
 normal='actual_stock_rank60_direct_embedding35_after199_normalization_queue_v6_20261011'
 row=read(A/'service_owned_workflows_20261006'/normal/'native_launch.json');assert owned(row)
 correction={'status':'actual_sources_admitted_and_existing_normalizer_owned_remaining_two_names_corrected','preserved_v6_factory_dispatch_error':'old retired v1 selected_native14 folder already exists; no new native or future run was launched under that name','compiled_proof_sha256':sha(proof),'input_sha256':{str(p):sha(p) for p in [Path(__file__),A/factory.EXTRAS[1],A/factory.EXTRAS[5],A/'complete200_dependencies_actual_idle_retirement_v6_20261011.json']},'actual_existing_normalizer':row,'new_fits_or_scores':0,'future_qualification_pending':True}
 admission=A/'complete200_actual_v6_remaining_dispatch_admission_v1_20261011.json';create(admission,correction)
 for name,driver in [('StockRank60DirectEmbedding35_selected_native14_v6_20261011',factory.EXTRAS[1]),('StockRank60DirectEmbedding200_complete35_family_v6_20261011',factory.EXTRAS[5])]:
  assert allowed();r=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(admission):sha(admission),str(proof):sha(proof)})
  create(A/(name+'_activation.json'),r)
 print({'actual_complete200_three_current_helpers_owned':True,'no_duplicate_normalization_or_future':True},flush=True)
if __name__=='__main__':main()
