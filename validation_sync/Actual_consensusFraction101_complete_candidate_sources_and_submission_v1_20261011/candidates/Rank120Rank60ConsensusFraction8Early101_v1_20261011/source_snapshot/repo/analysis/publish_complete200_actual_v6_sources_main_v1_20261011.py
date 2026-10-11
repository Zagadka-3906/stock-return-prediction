"""Publish the actual35 source admission and corrected live200 helper identities."""
from pathlib import Path
import sys,runpy,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 import prepare_StockRank60Direct200_complete35_pipeline_v6_20261011 as factory
 proof=read(A/factory.PROOF);assert proof['expected_records']==35 and proof['expected_board']==18149
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 paths=[Path(__file__),*factory.source_paths(),A/'repair_complete200_dependencies_before_future_v6_20261011.py',A/'complete200_dependencies_actual_idle_retirement_v6_20261011.json',A/'finish_complete200_actual_v6_partial_dispatch_v1_20261011.py',A/'complete200_actual_v6_remaining_dispatch_admission_v1_20261011.json']
 for name in ('actual_stock_rank60_direct_embedding35_after199_normalization_queue_v6_20261011','StockRank60DirectEmbedding35_selected_native14_v6_20261011','StockRank60DirectEmbedding200_complete35_family_v6_20261011'):
  paths += [A/'service_owned_workflows_20261006'/name/p for p in ('job_definition.json','native_launch.json')]
 template=A/'publish_frozen_Actual183_parent37_and_mixed60_49_sources_main_v1_20261011.py';paths.append(template)
 text=template.read_text(encoding='utf8').replace('Actual183_parent37_and_mixed60_49_sources','Complete200_actual35_v6_sources')
 lines=text.splitlines();i=next(i for i,s in enumerate(lines) if s.strip().startswith('paths=[Path(__file__)'))
 lines[i]='    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]'
 i=next(i for i,s in enumerate(lines) if "payload[(prefix/'manifest.json')" in s)
 manifest={'status':'actual200_complete35_sources_compiled_and_three_corrected_helpers_owned_before_scientific_completion','expected_records':35,'expected_connected_board':18149,'expected_QA':111,'anchors':[183,199],'parent_callback_CPU_cases':12,'compiled_literal_wait_gates_checked':True,'v5_idle_helpers_retired_only_before_any_native_or_future_execution':True,'v6_partial_dispatch_error_preserved_and_remaining_two_helpers_actually_dispatched':True,'new_fits_or_scores_by_publication':0,'selected_native14_future_and_main200_pending':True,'test_labels_read':False}
 lines[i]="    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})"
 i=next(i for i,s in enumerate(lines) if "'commit','-m'" in s);lines[i]="            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','第200轮纯60日完整35项流程：实际原生依赖与候选等待任务名核验修复；评分与推理资格待完成',timeout=180)"
 p=A/'publish_frozen_Complete200_actual35_v6_sources_main_v1_20261011.py';text='\n'.join(lines)+'\n';ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf8');assert allowed();runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
