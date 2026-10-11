"""Repair the prefix audit for stock-major original TEST row order.

Predictions, features, original TRAIN source, protocol and all six models are
unchanged. Date-prefix checks must mask the full output, not take its first N rows.
"""
from pathlib import Path
import argparse,hashlib,inspect,shutil,zipfile
import train_only_baseline143_v1_20261011 as b
import train_only_baseline143_inference_v2_20261011 as v2


def prepare(a):
    v2.prepare_adapter(a)
    w=a.work_dir;p=Path(__file__);target=w/p.name
    if target.resolve()!=p.resolve():shutil.copyfile(p,target)
    original=inspect.getsource(b.infer)
    old='exact(pred[:len(p)],p)'
    new="exact(pred[f['trade_date'].to_numpy()<=cut],p)"
    assert original.count(old)==1
    protocol=b.protocol(a)
    assert b.sha(Path(b.__file__))==protocol['source_sha256'][Path(b.__file__).name]
    patched=original.replace(old,new)
    # The single changed statement only chooses rows for an equality assertion.
    exec(compile(patched,'<baseline143_original_row_order_prefix_check_v3>','exec'),b.__dict__)
    record=w/'inference_prefix_audit_alignment_v3.json'
    info={'status':'date_mask_only_prefix_audit_repair','at_local':b.now(),
          'reason':'Original TEST rows are stock-major. Its first N rows are not its first 80 dates.',
          'old_assertion':old,'new_assertion':new,'adapter_sha256':b.sha(target),
          'only_assertion_row_selection_changed':True,'prediction_computation_unchanged':True,
          'original_training_source_model_feature_protocol_unchanged':True,
          'no_scientific_choice_based_on_TEST_outcomes':True,
          'previous_unverified_submission_sha256':b.sha(w/'submission.csv') if (w/'submission.csv').exists() else None}
    if record.exists():assert b.read(record)['adapter_sha256']==info['adapter_sha256']
    else:b.put(record,info)
    failure=w/'second_inference_audit_failure.json'
    if not failure.exists():b.put(failure,{'status':'retained_prefix_audit_index_failure',
          'at_local':'2026-10-11T22:13:11+08:00',
          'actual_feature_prefix_equal':True,'full_CSV_keys_and_finiteness_passed':True,
          'error':'Prediction prefix was compared with head(N) instead of date-filtered stock-major rows.',
          'TEST_outcomes_read_or_reconstructed':False})


def package(a):
    b.guard(a,'package completed baseline with original-row-order-aware prefix audit')
    w=a.work_dir;v=b.read(w/'verification.json');assert v['status'].startswith('passed_')
    assert v['cold80_original_row_order_filtered_by_date']
    d=a.delivery_dir;d.mkdir(parents=True,exist_ok=True)
    names=['train_only_baseline143_v1_20261011.py','train_only_features143_v1_20261011.py',
           'train_only_baseline143_inference_v2_20261011.py',Path(__file__).name,
           'inference_adapter_frozen_before_TEST_inference.json','inference_prefix_audit_alignment_v3.json',
           'first_inference_failure.json','second_inference_audit_failure.json',
           'evaluate.py','protocol.json','protocol.sha256','synthetic_causality.json',
           'model_final.txt','model_final.json','official_TRAIN_metrics.json',
           'frozen_before_TEST_inference.json','verification.json','submission.csv']
    for y in range(2020,2025):names += [f'model_{y}.txt',f'model_{y}.json']
    for n in names:shutil.copyfile(w/n,d/n)
    text=f'''# 固定训练内基线143：未来一天收益预测

用户指令：训练符合要求的模型。本轮直接拟合原始训练集的一天收益率，采用测试收益揭示前已存在的63项量价特征及LightGBM参数：31叶、180轮、学习率0.05、种子2026。只有一个候选，科学设计在本轮首次训练和评分前冻结。当前执行的模型、特征、参数、输出不使用历史测试评分来选择，不继承历史赢家、教师信号、成员与排序分离或后处理。

训练内部2020—2024年逐年向前预测连续连接，共1,212日、5,635,800行。未修改官方evaluate.py，综合分为 **{v['official_TRAIN_score']:.10f}**。这是训练验证分，不是比赛平台测试成绩，也不代表所有模型中最优。各年度标签的结束日期严格早于验证开始；最终训练剔除训练集末日标签。特征在计算前移除标签列，滚动使用本股票当前/历史行情，截面排名仅使用同日数据。预测时点为当日行情完整获得之后。

完成5次年度训练、1次最终训练；最终推理只用1个模型。保留5个年度模型供审计。测试预测覆盖1,599,600行、344日、4,650只股票，主键和顺序与测试输入相同，pred为未来一天收益率小数。模型重载、全量CSV重放及80日特征/预测前缀一致性均通过。

推理中修正了两个实现问题：历史/测试连接列顺序不一致；80日核验把按股票排列的原始文件误当按日期排列。v2仅对齐输入列，v3仅按日期筛选原文件位置后比较前缀。特征与模型输出计算、原训练/评分代码及科学协议保留原哈希。两次失败及修复记录均保留。当前执行不重建或使用测试收益。

限制：历史测试反馈及研究者已接触测试信息的事实不能抹去。预揭示模型哈希锚定的是架构和特征名；这一新的直接收益目标和完整执行协议在本次才冻结，不能宣称整个新方案早在9月28日前已固定。当前数据使用与执行检查通过，比赛提交资格仍由组委会认定。旧37模型方案的合规更正继续有效。这份预测与旧37模型分析报告对应不同方案。

## 重现推理

安装lightgbm、numpy、polars。进入本目录，替换数据路径后运行：

```powershell
python -B -X utf8 train_only_baseline143_inference_v3_20261011.py --stage infer --work-dir . --train-csv 'D:/路径/训练集.csv' --test-x 'D:/路径/测试集_X.csv'
```

评分另需pandas、scipy、loguru。训练、评分、最终训练使用原始train_only_baseline143_v1_20261011.py的train、score、final阶段；推理使用上述v3入口。freeze阶段需原历史架构哈希锚定目录，已有协议不得覆盖。训练会生成约1.7GB本地特征缓存。预测只选取行情字段，不读取数据文件中的标签列。

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
    b.put(w/'delivery.json',{'status':'verified_fixed_baseline_with_aligned_prefix_audit_packaged',
        'path':str(d),'archive':str(archive),'archive_sha256':b.sha(archive),'archive_bytes':archive.stat().st_size,
        'submission_sha256':b.sha(d/'submission.csv'),'official_TRAIN_score':v['official_TRAIN_score'],
        'saved_models':6,'final_prediction_models':1,'official_TEST_score':None,'competition_upload_performed':False})
    b.log(f'Complete package and ZIP hashes verified: {d}')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--stage',choices=['infer','package'],required=True)
    p.add_argument('--work-dir',type=Path,default=Path('E:/赛题五_本机临时/固定训练内基线143_20261011'))
    p.add_argument('--train-csv',type=Path,default=b.ROOT/'data/raw/训练集.csv')
    p.add_argument('--test-x',type=Path,default=b.ROOT/'data/raw/测试集_X.csv')
    p.add_argument('--control-root',type=Path)
    p.add_argument('--delivery-dir',type=Path,default=Path('E:/赛题五_最终提交/固定训练内基线143_20261011'))
    a=p.parse_args();a.work_dir=a.work_dir.resolve()
    if a.stage=='infer':
        prepare(a);b.infer(a)
        v=b.read(a.work_dir/'verification.json');v['cold80_original_row_order_filtered_by_date']=True
        v['column_order_and_prefix_audit_patch_records_preserved']=True
        b.put(a.work_dir/'verification.json',v)
    else:package(a)


if __name__=='__main__':main()
