from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
 assert allowed();closed('recovery61_MixedObjectiveWindow189_complete149_family_v3_20261011')
 proof=A/'verified_idle_future_single_dispatch63_admission_v1_20261011.json';data=read(proof)
 for name,driver in data['tasks']:
  assert allowed();p=A/data['driver_wrappers'][driver]
  identity=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)})
  create(A/(name+'_activation.json'),identity);closed(name)
 print('All actual54 future stages completed; full objective audit still required',flush=True)
if __name__=='__main__':main()
