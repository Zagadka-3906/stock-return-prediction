"""Preserve the metadata-only publication failure; fix the exact existing bank launch path in fresh versions."""
from pathlib import Path
import ast,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    failed=A/'service_owned_workflows_20261006/HuberIRLS64_causal_and_handoff_main_publication_v2_20261008'
    assert not owned(read(failed/'native_launch.json')) and read(failed/'service_execution.json')['status']=='failed'
    actual=A/'actual_nonflag_HuberIRLS64_bank10_hidden_launch_v1_20261008.json';assert actual.exists()
    old_record=A/'record_actual_optimization_handoff_v6_20261008.py';text=old_record.read_text(encoding='utf8')
    text=text.replace('actual_HuberIRLS64_bank10_hidden_launch_v1_20261008','actual_nonflag_HuberIRLS64_bank10_hidden_launch_v1_20261008')
    text=text.replace('actual_optimization_handoff_v6_20261008','actual_optimization_handoff_v7_20261008').replace('交接 v6','交接 v7').replace('handoff6','handoff7')
    new_record=A/'record_actual_optimization_handoff_v7_20261008.py';assert not new_record.exists();compile(text,str(new_record),'exec')
    # Check every explicitly declared input path, excluding the output paths outside this list.
    tree=ast.parse(text);source_list=next(node.value for node in ast.walk(tree) if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='sources' for target in node.targets))
    checked=[]
    for value in source_list.elts:
        if isinstance(value,ast.BinOp) and isinstance(value.left,ast.Name) and value.left.id=='A' and isinstance(value.right,ast.Constant):
            path=A/value.right.value;assert path.exists(),path;checked.append(str(path))
    new_record.write_text(text,encoding='utf8',newline='\n')
    old_publisher=A/'publish_HuberIRLS64_causal_and_handoff_v2_20261008.py';text=old_publisher.read_text(encoding='utf8')
    text=text.replace('record_actual_optimization_handoff_v6_20261008','record_actual_optimization_handoff_v7_20261008')
    text=text.replace('actual_optimization_handoff_v6_20261008','actual_optimization_handoff_v7_20261008')
    text=text.replace('HuberIRLS64_causal_handoff_main_v2_20261008','HuberIRLS64_causal_handoff_main_v3_20261008')
    text=text.replace('validation_sync/HuberIRLS64_causal_handoff_v2_20261008','validation_sync/HuberIRLS64_causal_handoff_v3_20261008')
    needle='    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources};'
    assert text.count(needle)==1
    text=text.replace(needle,"""    sources += [A/'HuberIRLS64_bounded_plan_recheck_v2_20261008.json',
        A/'recover_HuberIRLS64_handoff_path_publication_v3_20261008.py',A/'HuberIRLS64_handoff_path_recovery_v3_20261008.json',
        A/'record_actual_optimization_handoff_v5_20261008.py',A/'record_actual_optimization_handoff_v6_20261008.py',
        A/'publish_HuberIRLS64_causal_and_handoff_v1_20261008.py',A/'publish_HuberIRLS64_causal_and_handoff_v2_20261008.py']
    for suffix in ('v1','v2'):
        failed=A/'service_owned_workflows_20261006'/('HuberIRLS64_causal_and_handoff_main_publication_'+suffix+'_20261008')
        sources += list(failed.glob('*.json'))+list(failed.glob('*.log'))
"""+needle)
    new_publisher=A/'publish_HuberIRLS64_causal_and_handoff_v3_20261008.py';assert not new_publisher.exists()
    compile(text,str(new_publisher),'exec');new_publisher.write_text(text,encoding='utf8',newline='\n')
    create(A/'HuberIRLS64_handoff_path_recovery_v3_20261008.json',{
        'status':'fresh_metadata_writer7_and_publisher3_existing16_input_paths_checked',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'checked_static_input_paths':checked,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old_record,old_publisher,actual,failed/'service_execution.json']},
        'generated_source_sha256':{str(p):sha(p) for p in (new_record,new_publisher)},
        'all_scientific_models_controls_scores_and_live_GPU_work_unchanged':True,'all_original_failures_preserved':True})
    pins={str(p):sha(p) for p in (Path(__file__),new_record,new_publisher)}
    row=start('HuberIRLS64_causal_and_handoff_main_publication_v3_20261008',new_publisher.name,[],pins)
    create(A/'actual_HuberIRLS64_causal_handoff_publication_hidden_launch_v3_20261008.json',{
        'status':'started_fresh_metadata_path_repaired_publication_of_actual_causal_controls','identity':row,'input_sha256':pins,
        'actual_quality_scores':0,'goal_remains_active':True})


if __name__=='__main__':main()
