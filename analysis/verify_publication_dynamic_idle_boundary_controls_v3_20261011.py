from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
import owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 as subject
import handoff_joint_goss_round97_full_execution_20261006 as h
saved=(h.pair,h.stack,subject.original_hold,subject.time.sleep);results=[]
idle='    main (watch_validations_main_v7_20261006.py:71)';guard='guarded (watch_validations_main_safe_v11_20261010.py:24)';waiting='acquire (serial_main_publication_mutex_v1_20261009.py:19)\n'+guard
class Fake:
 def __init__(self,name,events):self.pid=17;self.name=name;self.events=events
 def suspend(self):self.events.append('suspend_'+self.name)
 def resume(self):self.events.append('resume_'+self.name)
 def children(self):return []
try:
 for case,stacks,expected in [('unchanged_idle',[idle,idle],idle),('busy_then_mutex_wait',['active_Git_not_idle',waiting,waiting],guard),('idle_race_moves_to_mutex',[idle,'active_Git_not_idle',waiting,waiting],guard)]:
  events=[];parent=Fake('parent',events);worker=Fake('worker',events);queue=list(stacks)
  h.pair=lambda row:(parent,worker);h.stack=lambda pid:queue.pop(0);subject.original_hold=lambda identity,needle,_original:_original(identity,needle);subject.time.sleep=lambda seconds:None
  p,w,evidence=subject.hold({'CPU_fixture_only':True},idle)
  assert p is parent and w is worker and evidence['actual_boundary']==expected and not queue
  assert events[-2:]==['suspend_worker','suspend_parent']
  if case=='idle_race_moves_to_mutex':assert events[:4]==['suspend_worker','suspend_parent','resume_parent','resume_worker']
  results.append({'case':case,'events':events,'actual_selected_fixture_boundary':expected,'real_process_suspended':False})
finally:
 h.pair,h.stack,subject.original_hold,subject.time.sleep=saved
assert (h.pair,h.stack,subject.original_hold,subject.time.sleep)==saved
create(A/'publication_dynamic_idle_boundary_actual_CPU_controls_v3_20261011.json',{'status':'passed_three_actual_helper_expression_CPU_fixtures_idle_mutex_transition_race_and_all_binding_restoration','input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(subject.__file__),A/'owned_idle_publication_wait_reboot_identity_v2_20261011.py']},'records':results,'real_processes_suspended':0,'new_fits_or_scores':0})
print({'actual_CPU_boundary_controls':3,'real_processes_stopped':0},flush=True)
