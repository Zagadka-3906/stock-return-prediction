"""Create an E-backed exact ready-to-submit CSV only from fully qualified main-published candidates."""
from pathlib import Path
import sys,time,json,subprocess,os
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    assert read(A/'optimization_20261003_r144/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round144_receipt.json')['status']=='pushed_and_remote_head_verified'
    choices=[]
    for number in (134,135,143,144):
        release=A/f'optimization_20261003_r{number}';candidate=ROOT/f'candidates/optimization_20261003_r{number}'
        assert read(release/'full_registration_execution.json')['status']=='passed';assert read(A/f'github_validation_sync_main_20261005/round{number}_receipt.json')['status']=='pushed_and_remote_head_verified'
        verification=read(candidate/'verification.json');selection=read(candidate/'selection.json');assert verification['status']=='passed'
        count=len({v['sha256'] for v in verification['models'].values()});choices.append((selection['winner']['metrics']['final_score'],count,number,candidate))
    score,count,number,candidate=min(choices,key=lambda row:(-row[0],row[1],row[2]));assert number==144
    proof=read(candidate/'verification.json');assert (proof['rows'],proof['days'],proof['codes'])==(1599600,344,4650)
    for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert proof[key]
    source=candidate/'submission.csv';digest=sha(source);assert digest==proof['csv_sha256']
    target=Path(f'E:/赛题五_最终提交/已完全验证第{number}轮_20261008');assert not target.exists();target.mkdir(parents=True)
    source_physical=source.resolve();destination=target/'submission.csv';assert source_physical.drive.upper()==destination.drive.upper()=='E:';os.link(source_physical,destination);assert sha(destination)==digest
    receipt=read(A/f'github_validation_sync_main_20261005/round{number}_receipt.json')
    manifest={'status':'ready_exact_fully_qualified_main_published_submission_csv','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deadline_local':'2026-10-10T23:59:00+08:00','selected_round':number,'TRAIN_internal_continuous_forward_official_score':score,'actual_unique_native_models':count,'rows':1599600,'days':344,'codes':4650,'columns':['ts_code','trade_date','pred'],'submission_csv_sha256':digest,'source_candidate':str(candidate),'source_manifest_sha256':sha(candidate/'manifest.json'),'main_publication_commit':receipt['commit'],'main_publication_receipt':str(A/f'github_validation_sync_main_20261005/round{number}_receipt.json'),'all_full_native_independent_reload_CSV_and_cold80_checks_passed':True,'competition_upload_performed':False,'test_labels_read':False,'optimization_continues':True}
    create(target/'submission_manifest.json',manifest)
    create(A/'latest_verified_submission_delivery_v1_20261008.json',{'status':manifest['status'],'output':str(target),'selected_round':number,'csv_sha256':digest,'manifest_sha256':sha(target/'submission_manifest.json'),'main_commit':receipt['commit']})
    (target/'提交说明.md').write_text(f"# 已验证提交文件\n\n提交截止：2026年10月10日23:59。\n\n待提交文件：`submission.csv`，含1,599,600行，字段为ts_code、trade_date、pred；顺序已与比赛测试输入逐行核验。无需手工排序或编辑。\n\n来自第{number}轮，训练内部连续前向验证官方分数为{score:.12f}，保存模型物理SHA去重后为{count}份。两次全量原生推理、独立解码、模型重载、CSV逐字节复现和80天冷启动全部通过；完整榜原始六视图QA及main同步已完成。\n\n文件SHA256：`{digest}`。详见submission_manifest.json。模型、完整冻结源码和原始证据保留在{candidate}；该位置通过目录连接存放于E盘。\n\n此文件已经准备好，本程序没有向比赛平台执行提交。优化仍继续；后续只有完全通过验证的更高分方案才会生成新的提交目录。\n",encoding='utf8')
    print(json.dumps({'ready':str(destination),'round':number,'score':score,'models':count,'sha256':digest},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
