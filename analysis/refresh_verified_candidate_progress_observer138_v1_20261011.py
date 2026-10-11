"""Refresh administrative progress with actual sealed candidate delivery pointers."""
from pathlib import Path
from datetime import datetime
import sys, time, subprocess, psutil
A = Path(__file__).resolve().parent
sys.path[:0] = [str(A.parent), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    assert allowed()
    original = A / 'monitor_verified_current_optimization_v136_20261011.py'
    target = A / 'monitor_verified_current_optimization_v138_20261011.py'
    text = original.read_text(encoding='utf-8').replace('import read,owned', 'import read,owned,sha')
    needle = "  state={'at_local':now.isoformat()"
    assert text.count(needle) == 1
    insertion = '''  sealed_candidates=[]
  for pointer in sorted(A.glob('alternate_verified_*submission_delivery_v1_20261011.json')):
   value=read(pointer)
   if value.get('all_full_native_independent_reload_csv_and_cold80_checks_passed') and value.get('actual_main_commit') and Path(value['output']).is_dir():
    sealed_candidates.append({'pointer':str(pointer),'pointer_sha256':sha(pointer),'delivery':value})
  sealed_candidates.sort(key=lambda r:(-r['delivery']['official_TRAIN_internal_score'],r['delivery']['models'],r['delivery']['csv_sha256']))
  best_sealed=sealed_candidates[0] if sealed_candidates else None
'''
    text = text.replace(needle, insertion + needle)
    needle = "  write(A/'optimization_live_progress_v136_20261011.json',state);"
    assert text.count(needle) == 1
    text = text.replace(needle, "  state.update({'native_verified_main_published_candidates':sealed_candidates,'highest_native_verified_main_published_candidate':best_sealed,'pending_cached_highest_native_candidate_verified':bool(best_sealed and best_sealed['delivery']['official_TRAIN_internal_score']>=pending_highest),'full_connected_board_qualification_is_separate':True})\n" + needle)
    needle = "  lines += [f'{tag}：{row}' for tag,row in science.items()]"
    assert text.count(needle) == 1
    text = text.replace(needle, "  if best_sealed:\n   lines.append(f\"已完成原生/独立复算/冷启动/main及交付的最高候选：S={best_sealed['delivery']['official_TRAIN_internal_score']}；{best_sealed['delivery']['output']}。完整关联总榜登记仍单独推进。\")\n" + needle)
    text = text.replace('更高缓存分数尚待提交核验。', '完整关联总榜资格以登记记录为准。')
    text = text.replace('v136_20261011', 'v138_20261011').replace('v273_20261011', 'v276_20261011').replace("+'.136.tmp'", "+'.138.tmp'")
    compile(text, str(target), 'exec')
    assert not target.exists()
    target.write_text(text, encoding='utf-8', newline='\n')
    old_folder=A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v136_20261011'
    old=read(old_folder/'native_launch.json')
    assert owned(old)
    proof=A/'actual_observer138_verified_candidate_delivery_reporting_admission_v1_20261011.json'
    identity=start_service('actual_fast_optimization_progress_reboot_v138_20261011', target.name, [], {str(target):sha(target),str(original):sha(original)})
    snapshot=A/'optimization_live_progress_v138_20261011.json'
    for _ in range(30):
        if snapshot.exists():break
        time.sleep(1)
    assert snapshot.exists()
    state=read(snapshot)
    assert state['highest_native_verified_main_published_candidate']['delivery']['actual_main_commit']=='1f1e7770389e97cee3e4767cd5d35122144ce369'
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    dump=subprocess.run([str(spy),'dump','--pid',str(old['owned_worker_pid'])],capture_output=True,text=True,encoding='utf-8',check=True).stdout
    assert '(idle)' in dump and 'monitor_verified_current_optimization_v136_20261011.py' in dump
    assert owned(old)
    worker=psutil.Process(old['owned_worker_pid'])
    assert not worker.children(recursive=True)
    worker.terminate()
    create(proof, {'status':'passed_actual138_correct_sealed_candidate_reporting_snapshot', 'at_local':datetime.now().isoformat(), 'new':identity,'old':old,'old_actual_idle_dump':dump,'input_sha256':{str(original):sha(original),str(target):sha(target)},'scientific_workers_terminated':0,'new_scientific_scores_claimed':0,'highest_candidate_full_connected_board_still_pending':True})
    print({'observer':138,'actual_highest_sealed_candidate_S':state['highest_native_verified_main_published_candidate']['delivery']['official_TRAIN_internal_score'],'scientific_workers_terminated':0},flush=True)

if __name__=='__main__':main()
