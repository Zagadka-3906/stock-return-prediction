"""Publish completed acceleration controls and fixed-case native probes on main."""
from pathlib import Path
import sys, ast, runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def main():
    assert allowed()
    for n in ['actual_shared_live_ranking_report180_reader_controls_v1_20261011',
      'actual_shared_live_ranking_report_scope_controls_v1_20261011',
      'actual_stock_rank60_fixed_leading_case17_native14_v2_20261011']:closed(n)
    location=A/'actual_stock_rank60_fixed_leading_case17_native14_location_v2_20261011.json'
    folder=Path(read(location)['output']); proof=read(folder/'verification.json')
    assert proof['status']=='passed_fixed_case17_six_states14_native_and14_cold_and7_prefit_rejections'
    assert len(proof['records'])==14 and len(proof['prefit_rejections'])==7
    controls=[A/'shared_live_ranking_report_actual180_controls_v1_20261011.json',A/'shared_live_ranking_report_scope_controls_v1_20261011.json']
    for obj in [proof,*[read(p) for p in controls]]:
        for p,d in obj['input_sha256'].items():assert sha(p)==d,p
    paths=[Path(__file__),A/'shared_live_ranking_report_runtime_v1_20261011.py',
      A/'verify_shared_live_ranking_report_actual180_v1_20261011.py',
      A/'verify_shared_live_ranking_report_scope_controls_v1_20261011.py',
      A/'prepare_stock_rank60_fixed_leading_case17_native14_v1_20261011.py',
      A/'verify_stock_rank60_fixed_leading_case17_native14_v2_20261011.py',
      A/'stock_rank60_fixed_case17_decay_none_recovery_v2_20261011.json',location,
      *controls,*folder.glob('*.json')]
    template=A/'publish_frozen_Actual183_parent37_and_mixed60_49_sources_main_v1_20261011.py';paths.append(template)
    label='Shared_report_controls_and_fixed60_case17_v2'
    lines=template.read_text(encoding='utf8').replace('Actual183_parent37_and_mixed60_49_sources',label).splitlines()
    i=next(i for i,s in enumerate(lines) if s.strip().startswith('paths=[Path(__file__)'))
    lines[i]='    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]'
    i=next(i for i,s in enumerate(lines) if "payload[(prefix/'manifest.json')" in s)
    manifest={'status':'actual_full180_bytes_and_private_scope_controls_and_fixed_scored60_case17_native_probes_passed',
      'full180_original_native_bytes':read(controls[0])['original_native_bytes'],
      'actual_native_replays':14,'actual_cold_replays':14,'actual_prefit_rejections':7,
      'fixed_case':17,'continuous_official_S':0.4514355480841008,
      'search_winner_not_claimed':True,'new_candidate_full_graph_and_future_inference_pending':True,
      'shared_report_runtime_not_yet_adopted':True,'new_fits_by_publication':0,
      'new_scores_by_publication':0,'test_labels_read':False}
    lines[i]="    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})"
    i=next(i for i,s in enumerate(lines) if "'commit','-m'" in s)
    lines[i]="            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存完整180榜字节一致性及作用域控制，60日case17原生14和冷启动14及拟合前拒绝7项；完整候选与搜索胜者资格待完成',timeout=180)"
    p=A/'publish_frozen_shared_report_controls_and_fixed60_case17_main_v2_20261011.py'
    source='\n'.join(lines)+'\n';ast.parse(source);assert not p.exists();p.write_text(source,encoding='utf8')
    assert allowed();runpy.run_path(str(p),run_name='__main__')

if __name__=='__main__':main()
