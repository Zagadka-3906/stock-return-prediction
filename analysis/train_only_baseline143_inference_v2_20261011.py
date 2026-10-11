"""Column-order-only inference adapter for the immutable baseline143 trainer.

The original training/scoring source and frozen scientific protocol are retained.
Both sides of a vertical concat are selected in exactly RAW + row_id order.
"""
from pathlib import Path
import argparse,gzip,hashlib,json,shutil,zipfile
import polars as pl
import train_only_baseline143_v1_20261011 as b
from train_only_features143_v1_20261011 import source,features,RAW


def corrected_features(a,limit=None):
    train=source(a.train_csv,False)
    dates=train.select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    history=train.filter(pl.col('trade_date')>=int(dates[-61:][0])).select(RAW+['row_id'])
    test=source(a.test_x,False).select(RAW+['row_id'])
    if limit is not None:test=test.filter(pl.col('trade_date')<=limit)
    lf,names=features(pl.concat([history,test],how='vertical'))
    return lf.filter(pl.col('trade_date')>20241231),names


def prepare_adapter(a):
    b.guard(a,'freeze column-order-only inference adapter')
    w=a.work_dir;protocol=b.protocol(a);seal=b.read(w/'frozen_before_TEST_inference.json')
    assert b.sha(w/'model_final.txt')==seal['model_sha256']
    assert b.sha(w/'protocol.json')==seal['protocol_sha256']
    p=Path(__file__);target=w/p.name
    if target.resolve()!=p.resolve():shutil.copyfile(p,target)
    record=w/'inference_adapter_frozen_before_TEST_inference.json'
    d={'status':'fixed_column_order_interface_only','frozen_at_local':b.now(),
       'change':'Select TEST-X columns in RAW + row_id order, matching the TRAIN-history concat side.',
       'original_training_scoring_source_unchanged':True,'scientific_protocol_unchanged':True,
       'features_model_parameters_targets_and_output_values_not_changed_by_adapter':True,
       'adapter_source_sha256':b.sha(target),'protocol_sha256':seal['protocol_sha256'],
       'final_model_sha256':seal['model_sha256'],'TEST_outcomes_read_or_reconstructed':False}
    if record.exists():assert b.read(record)['adapter_source_sha256']==d['adapter_source_sha256']
    else:b.put(record,d)
    failed=w/'first_inference_failure.json'
    if not failed.exists():b.put(failed,{'status':'retained_initial_interface_failure_not_scientific_selection',
       'at_local':'2026-10-11T22:11:53+08:00','error':'polars.InvalidOperationError: vertical concat column order mismatch',
       'training_and_validation_completed_before_failure':True,'TEST_outcomes_read_or_reconstructed':False,
       'original_training_protocol_retained':True})
    b.inference_features=corrected_features


def package(a):
    b.guard(a,'package verified fixed baseline with corrected inference entry')
    w=a.work_dir;v=b.read(w/'verification.json');assert v['status'].startswith('passed_')
    d=a.delivery_dir;d.mkdir(parents=True,exist_ok=True)
    files=['train_only_baseline143_v1_20261011.py','train_only_features143_v1_20261011.py',
           Path(__file__).name,'inference_adapter_frozen_before_TEST_inference.json','first_inference_failure.json',
           'evaluate.py','protocol.json','protocol.sha256','synthetic_causality.json',
           'model_final.txt','model_final.json','official_TRAIN_metrics.json','frozen_before_TEST_inference.json',
           'verification.json','submission.csv']
    for y in range(2020,2025):files += [f'model_{y}.txt',f'model_{y}.json']
    for n in files:shutil.copyfile(w/n,d/n)
    text=f'''# 固定训练内基线143：未来一天收益预测

本方案按用户“训练符合要求的模型”的指令重新训练。采用测试收益揭示前已存在的63项量价特征及LightGBM参数：31叶、180轮、学习率0.05、种子2026。目标直接使用原始训练集的未来一天收益率，不使用历史赢家、教师信号、成员与排序分离或后处理。只有一个固定候选，科学设计在本轮首次训练和评分前冻结。

训练内部2020—2024年逐年向前预测连续连接，共1,212日、5,635,800行。未修改官方evaluate.py，综合分为 **{v['official_TRAIN_score']:.10f}**。这是训练验证分，不是比赛平台测试成绩，也不代表所有模型中最优。每年训练标签的结束日期严格早于验证开始；最终训练剔除训练集末日标签。特征在计算前移除标签列，滚动使用本股票当前/历史行情，截面排名仅使用同日数据。预测时点为当日行情已完整获得之后。

已完成5次年度训练和1次最终训练。测试预测覆盖1,599,600行、344日、4,650只股票，主键顺序与测试输入相同，pred为收益率小数。模型重载、全量CSV重放及80日特征/预测前缀一致性均通过。最终模型仅有1个；另保留5个年度验证模型以供审计。

最初推理因字段顺序不一致中止。v2入口仅对齐数据连接的列顺序，原训练/评分源码、特征、模型和协议保持原哈希；失败记录和修复冻结记录一并保留。当前执行不重建或使用测试收益。

限制：历史测试反馈及研究者已接触测试信息的事实不能抹去。预揭示模型哈希锚定的是架构与特征名；这一新的直接收益目标和完整执行协议是本次才冻结，不能宣称整个新方案早在9月28日前已固定。当前数据使用与执行检查已通过，比赛提交资格仍由组委会认定。旧37模型方案的合规更正继续有效。这份预测与旧37模型分析报告对应不同方案。

## 重现推理

安装lightgbm、numpy、polars。将本目录作为工作目录，替换下列数据路径：

```powershell
python -B -X utf8 train_only_baseline143_inference_v2_20261011.py --stage infer --work-dir . --train-csv 'D:/路径/训练集.csv' --test-x 'D:/路径/测试集_X.csv'
```

评分另需pandas、scipy、loguru。训练、评分、最终训练的原入口是train_only_baseline143_v1_20261011.py，分别使用train、score、final阶段；推理使用上述v2入口。freeze阶段需原历史架构哈希锚定目录，已有封存协议不得覆盖。训练会生成约1.7GB的本地特征缓存，不需要读取测试答案。

submission.csv SHA256: {v['submission_sha256']}
final model SHA256: {v['final_model_sha256']}
'''
    (d/'README.md').write_text(text,encoding='utf-8',newline='\n')
    manifest={p.name:b.sha(p) for p in d.iterdir() if p.is_file() and p.suffix!='.zip' and p.name!='manifest.json'}
    b.put(d/'manifest.json',manifest)
    archive=d/'赛题五_固定训练内基线143_20261011.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in d.iterdir():
            if p.is_file() and p!=archive:z.write(p,p.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for n,h in manifest.items():assert hashlib.sha256(z.read(n)).hexdigest()==h
    b.put(w/'delivery.json',{'status':'verified_fixed_baseline_with_column_aligned_inference_packaged',
        'path':str(d),'archive':str(archive),'archive_sha256':b.sha(archive),'archive_bytes':archive.stat().st_size,
        'submission_sha256':b.sha(d/'submission.csv'),'official_TRAIN_score':v['official_TRAIN_score'],
        'saved_models':6,'final_prediction_models':1,'official_TEST_score':None,'competition_upload_performed':False})
    b.log(f'Package and every ZIP entry verified: {d}')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--stage',choices=['infer','package'],required=True)
    p.add_argument('--work-dir',type=Path,default=Path('E:/赛题五_本机临时/固定训练内基线143_20261011'))
    p.add_argument('--train-csv',type=Path,default=b.ROOT/'data/raw/训练集.csv')
    p.add_argument('--test-x',type=Path,default=b.ROOT/'data/raw/测试集_X.csv')
    p.add_argument('--control-root',type=Path)
    p.add_argument('--delivery-dir',type=Path,default=Path('E:/赛题五_最终提交/固定训练内基线143_20261011'))
    a=p.parse_args();a.work_dir=a.work_dir.resolve()
    if a.stage=='infer':prepare_adapter(a);b.infer(a)
    else:package(a)


if __name__=='__main__':main()
