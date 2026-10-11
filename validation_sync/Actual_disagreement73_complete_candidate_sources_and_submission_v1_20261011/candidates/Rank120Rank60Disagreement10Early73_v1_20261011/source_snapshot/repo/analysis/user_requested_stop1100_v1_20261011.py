"""Use the established owned-process stop at the user's replacement deadline."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent
sys.path[:0]=[str(A.parent),str(A)]
import user_requested_stop2355_v1_20261009 as current
from scheduled_user_pause_20261007 import read,write

def stop(folder,config,journal):
    current.stop_verified(folder,config,journal)
    path=folder/'disk_recovery_manifest.json';record=read(path)
    record['actual_user_shutdown_instruction']='模型优化截止时间更改至10月11日上午11点'
    write(path,record)
    for name in ('current_user_runtime_control_20261008.json','current_user_runtime_control_20261009.json','current_user_runtime_control_20261010.json'):
        path=A/name
        record=read(A/'current_user_runtime_control_20261009.json')
        record.update(actual_user_instruction='模型优化截止时间更改至10月11日上午11点',
                      optimization_deadline_local=config['stop_at_local'])
        write(path,record)

if __name__=='__main__':
    current.core.checkpoint_inventory=current.checkpoint_inventory
    current.core.stop_verified=stop
    current.core.main()
