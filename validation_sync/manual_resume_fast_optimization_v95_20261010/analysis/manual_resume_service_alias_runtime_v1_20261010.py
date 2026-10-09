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
    args=parser.parse_args()
    control=queue.read(A/'current_user_runtime_control_20261009.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume'
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    driver=Path(args.driver).resolve();assert driver.is_relative_to(A)
    aliases=queue.read(args.aliases)['service_aliases']
    original_read=queue.read
    def read(path):
        path=Path(path)
        if path.name in ('native_launch.json','service_execution.json') and path.parent.parent==A/'service_owned_workflows_20261006':
            name=aliases.get(path.parent.name)
            if name:path=path.parent.parent/name/path.name
        return original_read(path)
    queue.read=read
    for name in args.wait_for:
        folder=A/'service_owned_workflows_20261006'/name
        actual=folder.parent/aliases.get(name,name)
        while not (actual/'native_launch.json').exists() or queue.owned(read(folder/'native_launch.json')):
            time.sleep(5)
        assert read(folder/'service_execution.json')['status']=='passed',name
    for p,d in queue.read(args.aliases)['original_driver_sha256'].items():assert queue.sha(p)==d,p
    sys.argv=[str(driver)]
    runpy.run_path(str(driver),run_name='__main__')

if __name__=='__main__':main()
