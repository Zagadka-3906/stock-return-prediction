from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
paths=[Path(__file__)]
for name in ['actual_ancestor_guard83_future_scope_admission_v1_20261011.json','actual_weight84_and_remaining45_scope_admission_v1_20261011.json','rank120_rank60_consensusWeight8_early85_sources_admission_v2_20261011.json','rank120_rank60_consensus8_early81_sources_admission_v2_20261011.json']:
 p=A/name;paths.append(p);paths.extend(Path(k) for k in read(p)['input_sha256'])
for pattern in ['*ancestor_index_guard83*','*cleanup*79*','*cleanup*82*','*handoff*v310*','*consensus81*CPU*','*consensus8_pointwise_CPU*','*consensus8_gain_decision81*','*consensus8*main_receipt*','*consensusWeight85*CPU*','*consensusWeight8_predeclared*','*consensusWeight8_screen84*py','*conditional_weight85*','*remaining45*84*','*final_consensus_weight8*','*consensus8_science_priority80*']:
 paths.extend(p for p in A.glob(pattern) if p.is_file())
paths.extend(Path('E:/赛题五_本机临时/已发布祖先索引安全同步83_20261011').glob('*/verification.json'))
paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
source=A/'publish_actual_disagreement10_score_priority72_observer148_sources_main_v1_20261011.py';s=source.read_text(encoding='utf8')
node=next(n for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets));lines=s.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'];s=''.join(lines)
s=s.replace('actual_disagreement10_score_priority72_observer148_sources','actual83_guard85_weights_and_completed_cleanup_sources86')
s=s.replace('actual_owned_idle_administrative_queue_only_replaced_original191_and_raw10_scientific_workers_preserved_raw10_and_if_gain_full_native_candidate_prioritized_before_original48_future_records','actual_guard83_positive_private_negative_CPU_checks_cleanup79_82_and_frozen_weight84_85_sources_original_remaining45_scope_preserved')
s=s.replace("'actual_disagreement10_scores_pending': True","'weight84_actual_scores_and_full_candidate_completion_claimed_only_in_separate_receipts': True")
s=s.replace('冻结10项跨时长预测分歧评分优先队列与实际监控148；保留正在运行191和原48项任务，提分后完整候选核验仍必要','保存实际索引保护正反对照、弃用缓存清理记录与六项新增一致性权重及条件完整候选方案；保留原45项后续任务')
p=A/'publish_actual83_guard85_weights_and_completed_cleanup_sources86_main_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
name='actual83_guard85_weights_and_completed_cleanup_sources86_main_v1_20261011';r=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r)
