"""Publish actual12 parent CPU controls and predeclared33 sources, not scores."""
from pathlib import Path
import sys,runpy,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 proofpath=A/'stock_rank60_after183_direct33_predeclared_sources_v1_20261011.json';proof=read(proofpath)
 cpu_path=A/'stock_rank60_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json';cpu=read(cpu_path)
 assert len(proof['cases'])==33 and len(cpu['records'])==12
 paths=[Path(__file__),proofpath,cpu_path,A/'actual_stock_rank60_after183_direct33_activation_v1_20261011.json',A/'actual_rank60_after183_completed33_main_activation_v1_20261011.json',A/'run_publish_rank60_after183_completed33_main_v1_20261011.py']
 for p,d in {**proof['input_sha256'],**cpu['input_sha256']}.items():assert sha(p)==d,p;paths.append(Path(p))
 template=A/'publish_frozen_Actual183_parent37_and_mixed60_49_sources_main_v1_20261011.py';paths.append(template)
 text=template.read_text(encoding='utf8').replace('Actual183_parent37_and_mixed60_49_sources','Rank60_direct33_actual12_CPU_predeclared_sources')
 lines=text.splitlines();i=next(i for i,s in enumerate(lines) if s.strip().startswith('paths=[Path(__file__)'))
 lines[i]='    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]'
 i=next(i for i,s in enumerate(lines) if "payload[(prefix/'manifest.json')" in s)
 manifest={'status':'actual12_complete_parent_CPU_callback_controls_and_frozen33_pure_H60_after183_hypotheses_before_scores','actual_parent_CPU_checks':12,'expected_official_records':33,'parent_round':183,'horizon':60,'new_fits_or_scores_by_publication':0,'score_and_selected_native14_and_future_qualification_pending':True,'test_labels_read':False}
 lines[i]="    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})"
 i=next(i for i,s in enumerate(lines) if "'commit','-m'" in s);lines[i]="            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','纯60日信号对完整183方案的33项大小权重及保护顶部排序预声明；12项实际父回调CPU通过',timeout=180)"
 p=A/'publish_frozen_Rank60_direct33_actual12_CPU_predeclared_main_v1_20261011.py';text='\n'.join(lines)+'\n';ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf8');assert allowed();runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
