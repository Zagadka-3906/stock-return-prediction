from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();proof=A/'high_gain_science_priority_after_actual190_admission_v1_20261011.json';data=read(proof)
 closed(data['live190_family_preserved'])
 for name in data['high_gain_science_gates']:
  assert allowed();closed(name)
 routing=A/'verified_future_byte_exact64_admission_v1_20261011.json';sources=read(routing)
 for name,original in data['remaining_original_tasks']:
  assert allowed();p=A/sources['driver_wrappers'][original]
  i=start_service(name,p.name,[],{str(p):sha(p),str(routing):sha(routing),str(proof):sha(proof)})
  create(A/(name+'_activation.json'),i);closed(name)
 print('All remaining original51 full-board stages complete after high-gain science; goal audit still required',flush=True)
if __name__=='__main__':main()
