"""Read exact owned workflow states and selected stack without altering workers."""
from pathlib import Path
import sys,json,psutil,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned

def main():
    names=['nonflag_EmpiricalBayes40_round130_full_registration_v1','nonflag_RidgeMicro40_actual131_after130_dependency_queue',
      'nonflag_RidgeMicro40_round131_full_registration_v1','nonflag_ReverseBayes40_actual132_after131_dependency_queue_v2',
      'actual_sparse_and_isolated_scoring_controls_main_publication','neural16384_annual']
    result={'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'available_RAM_GiB':psutil.virtual_memory().available/2**30,'services':{}}
    for name in names:
        f=A/'service_owned_workflows_20261006'/name
        if not (f/'native_launch.json').is_file():result['services'][name]={'not_launched':True};continue
        row=read(f/'native_launch.json');live=owned(row)
        item={'owned_live':live,'actual_execution':read(f/'service_execution.json') if (f/'service_execution.json').is_file() else None}
        if live:
            p=psutil.Process(row['owned_worker_pid']);item.update(pid=p.pid,RSS_GiB=p.memory_info().rss/2**30,cpu_seconds=sum(p.cpu_times()[:2]),status=p.status())
            if '--stack' in sys.argv and name in names[:1]:
                from handoff_joint_goss_round97_full_execution_20261006 import stack
                lines=stack(p.pid).splitlines();item['current_stack_tail']=lines[-10:]
        result['services'][name]=item
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
