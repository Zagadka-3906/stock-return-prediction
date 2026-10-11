"""Publish actual completed early full candidate controls; full board qualification stays pending."""
from pathlib import Path
import sys,ast,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def main():
 assert allowed();closed('actual_StockRank60Fixed17Early2_selected_candidate_sealing_v3_20261011')
 release=A/'StockRank60Fixed17Early2_selected_release_v2_20261011'
 ready=read(release/'selected_candidate_ready_for_registration.json')
 assert ready['status']=='passed_fixed_case17_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
 candidate=Path(ready['source_candidate']);prediction=read(candidate/'verification.json')
 assert prediction['status']=='passed' and prediction['rows']==1599600
 assert len(prediction['models'])==36 and prediction['csv_sha256']==sha(candidate/'submission.csv')
 for k in ['model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical']:assert prediction[k]
 manifest=read(candidate/'manifest.json')
 for rel,info in manifest['files'].items():assert sha(candidate/rel)==info['sha256'],rel
 aliases=A/'actual_rank60_120_direct_own_pointer_aliases_v2_20261011.json'
 for p,d in read(aliases)['input_sha256'].items():assert sha(p)==d,p
 screen=Path('E:/赛题五_本机临时/StockRank60EmbeddingSmall512_after183_direct_allocation33_screen_v1_20261011/verification.json')
 proof=read(screen);assert len(proof['records'])==33 and max(r['connected_final_score'] for r in proof['records'])==0.4514355480841008
 paths=[Path(__file__),aliases,A/'recover_fixed17_early_candidate_and_canonical_own_pointers_v2_20261011.py',
  A/'stock_rank60_fixed17_early_candidate_sources_preparation_v2_20261011.json',
  A/'stock_rank60_fixed17_early_storage_v2_20261011.py',
  A/'prepare_StockRank60Fixed17Early2_selected_candidate_v2_20261011.py',
  A/'seal_StockRank60Fixed17Early2_selected_candidate_v3_20261011.py',
  A/'run_StockRank60Fixed17Early2_selected_candidate_feature_cache_v2_20261011.py',
  *release.glob('*.json'),screen,candidate/'submission.csv',candidate/'manifest.json']
 # Scientific Python snapshots and metadata are publicable; large model/array binaries stay on E.
 paths += [p for p in candidate.rglob('*') if p.is_file() and p.suffix in ('.py','.json')]
 for h in [60,120]:paths += [A/f'actual_StockRank{h}EmbeddingSmall512_full5_independent_location_v1_20261011.json',A/f'actual_StockRank{h}DirectEmbeddingSmall512_full5_independent_location_v1_20261011.json']
 template=A/'publish_frozen_Actual183_parent37_and_mixed60_49_sources_main_v1_20261011.py';paths.append(template)
 label='Early_fixed60_full_candidate_and_actual_own_aliases_v2'
 lines=template.read_text(encoding='utf8').replace('Actual183_parent37_and_mixed60_49_sources',label).splitlines()
 i=next(i for i,s in enumerate(lines) if s.strip().startswith('paths=[Path(__file__)'))
 lines[i]='    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]'
 i=next(i for i,s in enumerate(lines) if "payload[(prefix/'manifest.json')" in s)
 result={'status':'actual_fixed_case17_complete_frozen_candidate_native_independent_cold80_CSV_source_package_passed',
  'S':0.4514355480841008,'actual_native_models':36,'actual_future_rows':1599600,
  'csv_sha256':prediction['csv_sha256'],'complete_direct33_scores_passed':True,
  'fixed_case_pre_future_freeze_and_all_original_replay_checks_retained':True,
  'full_connected_ranking_QA_and_round200_main_still_pending':True,
  'delivered183_not_replaced_by_this_source_publication':True,
  'actual60_and120_complete_own_panel_pointer_aliases_byte_identical':True,
  'new_fits_by_publication':0,'new_scores_by_publication':0,'test_labels_read':False}
 lines[i]="    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(result)+",'files':bindings})"
 i=next(i for i,s in enumerate(lines) if "'commit','-m'" in s)
 lines[i]="            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存60日case17完整36模型原生及独立与80日冷启动CSV核验和33项评分；两期限实际年度原始预测指针已按字节核实，完整榜资格仍待完成',timeout=180)"
 driver=A/'publish_frozen_early_fixed60_complete_candidate_and_own_aliases_main_v2_20261011.py'
 source='\n'.join(lines)+'\n';ast.parse(source);assert not driver.exists();driver.write_text(source,encoding='utf8')
 assert allowed();runpy.run_path(str(driver),run_name='__main__')

if __name__=='__main__':main()
