"""Preserve whole source-relative registration paths and validate every alias before writing."""
from pathlib import Path
import ast
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def write_new(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec')
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    return p

def main():
    old_name='protected_upper_pool_HGB66_round115_full_registration_v2'
    old=A/'service_owned_workflows_20261006'/old_name
    assert not owned(read(old/'native_launch.json')) and read(old/'service_execution.json')['status']=='failed'
    source=A/'register_protected_upper_pool_HGB66_round115_artifacts_v2_20261007.py'
    text=source.read_text(encoding='utf8')
    text=text.replace("target = CANDIDATE / 'registration_sources' / source.name","target = CANDIDATE / 'registration_sources' / 'round115_full_scope' / source.relative_to(ROOT)")
    before='        os.link(source, target)';assert text.count(before)==1
    text=text.replace(before,'        if target.exists():\n            assert sha(target)==sha(source),target\n        else:\n            os.link(source, target)')
    needle='    for relative, info in manifest[\'files\'].items():\n'
    idx=text.index('    for relative in manifest[\'files\']:\n')
    proofcode="""    # Resolve the complete alias map before touching even one file.
    targets = {}
    for relative in manifest['files']:
        alias = 'source_registration_selection.json' if relative == 'selection.json' else relative
        targets[str(CANDIDATE / alias)] = str(SOURCE_CANDIDATE / relative)
    for source in sources:
        target = CANDIDATE / 'registration_sources' / 'round115_full_scope' / source.relative_to(ROOT)
        if str(target) in targets:assert sha(targets[str(target)])==sha(source)
        targets[str(target)] = str(source)
    for target,source in targets.items():
        assert Path(target).resolve().is_relative_to(CANDIDATE.resolve())
        if Path(target).exists():assert sha(target)==sha(source),target
    create(A/'protected_upper_pool_HGB66_round115_complete_alias_map_controls_v3_20261007.json',
        {'status':'passed_full_source_and_inherited_alias_target_map_before_writes',
         'targets':len(targets),'existing_targets_exact':sum(Path(p).exists() for p in targets),
         'original_failed_flattened_files_retained':True,'new_quality_scores':0})
"""
    text=text[:idx]+proofcode+text[idx:]
    text=text.replace("    sources += [A/'prepare_local115_alias_and116_dependency_recovery_20261007.py'", "    sources += [A/'prepare_local115_alias_namespace_recovery_v3_20261007.py', A/'run_protected_upper_pool_HGB66_round115_full_registration_v3_20261007.py', *list((A/'service_owned_workflows_20261006/protected_upper_pool_HGB66_round115_full_registration_v2').glob('*.json')), A/'service_owned_workflows_20261006/protected_upper_pool_HGB66_round115_full_registration_v2/stderr.log', A/'prepare_local115_alias_and116_dependency_recovery_20261007.py'")
    reg=write_new('register_protected_upper_pool_HGB66_round115_artifacts_v3_20261007.py',text)
    source_runtime=A/'run_protected_upper_pool_HGB66_round115_full_registration_v2_20261007.py'
    text=source_runtime.read_text(encoding='utf8').replace('protected_upper_pool_HGB66_round115_actual_registration_v2_20261007','protected_upper_pool_HGB66_round115_actual_registration_v3_20261007')
    text=text.replace('register_protected_upper_pool_HGB66_round115_artifacts_v2_20261007','register_protected_upper_pool_HGB66_round115_artifacts_v3_20261007')
    runtime=write_new('run_protected_upper_pool_HGB66_round115_full_registration_v3_20261007.py',text)
    pins={str(p):sha(p) for p in (Path(__file__),source,reg,source_runtime,runtime,old/'service_execution.json',old/'stderr.log')}
    row=start_service('protected_upper_pool_HGB66_round115_full_registration_v3',runtime.name,[],pins)
    create(A/'protected_upper_pool_HGB66_round115_namespace_recovery_actual_launch_v3_20261007.json',{'input_sha256':pins,'actual_native_launch':row,'new_training_or_scores':0,'old_failures_and_partial_exact_aliases_retained':True})
    print({'status':'launched_full115_namespace_recovery','pid':row['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
