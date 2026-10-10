"""Freeze only real source/proof bytes for the pending 199 pipeline, main only."""
from pathlib import Path
import sys, ast, re
A=Path(__file__).resolve().parent
sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
 assert allowed()
 proofpath=A/'rank60_rank20_mixed199_full_execution_sources_admission_v1_20261011.json'
 proof=read(proofpath)
 assert proof['expected_records']==51 and proof['expected_board']==18114
 for p,d in proof['input_sha256'].items(): assert sha(p)==d,p
 import prepare_Rank60Rank20Mixed199_complete51_pipeline_v1_20261011 as factory
 paths=list(dict.fromkeys([Path(__file__),proofpath,*factory.source_paths(),A/'compress_new_completed_main_browser_profiles_v3_20261011.py']))
 for name in ('actual_rank60_rank20_mixed51_after198_normalization_v1_20261011','actual_rank60_rank20_mixed51_selected_native14_v1_20261011','Rank60Rank20Mixed199_complete51_family_v4_20261011'):
  for filename in ('job_definition.json','native_launch.json'):
   paths.append(A/'service_owned_workflows_20261006'/name/filename)
  driver=Path(read(A/'service_owned_workflows_20261006'/name/'job_definition.json')['driver']);paths.append(driver)
 assert all(p.is_file() for p in paths)
 prefix='Complete199_actual51_sources_v1_20261011'
 template=(A/'publish_frozen_Actual183_parent37_and_mixed60_49_sources_main_v1_20261011.py').read_text(encoding='utf8')
 template=template.replace('Actual183_parent37_and_mixed60_49_sources',prefix)
 lines=template.splitlines()
 i=next(i for i,s in enumerate(lines) if s.strip().startswith('paths=[Path(__file__)'))
 lines[i]='    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]'
 i=next(i for i,s in enumerate(lines) if "payload[(prefix/'manifest.json')" in s)
 manifest={'status':'actual199_source_factory_compiled_and_three_queues_launched_before_scientific_completion','expected_official_records':51,'expected_connected_board':18114,'anchors':[183,198],'horizons':[20,60],'new_fits_by_publication':0,'new_scores_by_publication':0,'native14_and_future_and_main_round199_pending':True,'test_labels_read':False}
 lines[i]="    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})"
 i=next(i for i,s in enumerate(lines) if "'commit','-m'" in s)
 lines[i]="            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','冻结第199轮20/60日混合完整51项流程源码及真实队列凭据；评分与候选资格仍待完成',timeout=180)"
 target=A/'publish_frozen_Complete199_actual51_sources_v1_20261011.py'
 text='\n'.join(lines)+'\n';ast.parse(text)
 assert not target.exists();target.write_text(text,encoding='utf8')
 pins={str(p):sha(p) for p in dict.fromkeys([*paths,target])}
 create(A/'complete199_actual_sources_main_preparation_v1_20261011.json',{'status':'passed_rehashed_actual_factory_and_sources_before_main_publication','input_sha256':pins,'actual_future_qualification_not_claimed':True})
 from start_fast_completed_owned_service_v1_20261011 import start_service
 assert allowed();row=start_service('actual_complete199_sources_main_v1_20261011',target.name,[],pins)
 create(A/'actual_complete199_sources_main_activation_v1_20261011.json',row)
 print({'frozen_actual_sources':len(pins),'publication_queued_main_only':True},flush=True)
if __name__=='__main__':main()
