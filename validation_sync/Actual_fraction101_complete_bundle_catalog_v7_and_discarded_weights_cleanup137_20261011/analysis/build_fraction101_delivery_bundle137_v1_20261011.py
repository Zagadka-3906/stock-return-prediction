from pathlib import Path
import sys,zipfile,hashlib,csv,copy,os
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from scoped_user_cleanup_package134_runtime_v1_20261011 import install
gates=install()
from run_dependency_queue_v3_20261006 import read,sha,create
gates.closed('actual_fraction101_scoped_main134_v1_20261011')
pointer=A/'alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json';delivery=read(pointer)
assert delivery['all_full_native_independent_reload_csv_and_cold80_checks_passed'] and delivery['official_TRAIN_internal_score']==.4514612196682616
directory=Path(delivery['output']);candidate=Path(delivery['source_candidate']);manifest=read(candidate/'manifest.json')
readme='''# 赛题五最新高分方案：60/120日一致性融合，保护比例15%

训练集内部连续向前验证的官方评分公式 S = 0.4514612196682616。
IC均值 0.12280208457197295；年化超额 0.3735093425702569；平均换手 0.032374723105348766。
这不是比赛平台测试集成绩，尚未向比赛平台上传。

直接提交本目录 submission.csv，或解压方案包后使用根目录 submission.csv。
CSV包含1,599,600行，344个交易日、4,650只股票；列为ts_code、trade_date、pred。
方案采用完整第183轮父方案，加上60/120日成熟标签信号，融合权重0.04、一致性参数0.75、保护比例0.15。
37个已保存模型的重载、两次独立全量推理、CSV字节一致和80日冷启动因果检查均实际通过。
全部8项TRAIN评分保留；不把中断的第192轮正式榜登记算作完成。

方案ZIP包括根目录提交文件、完整candidate目录中的37个原生权重、配置、冻结源码和验证证据。
保留candidate/manifest.json的原始内容；每个ZIP条目均另行核对SHA256。
该包不包含比赛原始训练数据或Python环境；冻结源码记录了本机工程绝对路径，迁移复现须恢复相应数据和路径。
原工程目录：D:\\3.Study\\数据分析\\赛题五。
已完成的推理无需重跑；先使用现成提交文件。旧分数0.4514555940046018候选保留为备份。

弃用模型已仅删除权重及训练恢复缓存，历史分数、模型配置、哈希和验证记录仍保留。
'''
(directory/'方案使用说明.md').write_text(readme,encoding='utf8')
archive=directory/'赛题五_高分方案_S0.45146122_20261011.zip';assert not archive.exists()
paths={'submission.csv':directory/'submission.csv','方案使用说明.md':directory/'方案使用说明.md','submission_manifest.json':directory/'submission_manifest.json','candidate/manifest.json':candidate/'manifest.json'}
paths.update({'candidate/'+name:candidate/name for name in manifest['files']})
expected={name:sha(p) for name,p in paths.items()}
for name,info in manifest['files'].items():assert expected['candidate/'+name]==info['sha256']
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as z:
    for name,p in paths.items():assert gates.allowed();z.write(p,name)
with zipfile.ZipFile(archive) as z:
    assert set(z.namelist())==set(expected) and len(z.namelist())==len(expected)
    for name,digest in expected.items():
        with z.open(name) as f:assert hashlib.file_digest(f,'sha256').hexdigest()==digest,name
cleanup=[read(A/n) for n in ['actual_unadopted_BF16micro134_cleanup_verification_v1_20261011.json','actual_unselected_banks135_cleanup_verification_v1_20261011.json','actual_unadopted_micro_restart136_cleanup_verification_v1_20261011.json']]
result={'status':'passed_complete_sealed_candidate_bundle_every_archive_entry_SHA256_verified','archive':str(archive),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,'archive_entries':len(paths),'csv_sha256':delivery['csv_sha256'],'official_TRAIN_internal_score':delivery['official_TRAIN_internal_score'],'models':37,'actual_main_commit':delivery['actual_main_commit'],'deleted_unadopted_files':sum(p['deleted_files'] for p in cleanup),'deleted_unadopted_logical_bytes':sum(p['logical_deleted_bytes'] for p in cleanup),'new_training':0,'new_scoring':0,'new_inference':0,'competition_upload_performed':False,'formal192_registration_not_complete':True,'test_labels_read':False}
create(directory/'方案包核验.json',result);create(A/'actual_fraction101_delivery_bundle137_verification_v1_20261011.json',result)
oldpointer=A/'complete191_plus_completed_raw_TRAIN_score_catalog_location_v5_20261011.json';old=Path(read(oldpointer)['output']);report=read(old/'verification.json');assert sha(old/'verification.json')==read(oldpointer)['verification_sha256']
out=Path('E:/赛题五_本机临时/完整191轮与新增已完成TRAIN评分明细榜_v7_20261011');out.mkdir(exist_ok=False)
for name,digest in report['csv_sha256'].items():assert sha(old/name)==digest;os.link(old/name,out/name);assert sha(out/name)==digest
latest=copy.deepcopy(report);latest.update(status='passed_existing_v5_scores_bytes_unchanged_latest_sealed_native37_delivery_and_packaging_metadata_updated',best_fully_verified_delivery=delivery,score_tables_bytes_unchanged_from_v5=True,new_scores=0,original_formal191_cap_preserved=True,interrupted192_registration_not_complete=True)
latest['source_sha256'].update({str(p):sha(p) for p in [Path(__file__),oldpointer,old/'verification.json',pointer,directory/'方案包核验.json']})
create(out/'verification.json',latest)
(out/'说明.md').write_text((old/'说明.md').read_text(encoding='utf8')+'\n本版本评分CSV与v5逐字节相同，仅更新已封装且完整核验的新高分交付指针。第192轮正式榜登记未完成，优化目标继续暂停。\n',encoding='utf8')
create(A/'complete191_plus_completed_raw_TRAIN_score_catalog_location_v7_20261011.json',{'output':str(out),'verification_sha256':sha(out/'verification.json'),'total_score_instances':report['total_score_instances'],'CSV_bytes_unchanged_from_v5':True,'best_ready_S':delivery['official_TRAIN_internal_score']})
print({k:result[k] for k in ['status','archive','archive_bytes','archive_entries','deleted_unadopted_files','deleted_unadopted_logical_bytes']},flush=True)
