"""Publish actual new120 CPU evidence and frozen sources, never unfinished fits as done."""
from pathlib import Path
import sys,ast,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 import prepare_stock_rank120_mature_own6_and_direct33_v1_20261011 as factory
 proof=read(A/'stock_rank120_new120_pipeline_admission_v1_20261011.json');assert proof['actual_CPU_cases']==31
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 paths=[Path(__file__),*factory.source_paths()]
 for name in ('actual_stock_rank120_own6_full5_native42_direct33_queue_v1_20261011','actual_rank120_after183_completed33_main_v1_20261011'):
  paths += [A/'service_owned_workflows_20261006'/name/p for p in ('job_definition.json','native_launch.json')]
 template=A/'publish_frozen_Actual183_parent37_and_mixed60_49_sources_main_v1_20261011.py';paths.append(template)
 lines=template.read_text(encoding='utf8').replace('Actual183_parent37_and_mixed60_49_sources','Rank120_actual31_CPU_frozen_sources').splitlines()
 i=next(i for i,s in enumerate(lines) if s.strip().startswith('paths=[Path(__file__)'));lines[i]='    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]'
 i=next(i for i,s in enumerate(lines) if "payload[(prefix/'manifest.json')" in s)
 manifest={'status':'actual31_new120_independent_CPU_cases_passed_before_training_and_official_scores','actual_label_maturity_and_gap_CPU_cases':19,'actual_complete183_parent_callback_CPU_cases':12,'label_horizon':120,'origin_window':'last252 past calendar origins before strict120 maturity filtering; not252 mature origins','expected_own_annual_fits':6,'expected_TRAIN_full_replay_years':5,'expected_native_and_cold_cases':42,'expected_direct183_official_records':33,'new_fits_or_scores_by_publication':0,'actual_fits_and_native_and_future_qualification_pending':True,'test_labels_read':False}
 lines[i]="    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})"
 i=next(i for i,s in enumerate(lines) if "'commit','-m'" in s);lines[i]="            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','新增成熟120日目标：19项标签时间与缺口检查、12项完整183回调检查通过；六年度训练与官方验证待完成',timeout=180)"
 p=A/'publish_frozen_Rank120_actual31_CPU_sources_main_v1_20261011.py';text='\n'.join(lines)+'\n';ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf8');assert allowed();runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
