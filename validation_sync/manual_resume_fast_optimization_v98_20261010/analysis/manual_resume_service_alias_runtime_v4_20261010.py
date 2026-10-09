"""Resume unchanged scientific drivers under fresh service identities, with explicit dependency aliases."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import argparse, runpy, sys, time
A=Path(__file__).resolve().parent
ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
import run_dependency_queue_v3_20261006 as queue

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--driver',required=True)
    parser.add_argument('--aliases',required=True,type=Path)
    parser.add_argument('--wait-for',action='append',default=[])
    parser.add_argument('--argument',action='append',default=[])
    args=parser.parse_args()
    control=queue.read(A/'current_user_runtime_control_20261009.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume'
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    driver=Path(args.driver).resolve();assert driver.is_relative_to(A)
    aliases=queue.read(args.aliases)['service_aliases']
    original_read=queue.read
    original_exists=Path.exists
    def redirected(path):
        path=Path(path)
        if path.name in ('native_launch.json','service_execution.json') and path.parent.parent==A/'service_owned_workflows_20261006':
            name=aliases.get(path.parent.name)
            if path.parent.name=='main_publisher_v10_20261009':name='main_publisher_v11_20261010'
            if name:path=path.parent.parent/name/path.name
        return path
    def read(path):return original_read(redirected(path))
    queue.read=read
    Path.exists=lambda path: original_exists(redirected(path))
    # Newly dispatched scoring/publishing receivers need the same explicit aliases.
    import start_nonflag_RFF128Low76_actual_admission_v4_20261007 as launches
    from handoff_ready_goss_full_execution_20261006 import start_service
    def start(name,filename,arguments,pins):
        child=A/filename
        child_args=['--driver',str(child),'--aliases',str(args.aliases)]
        child_args+=['--argument='+str(value) for value in arguments]
        extra={str(Path(__file__)):queue.sha(__file__),str(args.aliases):queue.sha(args.aliases),str(child):queue.sha(child)}
        try:return start_service(name,Path(__file__).name,child_args,{**pins,**extra})
        except AssertionError:
            folder=A/'service_owned_workflows_20261006'/name
            row=original_read(folder/'native_launch.json')
            assert not queue.owned(row) and original_read(folder/'service_execution.json')['status']=='passed'
            return row
    launches.start=start
    for name in args.wait_for:
        folder=A/'service_owned_workflows_20261006'/name
        actual=folder.parent/aliases.get(name,name)
        while not (actual/'native_launch.json').exists() or not (folder/'service_execution.json').exists() or queue.owned(read(folder/'native_launch.json')):
            time.sleep(5)
        assert read(folder/'service_execution.json')['status']=='passed',name
    for p,d in queue.read(args.aliases)['original_driver_sha256'].items():assert queue.sha(p)==d,p
    sys.argv=[str(driver),*args.argument]
    runpy.run_path(str(driver),run_name='__main__')

if __name__=='__main__':main()
