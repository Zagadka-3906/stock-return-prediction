from pathlib import Path
import sys,ast,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed();import prepare_StockRank120Direct201_complete35_pipeline_v7_20261011 as factory
 proof=read(A/factory.PROOF);assert proof['expected_records']==35 and proof['expected_board']==18184
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 paths=[Path(__file__),*factory.source_paths()]
 for name in ('actual_stock_rank120_direct_embedding35_after200_normalization_queue_v7_20261011','StockRank120DirectEmbedding35_selected_native14_v7_20261011','StockRank120DirectEmbedding201_complete35_family_v7_20261011'):
  paths += [A/'service_owned_workflows_20261006'/name/p for p in ('job_definition.json','native_launch.json')]
 template=A/'publish_frozen_Actual183_parent37_and_mixed60_49_sources_main_v1_20261011.py';paths.append(template)
 lines=template.read_text(encoding='utf8').replace('Actual183_parent37_and_mixed60_49_sources','Complete201_actual35_v7_sources').splitlines()
 i=next(i for i,s in enumerate(lines) if s.strip().startswith('paths=[Path(__file__)'));lines[i]='    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]'
 i=next(i for i,s in enumerate(lines) if "payload[(prefix/'manifest.json')" in s)
 manifest={'status':'actual201_source_factory_compiled_and_three_helpers_launched_before_scores_or_future','expected_records':35,'expected_connected_board':18184,'expected_QA':112,'expected_wave':484,'anchors':[183,200],'target_horizon':120,'canonical_optimize_finalize_adapters_included':True,'literal_waits_distinguish_actual_existing_and_predeclared_future_dependencies':True,'new_fits_or_scores_by_publication':0,'actual_native14_candidate_full_board_and_main201_pending':True,'test_labels_read':False}
 lines[i]="    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})"
 i=next(i for i,s in enumerate(lines) if "'commit','-m'" in s);lines[i]="            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','冻结第201轮成熟120日目标完整35项候选流程；规范动态模块入口、实际200父任务及前瞻原生依赖均已检查，科学资格待完成',timeout=180)"
 p=A/'publish_frozen_Complete201_actual35_v7_sources_main_v1_20261011.py';text='\n'.join(lines)+'\n';ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf8');assert allowed();runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
