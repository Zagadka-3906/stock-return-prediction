from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys
A=Path(__file__).resolve().parent
sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read
CONTROL=A/'actual_user_cleanup_package134_bounded_authorization_v1_20261011.json'
def allowed():
    controls=[read(A/f'current_user_runtime_control_202610{d}.json') for d in ('10','09')]
    now=datetime.now(timezone(timedelta(hours=8)))
    c=read(CONTROL)
    return c['status']=='active_bounded_cleanup_and_existing_candidate_packaging' and c['actual_user_instruction']=='删除前面没有采用的模型，封装新的更高分方案' and c['new_training_allowed'] is False and c['new_scoring_allowed'] is False and all(x['automatic_restart_enabled'] is False for x in controls) and now>=datetime.fromisoformat(c['at_local'])
def install():
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as gates
    gates.allowed=allowed
    assert allowed()
    return gates
