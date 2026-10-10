from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed()
    closed('StockTop10Embedding175_selected_candidate_sealing_recovery_v2_20261010')
    closed('actual_stock_pairrank_embedding_six_state_native42_v1_20261010')
    proof=A/'stock_pairrank_embedding_own32_controls46_sources_admission_v1_20261010.json'
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    for name,driver in [('actual_stock_pairrank_embedding_after174_fast17_screen_v1_20261010', 'run_stock_pairrank_embedding_after174_fast17_screen_v1_20261010.py'), ('actual_stock_pairrank_embedding_after174_large_allocation29_screen_v1_20261010', 'run_stock_pairrank_embedding_after174_large_allocation29_screen_v1_20261010.py')]:
        assert allowed();p=A/driver
        row=start_service(name,driver,[],{str(p):sha(p),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),row)
        while owned(row):
            assert allowed();time.sleep(15)
        assert read(A/'service_owned_workflows_20261006'/name/'service_execution.json')['status']=='passed',name
if __name__=='__main__':main()
