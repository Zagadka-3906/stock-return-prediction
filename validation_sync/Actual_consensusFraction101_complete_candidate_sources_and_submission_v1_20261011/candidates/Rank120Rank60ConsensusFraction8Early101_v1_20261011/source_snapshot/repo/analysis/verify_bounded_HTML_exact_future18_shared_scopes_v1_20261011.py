"""Actual190-207 private codec/QA reader scopes nested with bounded original HTML."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def main():
 assert allowed();closed('actual_bounded_original_ranking_HTML_tail_and_scope_controls_v1_20261011')
 old=A/'verify_shared_live_report_exact15_tuple_scope_controls_v4_20261011.py'
 text=old.read_text(encoding='utf-8').replace('共享榜对象精确15作用域控制_v4_20261011','原始榜HTML与共享读取18作用域实测_v1_20261011')
 needle='    namespace = {\'write_exact_report\': original_writer}';assert text.count(needle)==1
 text=text.replace(needle,"    namespace = {'write_exact_report': original_writer,'__file__':ranking.__file__}")
 needle="    import shared_live_ranking_report_runtime_v3_20261011 as runtime";assert text.count(needle)==1
 text=text.replace(needle,needle+'\n    import bounded_original_ranking_HTML_runtime_v1_20261011 as html')
 needle="with runtime.installed(row['number'],row['codec_name'],row['verifier_name']) as state:";assert text.count(needle)==1
 text=text.replace(needle,needle[:-1]+",html.installed():\n            assert ranking.main.__globals__['write_bounded_original_html'] is html.writer.write\n            assert ranking.main.__globals__['write_exact_report'] is namespace['write_exact_report']")
 namespace={'__name__':'actual_future18_bounded_HTML_shared_scope_fixture','__file__':str(old)};exec(compile(text,str(old),'exec'),namespace)
 variants=[r for r in read(A/'shared_live_report_exact15_variants_admission_v2_20261011.json')['variants'] if 190<=r['number']<=201]
 factories=['prepare_StockRank60Fraction202_complete40_pipeline_v2_20261011','prepare_Rank120Rank60Protected203_complete39_pipeline_v1_20261011','prepare_StockRank60Seed10Direct204_complete35_pipeline_v1_20261011','prepare_Rank60TwoSeedProtected205_complete39_pipeline_v2_20261011','prepare_StockRank60Window504Direct206_complete35_pipeline_v1_20261011','prepare_Rank120Rank60BestBlend207_complete40_pipeline_v1_20261011']
 paths=[Path(__file__),old,A/'bounded_original_ranking_HTML_runtime_v1_20261011.py',A/'bounded_original_ranking_HTML_actual_full180_and_scope_admission_v1_20261011.json']
 for number,name in zip(range(202,208),factories):
  m=importlib.import_module(name);variants.append({'number':number,'codec_name':Path(m.NAMES[5]).stem,'verifier_name':Path(m.NAMES[6]).stem});paths.append(Path(m.__file__))
 assert [r['number'] for r in variants]==list(range(190,208))
 results=[namespace['run_variant'](r) for r in variants]
 paths += [Path(r['execution']) for r in results]+[A/(r[k]+'.py') for r in variants for k in ('codec_name','verifier_name')]
 create(A/'bounded_original_HTML_exact_future18_shared_scopes_admission_v1_20261011.json',{'status':'passed_actual_all18_exact190207_private_codec_QA_reader_tuple_semantics_and_nested_bounded_HTML_scope_restore','variants':variants,'actual_scope_results':results,'input_sha256':{str(p):sha(p) for p in paths},'actual_scientific_rounds_not_executed_by_fixtures':True,'all_original_per_round_full_browser_QA_still_required':True,'new_fits':0,'new_scores':0,'test_labels_read':False})
 print('Actual18 exact future codec/QA reader and bounded HTML scope fixtures passed; future runtime adoption still pending',flush=True)

if __name__=='__main__':main()
