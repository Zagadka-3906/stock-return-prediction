from pathlib import Path
from datetime import datetime
import sys,os
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
assert allowed();closed('actual_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011')
decision=read(A/'rank60medium2048_best33_gain_decision_v1_20261011.json')
if not decision['adopt']:
 print('No higher TRAIN S: no new candidate delivery.',flush=True);sys.exit(0)
closed('actual_StockRank60MediumBest33Early_selected_candidate_sealing_v3_20261011')
closed('actual_rank60medium2048_best33_complete_candidate_main_v1_20261011')
release=A/'StockRank60MediumBest33Early_selected_release_v2_20261011';ready=read(release/'selected_candidate_ready_for_registration.json')
assert ready['sealed_candidate_complete'] and ready['new_inference_claimed'] and ready['actual_saved_native_models']==36
candidate=Path(ready['source_candidate']);proof=read(candidate/'verification.json');manifest=read(candidate/'manifest.json')
assert proof['status']=='passed' and (proof['rows'],proof['days'],proof['codes'])==(1599600,344,4650) and proof['test_labels_read'] is False
for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert proof[key]
assert len(proof['models'])==len({x['sha256'] for x in proof['models'].values()})==36
for relative,info in manifest['files'].items():assert sha(candidate/relative)==info['sha256'],relative
raw=read(Path('E:/赛题五_本机临时/StockRank60MediumEmbeddingMedium2048_after183_direct_allocation33_screen_v1_20261011/verification.json'))
assert raw['new_quality_score_records']==len(raw['records'])==33 and (raw['actual_nonidentity_full_controls'],raw['actual_nonidentity_prefix_controls'])==(32,96)
official=read(release/'calibrated_csv_official.json')['metrics']
assert official==decision['best']['metrics'] and official['final_score']>decision['incumbent_S']
assert max(r['connected_final_score'] for r in raw['records'])==official['final_score']
receiptpath=A/'Actual_rank60medium2048_best33_complete_candidate_sources_and_submission_main_receipt_v1_20261011.json';receipt=read(receiptpath)
assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
source=candidate/'submission.csv';digest=sha(source);assert digest==proof['csv_sha256']
directory=Path('E:/赛题五_最终提交/已核验候选_60日更大容量最佳33项_20261011');assert not directory.exists();directory.mkdir(parents=True)
physical=source.resolve();assert physical.drive.upper()=='E:';os.link(physical,directory/'submission.csv');assert sha(directory/'submission.csv')==digest
data={'status':'ready_sealed_native_verified_main_published_candidate_full_connected_board_pending','at_local':datetime.now().isoformat(),'optimization_deadline_local':'2026-10-11T13:00:00+08:00','official_TRAIN_internal_score':official['final_score'],'official_TRAIN_all8_metrics':official,'rows':1599600,'days':344,'codes':4650,'models':36,'csv_sha256':digest,'source_candidate':str(candidate),'source_candidate_manifest_sha256':sha(candidate/'manifest.json'),'actual_main_commit':receipt['commit'],'main_receipt':str(receiptpath),'all_full_native_independent_reload_csv_and_cold80_checks_passed':True,'full_connected_board_pending':True,'canonical_fully_qualified_delivery_pointer_unchanged':True,'competition_upload_performed':False,'test_labels_read':False}
create(directory/'submission_manifest.json',data)
(directory/'提交说明.md').write_text('此文件是完成全部原生重载、两次全量独立推理、CSV复现、80日冷启动、33项TRAIN官方评分与GitHub main同步的候选。完整榜登记尚待完成。\n\n训练内部官方S='+str(official['final_score'])+'；不代表官方测试成绩。\n\n提交文件：submission.csv；1599600行，列为ts_code、trade_date、pred。\n\nSHA256：'+digest+'。\n\n保留第183轮原提交文件；尚未向比赛平台上传。\n',encoding='utf8')
create(A/'alternate_verified_rank60medium2048_best33_submission_delivery_v1_20261011.json',{'output':str(directory),**data});print({'verified_alternate_candidate':str(directory),'S':official['final_score'],'full_board_pending':True},flush=True)
