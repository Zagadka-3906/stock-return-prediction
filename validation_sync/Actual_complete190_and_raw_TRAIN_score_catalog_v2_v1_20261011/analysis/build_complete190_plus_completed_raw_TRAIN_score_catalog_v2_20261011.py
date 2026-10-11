from pathlib import Path
import sys,ast,json,csv,hashlib,datetime,math
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def main():
 assert allowed();closed('recovery65_actual_flag17_after_verified_best38_direct17_v1_20261011')
 out=Path('E:/赛题五_本机临时/完整190轮与新增已完成TRAIN评分明细榜_v2_20261011');out.mkdir(exist_ok=False)
 source=A/'build_all_model_rankings_20261003.py';text=source.read_text(encoding='utf8');old='if not match or int(match[1])<13:continue';new='if not match or int(match[1])<13 or int(match[1])>190:continue';assert text.count(old)==1
 namespace={'__name__':'original_ranking_inventory_frozen_to_verified190','__file__':str(source)};exec(compile(text.replace(old,new),str(source),'exec'),namespace)
 original,counts,failures=namespace['connected_inventory']();assert len(original)==17726
 fields=['row_id','rank','S','ic_mean','annual_excess','mean_turnover','name','source','source_sha256','official_capsule_sha256','known_restriction','qualification','configuration']
 rows=[];sources={str(source):sha(source)}
 for r in original:
  metrics=r.get('metrics',{});path=Path(r['source']) if 'source' in r else None
  rows.append({'row_id':'formal190/'+r['id'],'S':r['score'],'ic_mean':metrics.get('ic_mean'),'annual_excess':metrics.get('annual_excess'),'mean_turnover':metrics.get('mean_turnover'),'name':r['name'],'source':str(path) if path else str(r.get('source_path','')),'source_sha256':'','official_capsule_sha256':'','known_restriction':r['known_restriction'],'qualification':r['status'],'configuration':json.dumps({'source_pointer':r['source_pointer'],'parameters_preserved_in_original_source':True},ensure_ascii=False,separators=(',',':'))})
 for k,v in namespace['SOURCES'].items():sources[k]=v['sha256']
 for row in rows:row['source_sha256']=sources[row['source']]
 recent=[];rejected=[];base=Path('E:/赛题五_本机临时')
 required={'ic_mean','ic_std','icir','ic_positive_ratio','annual_excess','top1_annual_ret','mean_turnover','final_score'}
 common=A/'connected_validation_20261002/combined_fold_frame.parquet';common_sha=sha(common)
 for folder in sorted(base.glob('*screen*20261011')):
  report=folder/'verification.json'
  if not report.is_file():continue
  proof=read(report);rr=proof.get('records')
  if not isinstance(rr,list) or not rr:continue
  if proof.get('test_labels_read') is not False:rejected.append({'folder':str(folder),'reason':'explicit no-test-label proof missing'});continue
  if proof.get('input_sha256',{}).get(str(common))!=common_sha:rejected.append({'folder':str(folder),'reason':'exact common full TRAIN frame pin not present'});continue
  if not all(isinstance(r,dict) and 'official_score_cache' in r and 'official_metric_capsule_sha256' in r and required<=set(r.get('metrics',{})) and r.get('test_labels_read') is False and r.get('actual_return_mapping',{}).get('actual_return_mapped_csv_scored') is True for r in rr):rejected.append({'folder':str(folder),'reason':'full official record/capsule/calibrated output evidence not present'});continue
  before=len(rows);sources[str(report)]=sha(report)
  for r in rr:
   assert allowed();case=int(r['case']);rp=folder/f'case{case:03d}_official.json';assert read(rp)==r
   cap=Path(r['official_score_cache']['official_metrics_source']);digest=sha(cap);assert digest==r['official_metric_capsule_sha256'] and read(cap)['metrics']==r['metrics']
   controls=folder/f'case{case:03d}_controls.json';assert sha(controls)==r['control_sha256'];assert read(controls)['numeric_sha256']==r['prediction_numeric_sha256']
   m=r['metrics'];assert m['final_score']==r['connected_final_score'];assert math.isclose(m['final_score'],.4*m['ic_mean']+.3*m['annual_excess']+.3*(1-m['mean_turnover']),rel_tol=0,abs_tol=1e-12)
   sources[str(rp)]=sha(rp);sources[str(cap)]=digest;sources[str(controls)]=sha(controls)
   rows.append({'row_id':'raw/'+folder.name+'/'+str(case),'S':m['final_score'],'ic_mean':m['ic_mean'],'annual_excess':m['annual_excess'],'mean_turnover':m['mean_turnover'],'name':r.get('recipe',folder.name),'source':str(rp),'source_sha256':sha(rp),'official_capsule_sha256':digest,'known_restriction':False,'qualification':'全量TRAIN官方评分及数值因果对照完成；完整候选推理资格单独核验','configuration':json.dumps(r['configuration'],ensure_ascii=False,separators=(',',':'))})
  recent.append({'folder':str(folder),'score_records':len(rows)-before,'verification_sha256':sources[str(report)]})
 assert len({r['row_id'] for r in rows})==len(rows)
 rows.sort(key=lambda r:(r['S'] is None,-(r['S'] or 0),r['row_id']))
 prior=None;rank=0
 for i,r in enumerate(rows,1):
  if r['S']!=prior:rank=i;prior=r['S']
  r['rank']=rank
 best=read(A/'alternate_verified_best_blend38_submission_delivery_v1_20261011.json')
 for name,subset in [('全部训练验证分数明细.csv',rows),('排除已知非因果限制后的训练分数明细.csv',[r for r in rows if not r['known_restriction']])]:
  with (out/name).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(subset)
 for file,d in sources.items():assert sha(file)==d,file
 manifest={'status':'passed_exact_original17726_formal190_inventory_plus_full_evidence_completed_raw_TRAIN_records_compact_catalog','original_formal_records':17726,'added_completed_raw_score_instances':len(rows)-17726,'total_score_instances':len(rows),'recent_families':recent,'excluded_from_new_raw_addition':rejected,'known_original_failures_preserved_count':len(failures),'source_sha256':sources,'best_fully_verified_delivery':best,'score_instance_aliases_retained_not_unique_physical_models':True,'full_six_view_browser_QA_not_replaced_or_claimed_for_this_compact_export':True,'candidate_test_inference_qualification_not_implied_by_raw_score_rank':True,'new_fits':0,'new_scores':0,'test_labels_read':False,'global_exhaustion_proven':False,'csv_sha256':{p.name:sha(p) for p in out.glob('*.csv')}}
 create(out/'verification.json',manifest)
 (out/'说明.md').write_text('此表包含第190轮17726条原始训练验证评分记录及具有完整官方分数、共同TRAIN样本和因果对照证据的新记录。重复配置、锚点和缓存对照按验证记录保留，不等于独立物理模型数量。\n\n原有非因果限制仍明确标记。原始完整榜及六视图QA保持独立；本表不冒充新的完整浏览器核验。新记录的官方评分完成不等于完整候选推理完成，提交应以已完整核验交付记录为准。未读取测试标签。\n',encoding='utf8')
 create(A/'complete190_plus_completed_raw_TRAIN_score_catalog_location_v2_20261011.json',{'output':str(out),'verification_sha256':sha(out/'verification.json'),'total_score_instances':len(rows),'added_raw_score_instances':len(rows)-17726})
 print({'total_score_instances':len(rows),'added_raw_score_instances':len(rows)-17726,'output':str(out)},flush=True)
if __name__=='__main__':main()
