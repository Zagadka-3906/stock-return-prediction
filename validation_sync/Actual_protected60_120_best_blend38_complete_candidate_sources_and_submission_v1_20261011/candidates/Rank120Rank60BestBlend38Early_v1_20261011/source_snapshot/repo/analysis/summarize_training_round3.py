"""Publish the completed training-only round3 record and its research summary."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'analysis/optimization_20261003_r3'
CANDIDATE = ROOT/'candidates/optimization_20261003_r3'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):
            value.update(block)
    return value.hexdigest()


def dump(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def main():
    selection = read(OUT/'selection.json')
    validation = read(OUT/'causal_validation.json')
    prediction = read(CANDIDATE/'verification.json')
    prior = read(ROOT/'results/optimization_20261003_r2.json')
    assert validation['status']==prediction['status']=='passed'
    assert sha(CANDIDATE/'submission.csv')==prediction['csv_sha256']
    assert prediction['old_delivery_pointer_unchanged']
    audits = [read(path) for path in (OUT/'raw').glob('*.json')]
    assert len(audits)==65
    assert all(a['model_reload_bit_identical'] and a['cached_source_control_bit_identical'] and a['same_training_keys_and_labels'] for a in audits)
    assert len({(a['seed'],a['year']) for a in audits})==15
    winner = selection['winner']
    baseline = prior['winner']['metrics']
    delta = {key:winner['metrics'][key]-baseline[key] for key in ('ic_mean','annual_excess','mean_turnover')}
    contributions = {'IC':0.4*delta['ic_mean'],'excess':0.3*delta['annual_excess'],'turnover':-0.3*delta['mean_turnover']}
    assert abs(sum(contributions.values())-selection['score_gain'])<1e-12
    sources = [ROOT/'analysis/optimize_training_round3.py',ROOT/'analysis/finalize_training_round3.py',Path(__file__)]
    result = {'status':'complete','scope':'waves47-49','winner':winner,'baseline_score':selection['baseline_score'],
        'score_gain':selection['score_gain'],'scored_records':selection['scored_records'],
        'total_scored_records_including_repeats':prior['total_scored_records_including_repeats']+selection['scored_records'],
        'new_fold_models_trained':0,'saved_fold_models_used':15,'checkpoint_predictions':65,
        'cached_source_controls_passed':15,'same_samples_and_mature_labels':True,
        'official_metric_change':delta,'score_contribution_change':contributions,
        'validation':validation,'prediction':prediction,'candidate_submission':str(CANDIDATE/'submission.csv'),
        'selection_rule':selection['selection_rule'],'test_labels_read_this_round':False,'test_score_of_this_candidate':None,
        'historical_test_best':{'arm':'wave13','score':0.417099224},
        'historical_test_best_scope':'previously disclosed written-CSV results; not used for selection',
        'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
        'previous_complete_deliveries_and_pointers_preserved':True,
        'boundary_label_maturity_audit':read(ROOT/'analysis/optimization_20261003_r2/boundary_maturity.json'),
        'source_sha256':{path.relative_to(ROOT).as_posix():sha(path) for path in sources}}
    dump(ROOT/'results/optimization_20261003_r3.json',result)
    dump(ROOT/'results/optimization_ranking_20261003_r3.json',{'status':'complete','ranking':selection['ranking']})
    dump(CANDIDATE/'manifest.json',{'status':'passed','files':{path.relative_to(CANDIDATE).as_posix():
         {'sha256':sha(path),'bytes':path.stat().st_size} for path in sorted(CANDIDATE.rglob('*'))
         if path.is_file() and path.name!='manifest.json'}})
    heading = '### 第三轮继续优化（波47–49）'
    end = '<!-- optimization20261003r3 end -->'
    recipe = winner['recipe']
    post = recipe['postprocessing']
    detail = (f'训练目标比例{recipe["fraction"]:.1%}、种子{recipe["seed"]}、{recipe["rounds"]}轮'
              if recipe['type']=='model' else '原始日排名集成：'+
              '、'.join(f'{c["rounds"]}轮×{c["weight"]:.0%}' for c in recipe['components']))
    section = (f'{heading}\n\n'
        f'复用15个已保存年度模型，新增65组检查点预测及{selection["scored_records"]}条完整方案评分记录；'
        '未重复年度模型训练。15个来源模型均精确复现原缓存，所有方案使用相同样本、标签成熟边界及官方评分。'
        '先比较三个种子的检查点与原始分数集成，再比较平滑、辅助排序及最终输出参数。\n\n'
        f'本轮最高连接验证分 **{winner["connected_final_score"]:.9f}**，较上一轮 **{selection["score_gain"]:+.9f}**。'
        f'{detail}；成员来源平滑alpha={post["alpha"]:g}、bonus={post["bonus"]:g}、辅助权重{post["weight"]:g}；'
        f'排序slow16权重{winner["slow16_weight"]:.1%}、成员留存{winner["retention"]:.1%}、涨停排序偏移{winner["limit_up_delta"]:+g}。'
        '选定方案冻结后，因果收益率映射及官方评分复核、历史前缀重放、最终模型重载和CSV逐字节重放均通过。\n\n'
        '本轮未读取测试标签，候选无新增测试评分；历史测试回顾最佳仍为波13的0.417099224。'
        '既有交付和版本指针保留，新候选位于`candidates/optimization_20261003_r3/submission.csv`。'
        '详细结果见[第三轮优化记录](results/optimization_20261003_r3.json)。验证年份均已参与此前研究，未校正多次搜索带来的选择偏差。\n\n'
        '复现顺序：`analysis/optimize_training_round3.py`的freeze、checkpoints、models、smoothing、refine；'
        '再运行`analysis/finalize_training_round3.py`的select、calibrate、predict。\n\n'+end+'\n\n')
    path = ROOT/'README.md'
    original = path.read_text(encoding='utf-8')
    if heading in original:
        start = original.index(heading)
        stop = original.index(end,start)+len(end)
        original = original[:start]+original[stop:].lstrip('\n')
    anchor = '以下内容保留原67特征16种子基准的研究和运行说明。'
    assert anchor in original
    path.write_text(original.replace(anchor,section+anchor,1),encoding='utf-8')
    print(json.dumps({'score':winner['connected_final_score'],'gain':selection['score_gain'],
                      'records':selection['scored_records'],'candidate':str(CANDIDATE/'submission.csv')},ensure_ascii=False))


if __name__=='__main__':
    main()
