from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
paths=[Path(__file__)]
for name in ['rank120_rank60_consensusFraction8_early89_sources_admission_v2_20261011.json','actual_namespace_safe_catalog5_admission_v1_20261011.json']:
 p=A/name;paths.append(p);paths.extend(Path(k) for k in read(p)['input_sha256'])
for pattern in ['*namespace*90*','*namespace*recovery90*','*weight85*90*activation*','*fraction89*92*activation*','*fraction88*91*activation*','*fraction88_conditional89*','*Fraction89*CPU*','*Fraction8_predeclared*','*Fraction8_screen88*py','*observer150*','*optimization_v150*py','*observer149_idle_retired*','*priority94*','*interruption94*','*watcher94*','*interruption_for_score_priority94*','*memory_release94*','*catalog5*','*catalog_v5*py']:
 paths.extend(p for p in A.glob(pattern) if p.is_file())
for name in ['actual_rank120_rank60_after183_consensusWeight8_screen84_v1_20261011','actual_consensusWeight8_results_selection_main85_v1_20261011','actual_completed_weight84_namespace_bridge90_v1_20261011','recovery58_StockRank10Embedding192_round192_full_registration_v1_20261011']:
 f=A/'service_owned_workflows_20261006'/name
 paths.extend(f/p for p in ['job_definition.json','service_execution.json','observation_interruption.json'] if (f/p).is_file())
source=A/'publish_actual83_guard85_weights_and_completed_cleanup_sources86_main_v1_20261011.py';s=source.read_text(encoding='utf8');node=next(n for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets));lines=s.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'];s=''.join(lines)
s=s.replace('actual83_guard85_weights_and_completed_cleanup_sources86','namespace_bridges_and_actual_metadata_priority94_sources95')
s=s.replace('actual_guard83_positive_private_negative_CPU_checks_cleanup79_82_and_frozen_weight84_85_sources_original_remaining45_scope_preserved','actual_weight84_completed_only_final_pointer_collision_audited_fraction88_frozen_and_actual_owned192_metadata_writer_interrupted_scores_and_partial_records_preserved')
s=s.replace('保存实际索引保护正反对照、弃用缓存清理记录与六项新增一致性权重及条件完整候选方案；保留原45项后续任务','保存已完成8项权重评分尾部指针冲突的审计桥、6项保护比例方案与实际192榜单写出中断记录；原分数和任务范围保留')
p=A/'publish_namespace_bridges_and_actual_metadata_priority94_sources95_main_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');name='actual_namespace_bridges_and_metadata_priority94_sources95_main_v1_20261011';r=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r)
