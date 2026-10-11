from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed();paths=[Path(__file__)]
for name in ['rank120_rank60_consensusFraction8_early101_sources_admission_v2_20261011.json','rank120_rank60_consensusFractionWeight8_early109_sources_admission_v2_20261011.json','actual_idle_fraction103_final_best_only110_admission_v1_20261011.json','actual_idle_fraction101_storage_safe103_controller_admission_v1_20261011.json']:
 p=A/name;paths.append(p);paths.extend(Path(k) for k in read(p)['input_sha256'])
for pattern in ['*TRAIN*98*','*TRAIN*102*','*CSV105*','*cleanup*105*','*TRAIN*103*','*storage*103*','*link103*','*observer151*','*optimization_v151*py','*observer150_idle*','*admitted_fraction100*','*fraction_weight108*','*best_only110*','*fraction100_and_weight108*','*actual8_early114*py','*actual8_96*receipt*','*same_bytes_TRAIN*111*','*storage_safe_controller111*']:
 paths.extend(p for p in A.glob(pattern) if p.is_file())
for name in ['actual_rank120_rank60_after183_consensusFraction8_screen88_v1_20261011','actual_completed_fraction88_namespace_bridge91_v1_20261011','actual_consensusFraction8_results_selection_main89_v1_20261011','actual_rank120_rank60_after183_consensusFraction8_screen100_v1_20261011']:
 f=A/'service_owned_workflows_20261006'/name;paths.extend(f/p for p in ['job_definition.json','service_execution.json','stdout.log','stderr.log'] if (f/p).is_file())
source=A/'publish_namespace_bridges_and_actual_metadata_priority94_sources95_main_v1_20261011.py';s=source.read_text(encoding='utf8');node=next(n for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets));lines=s.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'];s=''.join(lines).replace('namespace_bridges_and_actual_metadata_priority94_sources95','actual_fraction100_weight108_best_only110_CPU_and_cleanup_sources116')
s=s.replace('actual_weight84_completed_only_final_pointer_collision_audited_fraction88_frozen_and_actual_owned192_metadata_writer_interrupted_scores_and_partial_records_preserved','actual_valid_fraction100_complete8_partial88_disallowed05_failure_preserved_actual_same_byte_TRAIN_links_CPU2positive4negative_completed_unused_copies_cleanup_final_weight108_frozen_best_only110_pipeline')
s=s.replace('保存已完成8项权重评分尾部指针冲突的审计桥、6项保护比例方案与实际192榜单写出中断记录；原分数和任务范围保留','保存实际8项保护比例评分、边界拒绝记录、同字节训练数据链接正反检查及历史副本清理证据；冻结最后权重轮和仅最高分完整候选派发')
p=A/'publish_actual_fraction100_weight108_best_only110_CPU_and_cleanup_sources116_main_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');name='actual_fraction100_weight108_best_only110_CPU_cleanup_sources116_main_v1_20261011';r=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r)
