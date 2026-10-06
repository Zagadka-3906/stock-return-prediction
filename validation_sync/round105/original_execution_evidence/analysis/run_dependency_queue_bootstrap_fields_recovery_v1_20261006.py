"""Preserve the whole queue and supply required bootstrap identity fields."""
from pathlib import Path
import inspect
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha


def main():
    import run_dependency_queue_v3_20261006 as previous
    plan=read(Path(sys.argv[1]))
    source=A/'run_dependency_queue_v10_20261006.py'
    assert sha(source)==plan['original_controller_source_sha256']
    main_source=inspect.getsource(previous.main)
    before="    state_path = plan_path.parent / 'state.json'"
    assert main_source.count(before)==1
    main_source=main_source.replace(before,"    state_path = Path(plan['shared_original_state_path'])")
    exec(compile(main_source,str(A/'run_dependency_queue_v11_shared_state_main_20261006.py'),'exec'),vars(previous))
    text=source.read_text(encoding='utf-8')
    before="    run.update(dependency_queue_plan=str(plan_path),"
    after="    run.update(name=job['name'], recovery_driver_sha256=previous.sha(A / 'run_reboot_recovery_attempt_20261006.py'), dependency_queue_plan=str(plan_path),"
    assert text.count(before)==1
    text=text.replace(before,after)
    namespace={'__file__':str(source),'__name__':'actual_complete_dependency_queue_v11'}
    exec(compile(text,str(source),'exec'),namespace)
    original_ready=namespace['ready']
    def serialized_ready(job,jobs):
        if job['gate'].get('quality_slot') and job['name']!='round89':
            for path in plan['complete_ranking_registration_serialization_markers']:
                if not previous.marker(path,['passed']):return False
        return original_ready(job,jobs)
    namespace['ready']=serialized_ready
    namespace['main']()


if __name__=='__main__':main()
