"""Maintain immutable E deliveries only after complete candidate/QA/main qualification; continue optimization."""
from pathlib import Path
import argparse,json,os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from monitor_actual_chronological_optimization_progress_v21_20261008 import snapshot
POINTER=A/'latest_verified_submission_delivery_v2_20261008.json'
def update():
    best=snapshot()['best_fully_qualified'];number=best['round']
    if POINTER.exists() and read(POINTER)['selected_round']==number:return None
    release=A/f'optimization_20261003_r{number}';candidate=ROOT/f'candidates/optimization_20261003_r{number}'
    proof=read(candidate/'verification.json');selection=read(candidate/'selection.json')
    official=read(release/'calibrated_csv_official.json')['metrics'];receipt=read(A/f'github_validation_sync_main_20261005/round{number}_receipt.json')
    assert read(release/'full_registration_execution.json')['status']=='passed' and receipt['status']=='pushed_and_remote_head_verified'
    assert proof['status']=='passed' and selection['winner']['metrics']==official and official['final_score']==best['score']
    assert (proof['rows'],proof['days'],proof['codes'])==(1599600,344,4650)
    for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert proof[key]
    assert len({value['sha256'] for value in proof['models'].values()})==best['unique_models']
    source=candidate/'submission.csv';digest=sha(source);assert digest==proof['csv_sha256']
    directory=Path(f'E:/赛题五_最终提交/已完全验证第{number}轮_20261008')
    if directory.exists():
        manifest=read(directory/'submission_manifest.json')
        assert manifest['selected_round']==number and manifest['submission_csv_sha256']==sha(directory/'submission.csv')==digest
        assert manifest['TRAIN_internal_continuous_forward_official_score']==best['score']
    else:
        directory.mkdir(parents=True,exist_ok=False);physical=source.resolve();destination=directory/'submission.csv'
        assert physical.drive.upper()==destination.drive.upper()=='E:';os.link(physical,destination);assert sha(destination)==digest
        manifest={'status':'ready_exact_fully_qualified_main_published_submission_csv','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'deadline_local':'2026-10-10T23:59:00+08:00','selected_round':number,
            'TRAIN_internal_continuous_forward_official_score':best['score'],'actual_unique_native_models':best['unique_models'],
            'rows':1599600,'days':344,'codes':4650,'columns':['ts_code','trade_date','pred'],'submission_csv_sha256':digest,
            'source_candidate':str(candidate),'source_manifest_sha256':sha(candidate/'manifest.json'),
            'main_publication_commit':receipt['commit'],'main_publication_receipt':str(A/f'github_validation_sync_main_20261005/round{number}_receipt.json'),
            'all_full_native_independent_reload_CSV_and_cold80_checks_passed':True,'competition_upload_performed':False,
            'test_labels_read':False,'optimization_continues':True}
        create(directory/'submission_manifest.json',manifest)
        (directory/'提交说明.md').write_text(f"# 已验证提交文件\n\n截止：2026年10月10日23:59。\n\n提交文件为同目录的 submission.csv，共1,599,600行，字段为ts_code、trade_date、pred；已按比赛输入顺序逐行验证。\n\n第{number}轮，训练内部连续前向官方S={best['score']:.12f}，{best['unique_models']}个物理模型。两次完整推理、独立解码、模型重载、CSV逐字节复现、80天冷启动、完整榜原始六视图及main同步已通过。\n\nSHA256：{digest}。详见 submission_manifest.json。\n\n该文件已准备好，尚未向比赛平台提交。优化继续，旧的合格提交文件保留。\n",encoding='utf8')
    pointer={'status':manifest['status'],'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'output':str(directory),
        'selected_round':number,'official_score':best['score'],'actual_unique_native_models':best['unique_models'],
        'csv_sha256':digest,'manifest_sha256':sha(directory/'submission_manifest.json'),'main_commit':receipt['commit'],
        'previous_qualified_deliveries_preserved':True,'competition_upload_performed':False}
    temporary=POINTER.with_name(POINTER.name+f'.{os.getpid()}.tmp');temporary.write_text(json.dumps(pointer,ensure_ascii=False,indent=2)+'\n',encoding='utf8');os.replace(temporary,POINTER)
    ledger=A/f'qualified_submission_delivery_update_round{number}_v2_20261008.json';assert not ledger.exists();create(ledger,pointer)
    print(json.dumps(pointer,ensure_ascii=False),flush=True);return pointer
def main(once):
    while True:
        update()
        if once:return
        time.sleep(45)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--once',action='store_true');main(parser.parse_args().once)
